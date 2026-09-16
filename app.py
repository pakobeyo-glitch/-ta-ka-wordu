import streamlit as st
from docx import Document
from io import BytesIO

st.title("Word → Text")

uploaded_file = st.file_uploader(
    "Nahraj Word dokument",
    type=["docx"]
)

if uploaded_file:
    document = Document(BytesIO(uploaded_file.read()))

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    st.text_area("Vytiahnutý text", text, height=500)
