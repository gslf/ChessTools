import io
import os

from chess import pgn 

from image_processing.fen_to_image import render_from_fen
from utils.utils import read_file
from themes.theme import Theme




def render_from_pgn_string(pgn_string: str, theme: Theme, output_dir: str, output_filename: str, final_position_only: bool = True) -> None:
    """
    Render chessboard images from a PGN string.

    Args:
        pgn_string (str): The PGN string containing the chess game.
        output_dir (str): The directory to save the generated images.
        final_position_only (bool): If True, generate an image only for the final position.
    """
    game = pgn.read_game(io.StringIO(pgn_string))
    
    if game is None:
        raise ValueError("The game object is invalid or could not be parsed from the PGN.")

    board = game.board()
    move_number = 0

    if final_position_only:
        for move in game.mainline_moves():
            board.push(move)
        fen = board.fen()
        output_file = os.path.join(output_dir, output_filename)
        render_from_fen(fen, theme, output_file)
    else:
        for move in game.mainline_moves():
            board.push(move)
            fen = board.fen()
            move_number += 1
            output_file = os.path.join(output_dir, f"{output_filename}_{move_number}")
            render_from_fen(fen, theme, output_file)

def render_from_pgn_file(pgn_file: str, theme: Theme, output_dir: str, output_filename: str, final_position_only: bool = True) -> None:
    """
    Render chessboard images from a PGN file.

    Args:
        pgn_file (str): Path to the PGN file.
        output_dir (str): The directory to save the generated images.
        final_position_only (bool): If True, generate an image only for the final position.
    """
    pgn_string = read_file(pgn_file)
    render_from_pgn_string(pgn_string, theme, output_dir, output_filename, final_position_only)

def render_from_pgn_folder(folder_path: str, theme: Theme, output_dir: str, final_position_only: bool = True) -> None:
    """
    Render chessboard images from all PGN files in a folder.

    Args:
        folder_path (str): Path to the folder containing PGN files.
        output_dir (str): The directory to save the generated images.
        final_position_only (bool): If True, generate an image only for the final position.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pgn"):
            pgn_path = os.path.join(folder_path, file_name)
            output_filename = os.path.splitext(file_name)[0]
            render_from_pgn_file(pgn_path, theme, output_dir, output_filename, final_position_only)