import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")


@st.cache_resource
def summary_text(text):
    summary = Summary()
    result = summary(text)
    return result


# Extract text from the pdf file using PyPDF2
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text


# Initialize session state for the summarized result
if "summary_result" not in st.session_state:
    st.session_state.summary_result = ""

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("SUMMARIZING YOUR TEXT USING TEXTAI")
    st.write("This is a text summarization app")

    st.session_state.input_text = st.text_area("Enter your text here", value=st.session_state.input_text, key="text_input_area")

    if st.button("Summarize Text"):
        # Perform summarization
        st.session_state.summary_result = summary_text(st.session_state.input_text)

    if st.session_state.summary_result:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Your Input Text**")
            st.info(st.session_state.input_text)
        with col2:
            st.markdown("**Summarized Text**")
            st.text_area("Copy your summarized text", st.session_state.summary_result, height=200, key="summarized_text_area")
            st.download_button(
                label="Download Summary",
                data=st.session_state.summary_result,
                file_name="summary.txt",
                mime="text/plain",
                key="download_summary_text"
            )

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document", type=["pdf"])
    if input_file:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            # Extract text from the document
            extracted_text = extract_text_from_pdf("doc_file.pdf")
            # Perform summarization
            st.session_state.summary_result = summary_text(extracted_text)

    if st.session_state.summary_result:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Extracted Text from Document**")
            st.info(extracted_text)
        with col2:
            st.markdown("**Summarized Document**")
            st.text_area("Copy your summarized document", st.session_state.summary_result, height=200, key="summarized_document_area")
            st.download_button(
                label="Download Summary",
                data=st.session_state.summary_result,
                file_name="document_summary.txt",
                mime="text/plain",
                key="download_summary_document"
            )
