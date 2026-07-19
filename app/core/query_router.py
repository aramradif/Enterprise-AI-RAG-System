import re


CONVERSATION_PATTERNS = (
    r"\bwhat did we discuss\b",
    r"\bwhat have we discussed\b",
    r"\bsummarize (our|the) conversation\b",
    r"\bsummarize what we discussed\b",
    r"\bsummarize our discussion\b",
    r"\bwhat was my previous question\b",
    r"\bwhat did i ask\b",
    r"\bwhat did i say\b",
    r"\bwhat was your previous answer\b",
    r"\bwhat did you say\b",
    r"\bcontinue where we left off\b",
    r"\bcontinue our conversation\b",
    r"\bremind me what we discussed\b",
    r"\brecap (our|the) conversation\b",
    r"\brecap what we discussed\b",
    r"\bwhat were we talking about\b",
)


def is_conversation_question(
    question: str,
) -> bool:
    """
    Determine whether a question should be answered primarily
    from conversation memory instead of retrieved documents.

    Returns True for conversation-history questions such as:
    - What did we discuss?
    - Summarize our conversation.
    - What was my previous question?
    """

    normalized_question = re.sub(
        r"\s+",
        " ",
        question.strip().lower(),
    )

    if not normalized_question:
        return False

    return any(
        re.search(
            pattern,
            normalized_question,
        )
        for pattern in CONVERSATION_PATTERNS
    )