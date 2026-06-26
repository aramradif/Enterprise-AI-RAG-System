from pathlib import Path


def load_txt(file_path: str) -> str:
    """
    Load a text file and return its contents.
    """

    path = Path(file_path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return file.read()