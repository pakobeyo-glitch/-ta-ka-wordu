import streamlit as st
from docx import Document
from io import BytesIO

st.set_page_config(
    page_title="Dokumenty",
    page_icon="📚"
)

st.title("📚 Dokumenty")

st.write("Nahraj Word dokument a zobrazí sa jeho text.")

uploaded_file = st.file_uploader(
    "Vyber Word dokument",
    type=["docx"]
)

if uploaded_file is not None:

    document = Document(
        BytesIO(uploaded_file.read())
    )

    text = "\n\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    st.subheader("Text dokumentu")

    st.text_area(
        "Obsah",
        text,
        height=500
    )
