import json
import os
from typing import Dict, Any


class Theme:
    """
    Represents a chess theme, including board and piece images and square positions.
    """

    def __init__(self, name: str, board_image: str, piece_images: Dict[str, str], squares: Dict[str, Dict[str, int]]):
        """
        Initialize a Theme instance.

        Args:
            name (str): The name of the theme.
            board_image (str): The file name of the board image.
            piece_images (Dict[str, str]): Mapping of piece identifiers to image file names.
            squares (Dict[str, Dict[str, int]]): Mapping of square names to x, y coordinates.
        """
        self.name = name
        self.board_image = board_image
        self.piece_images = piece_images
        self.squares = squares

    @staticmethod
    def from_file(file_path: str) -> "Theme":
        """
        Create a Theme object from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            Theme: The Theme object created from the JSON data.
        """
        # Determine the base directory of the file path
        base_dir = os.path.dirname(file_path)
        
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        theme_data = data.get("theme", {})

        # Prepend the base directory to the board image and piece images if a directory exists
        board_image = os.path.join(base_dir, theme_data["boardImage"]) if base_dir else theme_data["boardImage"]
        piece_images = {
            piece: os.path.join(base_dir, image) if base_dir else image
            for piece, image in theme_data["pieceImages"].items()
        }

        return Theme(
            name=theme_data["name"],
            board_image=board_image,
            piece_images=piece_images,
            squares=theme_data["squares"]
        )

    @staticmethod
    def validate_theme(data: Dict[str, Any]) -> bool:
        """
        Validate the structure of theme data.

        Args:
            data (Dict[str, Any]): The data to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        required_keys = {"name", "boardImage", "pieceImages", "squares"}
        if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
            return False

        if not isinstance(data["pieceImages"], dict) or not isinstance(data["squares"], dict):
            return False

        return True

    def __repr__(self) -> str:
        """
        Return a string representation of the Theme object.

        Returns:
            str: The string representation.
        """
        return f"Theme(name='{self.name}', board_image='{self.board_image}')"
