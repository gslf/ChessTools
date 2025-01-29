from themes.theme import Theme
from chess import pgn 
from utils.fen import render_chessboard

import io
import os

class PGNToImage:
    """
    A class to generate chessboard images from a PGN string, PGN file, or all PGN files in a folder.
    """

    def __init__(self, theme: Theme):
        """
        Initialize the PGNToImage generator.

        Args:
            theme (Theme): A Theme object containing board and piece images.
        """
        self.theme = theme

    def render_from_pgn_string(self, pgn_string: str, output_dir: str, final_position_only: bool = True) -> None:
        """
        Render chessboard images from a PGN string.

        Args:
            pgn_string (str): The PGN string containing the chess game.
            output_dir (str): The directory to save the generated images.
            final_position_only (bool): If True, generate an image only for the final position.
        """
        game = pgn.read_game(io.StringIO(pgn_string))
        self._process_game(game, output_dir, final_position_only)

    def render_from_pgn_file(self, pgn_file: str, output_dir: str, final_position_only: bool = True) -> None:
        """
        Render chessboard images from a PGN file.

        Args:
            pgn_file (str): Path to the PGN file.
            output_dir (str): The directory to save the generated images.
            final_position_only (bool): If True, generate an image only for the final position.
        """
        with open(pgn_file, "r", encoding="utf-8") as file:
            game = pgn.read_game(file)
        self._process_game(game, output_dir, final_position_only)

    def render_from_pgn_folder(self, folder_path: str, output_dir: str, final_position_only: bool = True) -> None:
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
                self.render_from_pgn_file(pgn_path, output_dir, final_position_only)

    def _process_game(self, game, output_dir: str, final_position_only: bool) -> None:
        """
        Process a single game object and generate images.

        Args:
            game: The game object parsed from PGN.
            output_dir (str): The directory to save the generated images.
            final_position_only (bool): If True, generate an image only for the final position.
        """
        if game is None:
            raise ValueError("The game object is invalid or could not be parsed from the PGN.")

        board = game.board()
        move_number = 0

        if final_position_only:
            for move in game.mainline_moves():
                board.push(move)
            fen = board.fen()
            output_file = os.path.join(output_dir, "final_position.png")
            render_chessboard(fen, self.theme, output_file)
        else:
            for move in game.mainline_moves():
                board.push(move)
                fen = board.fen()
                move_number += 1
                output_file = os.path.join(output_dir, f"move_{move_number}.png")
                render_chessboard(fen, self.theme, output_file)