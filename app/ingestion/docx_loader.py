from docx import Document


def load_docx(file_path: str) -> str:
    """
    Load a DOCX file and return its text.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)