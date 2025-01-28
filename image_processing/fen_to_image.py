from PIL import Image
from themes.theme import Theme


class FENToImage:
    """
    A class to generate a chessboard image from a FEN string or FEN file, using a specific theme.
    """

    def __init__(self, theme: Theme):
        """
        Initialize the FENToImage generator.

        Args:
            theme (Theme): A Theme object containing board and piece images.
        """
        self.theme = theme

    def render_from_fen(self, fen: str, output_file: str) -> None:
        """
        Render a chessboard image from a FEN string and save it to a file.

        Args:
            fen (str): The FEN string representing the chessboard state.
            output_file (str): The file path to save the generated image.
        """
        # Load the board background image
        board_image = Image.open(self.theme.board_image).convert("RGBA")
        piece_positions = self._fen_to_positions(fen)

        # Place each piece on the board
        for square, piece in piece_positions.items():
            if piece:
                piece_image_path = self.theme.piece_images[piece]
                piece_image = Image.open(piece_image_path).convert("RGBA")

                # Get the square's coordinates from the theme
                x, y = self.theme.squares[square]["x"], self.theme.squares[square]["y"]
                x = x - (piece_image.width // 2)
                y = y - (piece_image.height // 2)
                
                # Overlay the piece image onto the board
                board_image.paste(piece_image, (x, y), piece_image)

        # Save the final image
        board_image.save(output_file)

    def render_from_fen_file(self, fen_file: str, output_file: str) -> None:
        """
        Render a chessboard image from a FEN file and save it to a file.

        Args:
            fen_file (str): Path to the FEN file.
            output_file (str): The file path to save the generated image.
        """
        # Read the FEN string from the file
        with open(fen_file, "r", encoding="utf-8") as file:
            fen = file.read().strip()
        self.render_from_fen(fen, output_file)

    @staticmethod
    def _fen_to_positions(fen: str) -> dict:
        """
        Convert a FEN string into a dictionary of piece positions.

        Args:
            fen (str): The FEN string representing the chessboard state.

        Returns:
            dict: A dictionary with square names as keys and piece codes as values.
        """
        positions = {}
        rows = fen.split()[0].split("/")
        for rank_index, row in enumerate(rows):
            file_index = 0
            for char in row:
                if char.isdigit():
                    # Empty squares
                    file_index += int(char)
                else:
                    # Piece on the square
                    square = chr(97 + file_index) + str(8 - rank_index)  # Convert file and rank to algebraic notation
                    piece = ("b" if char.islower() else "w") + char.lower()
                    positions[square] = piece
                    file_index += 1
        return positions
