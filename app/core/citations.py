from pathlib import Path
from typing import Any


def build_citations(
    context: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Extract unique citation records from selected RAG context.

    Each citation contains:
    - source filename;
    - chunk number;
    - retrieval method.

    Duplicate source-and-chunk combinations are removed while
    preserving the order in which documents were selected.
    """

    citations: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()

    for document in context:
        if not isinstance(document, dict):
            continue

        raw_source = document.get(
            "source",
            "Unknown source",
        )

        source = Path(
            str(raw_source)
        ).name

        raw_chunk = document.get(
            "chunk",
            0,
        )

        try:
            chunk = int(raw_chunk)
        except (TypeError, ValueError):
            chunk = 0

        retrieval = str(
            document.get(
                "retrieval",
                "unknown",
            )
        )

        citation_key = (
            source,
            chunk,
        )

        if citation_key in seen:
            continue

        seen.add(citation_key)

        citations.append(
            {
                "source": source,
                "chunk": chunk,
                "retrieval": retrieval,
            }
        )

    return citations


def format_citations(
    citations: list[dict[str, Any]],
) -> str:
    """
    Format citation records as a readable answer section.

    Example:

    Sources:
    - handbook.txt — Chunk 3
    - faq.docx — Chunk 1
    """

    if not citations:
        return ""

    citation_lines = [
        "\n\nSources:",
    ]

    for citation in citations:
        source = citation["source"]
        chunk = citation["chunk"]

        citation_lines.append(
            f"- {source} — Chunk {chunk}"
        )

    return "\n".join(
        citation_lines
    )


def attach_citations(
    answer: str,
    context: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    """
    Add a deterministic citation section to a generated answer.

    Returns:
        cited_answer:
            The original answer followed by its source list.

        citations:
            Structured citation records that can also be returned
            through APIs or displayed separately in the frontend.
    """

    citations = build_citations(
        context,
    )

    citation_text = format_citations(
        citations,
    )

    cited_answer = answer.strip()

    if citation_text:
        cited_answer += citation_text

    return (
        cited_answer,
        citations,
    )