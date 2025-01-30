from themes.theme import Theme

from utils.fen import render_chessboard

def render_from_fen(fen: str, theme: Theme, output_file: str) -> None:
    """
    Render a chessboard image from a FEN string and save it to a file.

    Args:
        fen (str): The FEN string representing the chessboard state.
        theme (Theme): The theme object containing the board and piece images.
        output_file (str): The file path to save the generated image.
    """
    render_chessboard(fen,theme,output_file)

def render_from_fen_file(fen_file: str, theme: Theme, output_file: str) -> None:
    """
    Render a chessboard image from a FEN file and save it to a file.

    Args:
        fen_file (str): Path to the FEN file.
        theme (Theme): The theme object containing the board and piece images.
        output_file (str): The file path to save the generated image.
    """
    # Read the FEN string from the file
    with open(fen_file, "r", encoding="utf-8") as file:
        fen = file.read().strip()
    render_chessboard(fen,theme,output_file)
