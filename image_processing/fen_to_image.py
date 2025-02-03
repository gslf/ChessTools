from PIL import Image

from themes.theme import Theme
from utils.fen import fen_to_positions
from utils.utils import read_file

def render_from_fen(fen: str, theme: Theme, output_filename: str) -> None:
    """
    Render a chessboard image from a FEN string and save it to a file.

    Args:
        fen (str): The FEN string representing the chessboard state.
        theme (Theme): The theme object containing the board and piece images.
        output_filename (str): The file path to save the generated image.
    """
    board_image = Image.open(theme.board_image).convert("RGBA")
    piece_positions = fen_to_positions(fen)

    for square, piece in piece_positions.items():
        if piece:
            piece_image_path = theme.piece_images[piece]
            piece_image = Image.open(piece_image_path).convert("RGBA")
            x, y = theme.squares[square]["x"], theme.squares[square]["y"]
            x -= piece_image.width // 2
            y -= piece_image.height // 2
            board_image.paste(piece_image, (x, y), piece_image)
    
    board_image.save(f"{output_filename}.png")

def render_from_fen_file(fen_file: str, theme: Theme, output_filename: str) -> None:
    """
    Render a chessboard image from a FEN file and save it to a file.

    Args:
        fen_file (str): Path to the FEN file.
        theme (Theme): The theme object containing the board and piece images.
        output_file (str): The file path to save the generated image.
    """
    # Read the FEN string from the file
    fen_string = read_file(fen_file)
    render_from_fen(fen_string, theme,output_filename)
