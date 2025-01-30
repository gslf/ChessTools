import os
import unittest
import tempfile

from themes.theme import Theme
from image_processing.fen_to_image import render_from_fen, render_from_fen_file


class TestFENToImage(unittest.TestCase):
    """Unit tests for the FENToImage class."""

    def setUp(self) -> None:
        """Set up mock data and theme for testing."""
        self.output_dir = tempfile.TemporaryDirectory()

        self.theme = Theme.from_file("themes/assets/standard/config.json")
        self.fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.test_output = os.path.join(self.output_dir.name, "test.png")
        

    def tearDown(self) -> None:
        """Clean up the temporary directory."""
        self.output_dir.cleanup()

    # render_from_fen_string OK
    def test_render_from_fen_string(self):
        """Test a standard rendering from a PGN string."""
        render_from_fen(self.fen_string, self.theme, self.test_output)

        self.assertTrue(os.path.exists(self.test_output))
        os.remove(self.test_output)

    # render_from_fen_string INVALID STRING
    def test_render_from_fen_string_invalid(self):
        """Test rendering from an invalid FEN string."""
        with self.assertRaises(ValueError):
            render_from_fen("invalid", self.theme, self.test_output)

    # render_from_fen_file OK
    def test_render_from_fen_file(self):
        """Test rendering from a valid FEN file."""
        with tempfile.NamedTemporaryFile(suffix=".fen", mode='w', delete=False) as tmp_fen:
            tmp_fen.write(self.fen_string)
            tmp_fen_path = tmp_fen.name

        render_from_fen_file(tmp_fen_path, self.theme, self.test_output)

        self.assertTrue(os.path.exists(self.test_output))
        os.remove(self.test_output)

    # render_from_fen_string INVALID FILE
    def test_render_from_fen_file_invalid(self):
        """Test rendering from an invalid FEN file."""
        with tempfile.NamedTemporaryFile(suffix=".fen", mode='w', delete=False) as tmp_fen:
            tmp_fen.write("invalid")
            tmp_fen_path = tmp_fen.name

        with self.assertRaises(ValueError):
            render_from_fen_file(tmp_fen_path, self.theme, self.test_output)


    # render_from_fen_string NOT FOUND FILE
    def test_render_from_fen_file_notfound(self):
        """Test rendering from a non existent FEN file."""
        with self.assertRaises(FileNotFoundError):
            render_from_fen_file("non_existing.fen", self.theme, self.test_output)


if __name__ == "__main__":
    unittest.main()
