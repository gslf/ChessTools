def read_file(filepath: str) -> str:
    """
    Read the contents of a file and return it as a string.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The contents of the file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().strip()