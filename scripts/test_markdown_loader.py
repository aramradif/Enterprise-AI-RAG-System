from app.ingestion.markdown_loader import load_markdown

text = load_markdown("data/sample.md")

print(text)