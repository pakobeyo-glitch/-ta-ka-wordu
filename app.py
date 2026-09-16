from flask import Flask, render_template, request, redirect
from docx import Document
import sqlite3
from io import BytesIO

app = Flask(__name__)


def get_db():
    return sqlite3.connect("documents.db")


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()


@app.route("/")
def index():
    db = get_db()

    documents = db.execute(
        "SELECT id, title FROM documents ORDER BY id DESC"
    ).fetchall()

    db.close()

    return render_template("index.html", documents=documents)


@app.route("/document/<int:document_id>")
def document(document_id):
    db = get_db()

    doc = db.execute(
        "SELECT id, title, text FROM documents WHERE id = ?",
        (document_id,)
    ).fetchone()

    db.close()

    if doc is None:
        return "Dokument neexistuje", 404

    return render_template("document.html", document=doc)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":

        file = request.files["file"]

        if not file.filename.endswith(".docx"):
            return "Nahraj súbor .docx"

        # Načítanie Word dokumentu
        document = Document(BytesIO(file.read()))

        # Vytiahnutie textu
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        title = file.filename

        db = get_db()

        db.execute(
            "INSERT INTO documents (title, text) VALUES (?, ?)",
            (title, text)
        )

        db.commit()
        db.close()

        return redirect("/")

    return render_template("admin.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
