from app.ingestion.pdf_loader import load_pdf

text = load_pdf("data/sample.pdf")

print(text)