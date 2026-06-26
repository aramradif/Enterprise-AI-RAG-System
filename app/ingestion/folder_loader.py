from pathlib import Path

from app.ingestion.txt_loader import load_txt
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.docx_loader import load_docx
from app.ingestion.markdown_loader import load_markdown


def load_documents(folder_path: str):

    documents = []

    folder = Path(folder_path)

    for file in folder.iterdir():

        if file.is_dir():
            continue

        suffix = file.suffix.lower()

        text = None

        if suffix == ".txt":
            text = load_txt(file)

        elif suffix == ".pdf":
            text = load_pdf(file)

        elif suffix == ".docx":
            text = load_docx(file)

        elif suffix == ".md":
            text = load_markdown(file)

        else:
            continue

        documents.append(
            {
                "filename": file.name,
                "content": text,
            }
        )

    return documents