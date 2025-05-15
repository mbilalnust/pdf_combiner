from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
from io import BytesIO

# Title of the app
st.title("PDF Merger")

# File uploader for PDF files
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# Initialize session state for file order
if 'file_order' not in st.session_state:
    st.session_state.file_order = []

# Update session state with uploaded files
if uploaded_files:
    st.session_state.file_order = uploaded_files

# Allow users to arrange the order of the uploaded files
if st.session_state.file_order:
    st.write("Arrange the order of the files:")
    file_order = st.multiselect("Select the order of files", options=[file.name for file in st.session_state.file_order], default=[file.name for file in st.session_state.file_order])

    # Button to merge PDFs
    if st.button("Merge PDFs"):
        if file_order:
            pdf_writer = PdfWriter()
            
            # Read and add each uploaded PDF in the selected order
            for file_name in file_order:
                for uploaded_file in st.session_state.file_order:
                    if uploaded_file.name == file_name:
                        pdf_reader = PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)

            # Create a BytesIO object to hold the merged PDF
            merged_pdf = BytesIO()
            pdf_writer.write(merged_pdf)
            merged_pdf.seek(0)

            # Provide a download link for the merged PDF
            st.download_button(
                label="Download Merged PDF",
                data=merged_pdf,
                file_name="combined_resume_portfolio.pdf",
                mime="application/pdf"
            )
            st.success("PDFs merged successfully!")
        else:
            st.warning("Please select the order of the files.")
else:
    st.warning("Please upload at least one PDF file.")
