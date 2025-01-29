import unittest
import os
import tempfile
from unittest import mock

from image_processing.pgn_to_image import PGNToImage
from themes.theme import Theme

class TestPGNToImage(unittest.TestCase):
    def setUp(self):
        """Setup the TMP folder and the default theme"""
        self.output_dir = tempfile.TemporaryDirectory()

        self.theme = Theme.from_file("themes/assets/standard/config.json")
        self.generator = PGNToImage(self.theme)


    def tearDown(self):
        """Delete the TMP folder"""
        self.output_dir.cleanup()

    # render_from_pgn_string OK
    def test_render_from_pgn_string(self):
        """Test a standard rendering from a PGN string."""
        pgn_string = "1. e4 e5 2. Nf3 *"
        self.generator.render_from_pgn_string(pgn_string, self.output_dir.name, final_position_only=True)

        path = self.output_dir.name + "/final_position.png"
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    # render_from_pgn_string WRONG STRING ERROR
    def test_render_from_pgn_string_error(self):
        """Test a standard rendering from an empty PGN string."""
        pgn_string = ""
        with self.assertRaises(ValueError):
            self.generator.render_from_pgn_string(pgn_string, self.output_dir.name, final_position_only=True)

    # render_from_pgn_file OK
    def test_render_from_pgn_file(self):
        """Test rendering from a valid PGN file using decorators."""
        
        with tempfile.NamedTemporaryFile(suffix=".pgn", mode='w', delete=False) as tmp_pgn:
            tmp_pgn.write("1. e4 e5 2. Nf3 *")
            tmp_pgn_path = tmp_pgn.name
        
        self.generator.render_from_pgn_file(tmp_pgn_path, self.output_dir.name, final_position_only=True)

        path = os.path.join(self.output_dir.name, "final_position.png")
        self.assertTrue(os.path.exists(path))  
        os.remove(path)

    # render_from_pgn_file file not exist
    def test_render_from_pgn_file_not_exist(self):
        """Test rendering from a non-existing PGN file."""
        with self.assertRaises(FileNotFoundError):
            self.generator.render_from_pgn_file("non_existing.pgn", self.output_dir.name, final_position_only=True)

    # render_from_pgn_file file is not a PGN
    def test_render_from_pgn_file_invalid(self):
        """Test rendering from an invalid PGN file."""
        with tempfile.NamedTemporaryFile(suffix=".pgn", mode='w', delete=False) as tmp_pgn:
            tmp_pgn.write("")
            tmp_pgn_path = tmp_pgn.name

        with self.assertRaises(ValueError):
            self.generator.render_from_pgn_file(tmp_pgn_path, self.output_dir.name, final_position_only=True)
        os.remove(tmp_pgn_path)

    # render_from_pgn_folder OK
    @mock.patch("os.listdir", return_value=["game1.pgn", "game2.pgn"])
    @mock.patch("image_processing.pgn_to_image.PGNToImage.render_from_pgn_file")
    def test_render_from_pgn_folder(self, mock_render_from_pgn_file, mock_listdir):
        """Test rendering from a folder containing PGN files."""
        print("START")
        folder_path = tempfile.mkdtemp()
        self.generator.render_from_pgn_folder(folder_path, self.output_dir.name, final_position_only=True)
        self.assertEqual(mock_render_from_pgn_file.call_count, 2)

    # render_from_pgn_folder folder not exist
    def test_render_from_pgn_folder_not_exist(self):
        """Test rendering from a non-existing folder."""
        with self.assertRaises(FileNotFoundError):
            self.generator.render_from_pgn_folder("non_existing_folder", self.output_dir.name, final_position_only=True)

    # render_from_pgn_folder folder empty
    @mock.patch("os.listdir", return_value=[])
    def test_render_from_pgn_folder_empty(self, mock_listdir):
        """Test rendering from an empty folder."""
        folder_path = tempfile.mkdtemp()
        self.generator.render_from_pgn_folder(folder_path, self.output_dir.name, final_position_only=True)
        mock_listdir.assert_called_once_with(folder_path)

if __name__ == "__main__":
    unittest.main()
