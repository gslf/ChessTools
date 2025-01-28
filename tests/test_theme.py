import unittest
from unittest.mock import mock_open, patch
from themes.theme import Theme


class TestTheme(unittest.TestCase):
    """Unit tests for the Theme class using mocks for file operations."""

    def setUp(self) -> None:
        """Set up valid theme data for testing."""
        self.valid_theme_data = {
            "theme": {
                "name": "standard",
                "boardImage": "board.png",
                "pieceImages": {
                    "br": "br.png",
                    "bn": "bn.png",
                    "bb": "bb.png",
                    "bq": "bq.png",
                    "bk": "bk.png",
                    "bp": "bp.png",
                    "wr": "wr.png",
                    "wn": "wn.png",
                    "wb": "wb.png",
                    "wq": "wq.png",
                    "wk": "wk.png",
                    "wp": "wp.png"
                },
                "squares": {
                    "a1": {"x": 0, "y": 0},
                    "b1": {"x": 100, "y": 0},
                    "c1": {"x": 200, "y": 0},
                    "h8": {"x": 700, "y": 700}
                }
            }
        }
        self.valid_theme_json = (
            '{"theme": {'
            '"name": "standard", '
            '"boardImage": "board.png", '
            '"pieceImages": {"br": "br.png", "bn": "bn.png", "bb": "bb.png", '
            '"bq": "bq.png", "bk": "bk.png", "bp": "bp.png", '
            '"wr": "wr.png", "wn": "wn.png", "wb": "wb.png", '
            '"wq": "wq.png", "wk": "wk.png", "wp": "wp.png"}, '
            '"squares": {"a1": {"x": 0, "y": 0}, "b1": {"x": 100, "y": 0}, '
            '"c1": {"x": 200, "y": 0}, "h8": {"x": 700, "y": 700}}}}'
        )

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_from_file_valid(self, mock_file):
        """Test that Theme can be created from a valid JSON file."""
        # Mock file contains valid JSON data
        mock_file.return_value.read.return_value = self.valid_theme_json

        theme = Theme.from_file("mock_theme.json")
        self.assertEqual(theme.name, "standard")
        self.assertEqual(theme.board_image, "board.png")
        self.assertIn("br", theme.piece_images)
        self.assertEqual(theme.squares["a1"], {"x": 0, "y": 0})

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_from_file_invalid(self, mock_file):
        """Test that an invalid JSON file raises an error."""
        with self.assertRaises(KeyError):
            Theme.from_file("mock_invalid_theme.json")

    def test_validate_theme(self):
        """Test the validate_theme method with valid and invalid data."""
        valid_data = self.valid_theme_data["theme"]
        invalid_data = {"invalid_key": "invalid_value"}

        self.assertTrue(Theme.validate_theme(valid_data))
        self.assertFalse(Theme.validate_theme(invalid_data))

    def test_repr(self):
        """Test the __repr__ method."""
        theme = Theme(
            name="example",
            board_image="example_board.png",
            piece_images={},
            squares={}
        )
        self.assertEqual(repr(theme), "Theme(name='example', board_image='example_board.png')")


if __name__ == "__main__":
    unittest.main()
