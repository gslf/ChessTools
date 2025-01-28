from PIL import Image
from themes.theme import Theme
from image_processing.fen_to_image import FENToImage
from chess import pgn 
import io

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
        import os
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
        import os
        board = game.board()
        move_number = 0

        if final_position_only:
            for move in game.mainline_moves():
                board.push(move)
            fen = board.fen()
            output_file = os.path.join(output_dir, f"final_position.png")
            self._render_from_fen(fen, output_file)
        else:
            for move in game.mainline_moves():
                board.push(move)
                fen = board.fen()
                move_number += 1
                output_file = os.path.join(output_dir, f"move_{move_number}.png")
                self._render_from_fen(fen, output_file)

    def _render_from_fen(self, fen: str, output_file: str) -> None:
        """
        Render a chessboard image from a FEN string.

        Args:
            fen (str): The FEN string representing the chessboard state.
            output_file (str): The file path to save the generated image.
        """
        board_image = Image.open(self.theme.board_image).convert("RGBA")
        piece_positions = FENToImage._fen_to_positions(fen)

        for square, piece in piece_positions.items():
            if piece:
                piece_image_path = self.theme.piece_images[piece]
                piece_image = Image.open(piece_image_path).convert("RGBA")

                x, y = self.theme.squares[square]["x"], self.theme.squares[square]["y"]
                x -= piece_image.width // 2
                y -= piece_image.height // 2

                board_image.paste(piece_image, (x, y), piece_image)

        board_image.save(output_file)
