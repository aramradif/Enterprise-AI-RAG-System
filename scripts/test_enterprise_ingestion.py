from app.ingestion.folder_loader import load_documents
from app.ingestion.chunking import chunk_text
from app.retrieval.indexing import index_chunks

documents = load_documents("data")

total_chunks = 0

for document in documents:

    chunks = chunk_text(document["content"])

    index_chunks(
        chunks,
        source=document["filename"],
    )

    total_chunks += len(chunks)

print()
print(f"Indexed {len(documents)} documents.")
print(f"Indexed {total_chunks} chunks.")