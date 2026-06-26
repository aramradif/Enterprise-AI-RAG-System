from markdown import markdown
from bs4 import BeautifulSoup


def load_markdown(file_path: str) -> str:
    """
    Load a Markdown file and return plain text.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        md = file.read()

    html = markdown(md)

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    return soup.get_text(separator="\n")