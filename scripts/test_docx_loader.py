from app.ingestion.docx_loader import load_docx

text = load_docx("data/sample.docx")

print(text)