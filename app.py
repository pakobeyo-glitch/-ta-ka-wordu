import streamlit as st
from docx import Document
from io import BytesIO
import sqlite3


# -------------------------
# NASTAVENIA
# -------------------------

ADMIN_PASSWORD = "admin123"
DATABASE = "documents.db"


# -------------------------
# DATABÁZA
# -------------------------

def init_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_document(filename, text):
    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "INSERT INTO documents (filename, text) VALUES (?, ?)",
        (filename, text)
    )

    connection.commit()
    connection.close()


def get_documents():
    connection = sqlite3.connect(DATABASE)

    documents = connection.execute(
        "SELECT id, filename, text FROM documents ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return documents


def delete_document(document_id):
    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    connection.commit()
    connection.close()


# -------------------------
# SPUSTENIE DATABÁZY
# -------------------------

init_database()


# -------------------------
# STRÁNKA
# -------------------------

st.set_page_config(
    page_title="Dokumenty",
    page_icon="📚"
)

st.title("📚 Dokumenty")


# -------------------------
# SIDEBAR - ADMIN
# -------------------------

with st.sidebar:

    st.header("🔐 Správca")

    password = st.text_input(
        "Heslo",
        type="password"
    )

    if st.button("Prihlásiť sa"):

        if password == ADMIN_PASSWORD:
            st.session_state["admin"] = True
            st.success("Prihlásenie úspešné!")

        else:
            st.session_state["admin"] = False
            st.error("Nesprávne heslo.")


# -------------------------
# ADMIN PANEL
# -------------------------

if st.session_state.get("admin", False):

    st.sidebar.divider()

    st.sidebar.subheader("⚙️ Administrácia")

    uploaded_file = st.sidebar.file_uploader(
        "Pridať Word dokument",
        type=["docx"]
    )

    if uploaded_file is not None:

        if st.sidebar.button("📤 Pridať dokument"):

            document = Document(
                BytesIO(uploaded_file.read())
            )

            text = "\n\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

            add_document(
                uploaded_file.name,
                text
            )

            st.sidebar.success(
                "Dokument bol pridaný!"
            )

            st.rerun()


# -------------------------
# ZOBRAZENIE DOKUMENTOV
# -------------------------

documents = get_documents()


if not documents:

    st.info("📭 Správca zatiaľ nič nepridal.")

else:

    st.subheader("Dostupné dokumenty")

    for document_id, filename, text in documents:

        with st.expander(f"📄 {filename}"):

            st.text(text)

            # Mazanie môže používať iba správca
            if st.session_state.get("admin", False):

                if st.button(
                    "🗑️ Vymazať",
                    key=f"delete_{document_id}"
                ):

                    delete_document(document_id)

                    st.success("Dokument bol vymazaný.")

                    st.rerun()
