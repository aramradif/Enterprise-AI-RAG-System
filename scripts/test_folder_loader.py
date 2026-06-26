from app.ingestion.folder_loader import load_documents

documents = load_documents("data")

print(f"\nLoaded {len(documents)} documents.\n")

for document in documents:

    print(document["filename"])