import unittest
from unittest.mock import MagicMock, patch
from themes.theme import Theme
from image_processing.pgn_to_image import PGNToImage
import io


class TestPGNToImage(unittest.TestCase):
    def setUp(self):
        """Set up a mock theme and PGNToImage instance."""
        self.mock_theme = MagicMock(spec=Theme)
        self.mock_theme.board_image = "mock_board.png"
        self.mock_theme.piece_images = {
            "wp": "mock_wp.png",
            "bp": "mock_bp.png",
        }
        self.mock_theme.squares = {
            "a1": {"x": 50, "y": 50},
            "h8": {"x": 450, "y": 450},
        }
        self.generator = PGNToImage(self.mock_theme)


    @patch("image_processing.pgn_to_image.Image.open")
    def test_render_from_pgn_string_final_position(self, mock_open):
        """Test rendering the final position from a PGN string."""

        pgn_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"
        output_dir = "mock_output"
        mock_board_image = MagicMock()
        mock_open.return_value = mock_board_image

        with patch.object(self.generator, "_render_from_fen", return_value=None) as mock_render_from_fen:
            self.generator.render_from_pgn_string(pgn_string, output_dir, final_position_only=True)
            mock_render_from_fen.assert_called_once()  # Ensure only the final position is rendered

    @patch("image_processing.pgn_to_image.Image.open")
    def test_render_from_pgn_string_all_moves(self, mock_open):
        """Test rendering all moves from a PGN string."""
        pgn_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"
        output_dir = "mock_output"
        mock_board_image = MagicMock()
        mock_open.return_value = mock_board_image

        with patch.object(self.generator, "_render_from_fen", return_value=None) as mock_render_from_fen:
            self.generator.render_from_pgn_string(pgn_string, output_dir, final_position_only=False)

            # Ensure _render_from_fen is called for each move
            self.assertEqual(mock_render_from_fen.call_count, 6)  # 6 moves total

    @patch("os.listdir")
    @patch("image_processing.pgn_to_image.PGNToImage.render_from_pgn_file")
    def test_render_from_pgn_folder(self, mock_render_from_pgn_file, mock_listdir):
        """Test rendering images from all PGN files in a folder."""
        mock_listdir.return_value = ["game1.pgn", "game2.pgn", "not_a_pgn.txt"]
        folder_path = "mock_folder"
        output_dir = "mock_output"

        self.generator.render_from_pgn_folder(folder_path, output_dir, final_position_only=True)

        # Ensure all PGN files are processed
        mock_render_from_pgn_file.assert_any_call("mock_folder\game1.pgn", output_dir, True)
        mock_render_from_pgn_file.assert_any_call("mock_folder\game2.pgn", output_dir, True)
        self.assertEqual(mock_render_from_pgn_file.call_count, 2)

    @patch("builtins.open", new_callable=MagicMock)
    @patch("image_processing.pgn_to_image.PGNToImage._process_game")
    def test_render_from_pgn_file(self, mock_process_game, mock_open):
        """Test rendering images from a single PGN file."""

        pgn_file = "mock_game.pgn"
        output_dir = "mock_output"
        mock_open.return_value.__enter__.return_value = io.StringIO("1. e4 e5 2. Nf3 Nc6 *")

        self.generator.render_from_pgn_file(pgn_file, output_dir, final_position_only=True)

        # Ensure the file is opened and processed
        mock_open.assert_called_once_with(pgn_file, "r", encoding="utf-8")
        mock_process_game.assert_called_once()

    @patch("image_processing.pgn_to_image.PGNToImage._render_from_fen")
    def test_process_game_final_position(self, mock_render_from_fen):
        """Test processing a single game and rendering only the final position."""
        mock_game = MagicMock()
        mock_game.mainline_moves.return_value = [
            "e4", "e5", "Nf3", "Nc6", "Bb5", "a6"
        ]
        output_dir = "mock_output"

        self.generator._process_game(mock_game, output_dir, final_position_only=True)

        # Ensure only one call to _render_from_fen (final position)
        mock_render_from_fen.assert_called_once()

    @patch("image_processing.pgn_to_image.PGNToImage._render_from_fen")
    def test_process_game_all_moves(self, mock_render_from_fen):
        """Test processing a single game and rendering all moves."""
        mock_game = MagicMock()
        mock_game.mainline_moves.return_value = [
            "e4", "e5", "Nf3", "Nc6", "Bb5", "a6"
        ]
        output_dir = "mock_output"

        self.generator._process_game(mock_game, output_dir, final_position_only=False)

        # Ensure _render_from_fen is called for each move
        self.assertEqual(mock_render_from_fen.call_count, 6)  # 6 moves total

if __name__ == "__main__":
    unittest.main()
