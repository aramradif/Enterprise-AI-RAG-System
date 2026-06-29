from typing import List


def select_context(
    documents: List[str],
    max_documents: int = 3,
    max_characters: int = 4000,
) -> List[str]:
    """
    Select the best context for the LLM.

    Limits:
    - maximum number of retrieved documents
    - maximum total context size
    """

    selected = []
    total_chars = 0

    for document in documents:

        if len(selected) >= max_documents:
            break

        if total_chars + len(document) > max_characters:
            break

        selected.append(document)
        total_chars += len(document)

    return selected