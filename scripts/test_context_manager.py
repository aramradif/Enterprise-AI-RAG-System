from app.core.context_manager import select_context

documents = [
    "Document A " * 200,
    "Document B " * 200,
    "Document C " * 200,
    "Document D " * 200,
    "Document E " * 200,
]

print("Length of first document:", len(documents[0]))

selected = select_context(
    documents,
    max_documents=3,
    max_characters=5000,
)

print("Selected documents:", len(selected))

for i, doc in enumerate(selected):
    print(f"Document {i+1}: {len(doc)} characters")