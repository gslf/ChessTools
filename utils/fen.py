from typing import Optional
import io

from PIL import Image
from chess import pgn

from themes.theme import Theme


def fen_to_positions(fen: str) -> dict:
    """
    Convert a FEN string into a dictionary of piece positions.

    Args:
        fen (str): The FEN string representing the chessboard state.

    Returns:
        dict: A dictionary with square names as keys and piece codes as values.

    Raises:
        ValueError: If the FEN string is not valid.
    """
    if not fen or " " not in fen:
        raise ValueError("Invalid FEN string: missing required fields")

    rows = fen.split()[0].split("/")
    
    if len(rows) != 8:
        raise ValueError("Invalid FEN string: must contain exactly 8 rows")

    positions = {}
    
    for rank_index, row in enumerate(rows):
        file_index = 0
        row_sum = 0  # Track the number of columns in the row
        
        for char in row:
            if char.isdigit():
                row_sum += int(char)
                file_index += int(char)
            elif char.isalpha() and char in "prnbqkPRNBQK":
                if file_index >= 8:
                    raise ValueError(f"Invalid FEN string: too many pieces in row {8 - rank_index}")
                square = chr(97 + file_index) + str(8 - rank_index)  # Convert file and rank to algebraic notation
                piece = ("b" if char.islower() else "w") + char.lower()
                positions[square] = piece
                file_index += 1
                row_sum += 1
            else:
                raise ValueError(f"Invalid FEN string: invalid character '{char}' in row {8 - rank_index}")

        if row_sum != 8:
            raise ValueError(f"Invalid FEN string: row {8 - rank_index} does not have exactly 8 columns")

    return positions

def pgn_to_fen(pgn_string: str) -> Optional[str]:
    """
    Extract the final position FEN from a PGN string.

    Args:
        pgn_string (str): The PGN string containing the chess game.

    Returns:
        str: The FEN representation of the final position.
    """
    game = pgn.read_game(io.StringIO(pgn_string))
    
    if game is None: 
        return None  

    board = game.board()  
    for move in game.mainline_moves():
        board.push(move)

    return board.fen()

def render_chessboard(fen: str, theme: Theme, output_file: str) -> None:
    """
    Render a chessboard image from a FEN string and save it to a file.

    Args:
        fen (str): The FEN string representing the chessboard state.
        theme: A Theme object containing board and piece images.
        output_file (str): The file path to save the generated image.
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
    
    board_image.save(output_file)