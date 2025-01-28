import unittest
from unittest.mock import patch, MagicMock
from themes.theme import Theme
from image_processing.fen_to_image import FENToImage


class TestFENToImage(unittest.TestCase):
    """Unit tests for the FENToImage class."""

    def setUp(self) -> None:
        """Set up mock data and theme for testing."""
        self.mock_theme = Theme(
            name="standard",
            board_image="board.png",
            piece_images={
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
                "wp": "wp.png",
            },
            squares={ "a1": { "x": 0, "y": 0 }, "b1": { "x": 100, "y": 0 }, "c1": { "x": 200, "y": 0 }, "d1": { "x": 300, "y": 0 },
                "e1": { "x": 400, "y": 0 },"f1": { "x": 500, "y": 0 },"g1": { "x": 600, "y": 0 },"h1": { "x": 700, "y": 0 },
                "a2": { "x": 0, "y": 100 },"b2": { "x": 100, "y": 100 }, "c2": { "x": 200, "y": 100 }, "d2": { "x": 300, "y": 100 },
                "e2": { "x": 400, "y": 100 }, "f2": { "x": 500, "y": 100 }, "g2": { "x": 600, "y": 100 }, "h2": { "x": 700, "y": 100 },
                "a3": { "x": 0, "y": 200 }, "b3": { "x": 100, "y": 200 }, "c3": { "x": 200, "y": 200 }, "d3": { "x": 300, "y": 200 },
                "e3": { "x": 400, "y": 200 }, "f3": { "x": 500, "y": 200 }, "g3": { "x": 600, "y": 200 }, "h3": { "x": 700, "y": 200 },
                "a4": { "x": 0, "y": 300 }, "b4": { "x": 100, "y": 300 }, "c4": { "x": 200, "y": 300 }, "d4": { "x": 300, "y": 300 },
                "e4": { "x": 400, "y": 300 }, "f4": { "x": 500, "y": 300 }, "g4": { "x": 600, "y": 300 }, "h4": { "x": 700, "y": 300 },
                "a5": { "x": 0, "y": 400 }, "b5": { "x": 100, "y": 400 }, "c5": { "x": 200, "y": 400 }, "d5": { "x": 300, "y": 400 },
                "e5": { "x": 400, "y": 400 }, "f5": { "x": 500, "y": 400 }, "g5": { "x": 600, "y": 400 }, "h5": { "x": 700, "y": 400 },
                "a6": { "x": 0, "y": 500 }, "b6": { "x": 100, "y": 500 }, "c6": { "x": 200, "y": 500 }, "d6": { "x": 300, "y": 500 },
                "e6": { "x": 400, "y": 500 }, "f6": { "x": 500, "y": 500 }, "g6": { "x": 600, "y": 500 }, "h6": { "x": 700, "y": 500 },
                "a7": { "x": 0, "y": 600 }, "b7": { "x": 100, "y": 600 }, "c7": { "x": 200, "y": 600 }, "d7": { "x": 300, "y": 600 },
                "e7": { "x": 400, "y": 600 }, "f7": { "x": 500, "y": 600 }, "g7": { "x": 600, "y": 600 }, "h7": { "x": 700, "y": 600 },
                "a8": { "x": 0, "y": 700 },"b8": { "x": 100, "y": 700 },"c8": { "x": 200, "y": 700 },"d8": { "x": 300, "y": 700 },
                "e8": { "x": 400, "y": 700 },"f8": { "x": 500, "y": 700 },"g8": { "x": 600, "y": 700 },"h8": { "x": 700, "y": 700 },
            })
        self.fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.test_output = "testoutput.png"
        

    @patch("PIL.Image.open")
    def test_render_from_fen(self, mock_open):
        """Test rendering a chessboard from a FEN string."""
        self.renderer = FENToImage(self.mock_theme)
        self.renderer.render_from_fen(self.fen_string, self.test_output)

        mock_open.assert_any_call("board.png")
        mock_open.assert_any_call("br.png")
        mock_open.assert_any_call("wr.png") 

    @patch("builtins.open", new_callable=MagicMock)
    @patch("PIL.Image.open")
    def test_render_from_fen_file(self, mock_open, mock_file_open):
        """Test rendering a chessboard from a FEN file."""

        # Mocks
        mock_file = MagicMock()
        mock_file.read.return_value = self.fen_string
        mock_file_open.return_value.__enter__.return_value = mock_file

        # Rendering
        fen_renderer = FENToImage(self.mock_theme)
        fen_renderer.render_from_fen_file("input.fen", self.test_output)

        mock_open.assert_any_call("board.png")
        mock_open.assert_any_call("br.png")  # Black rook
        mock_open.assert_any_call("wr.png") 


    def test_fen_to_positions(self):
        """Test conversion of a FEN string to piece positions."""
        expected_positions = {
            "a1": "wr",
            "b1": "wn",
            "c1": "wb",
            "d1": "wq",
            "e1": "wk",
            "f1": "wb",
            "g1": "wn",
            "h1": "wr",
            "a2": "wp",
            "b2": "wp",
            "c2": "wp",
            "d2": "wp",
            "e2": "wp",
            "f2": "wp",
            "g2": "wp",
            "h2": "wp",
            "a8": "br",
            "b8": "bn",
            "c8": "bb",
            "d8": "bq",
            "e8": "bk",
            "f8": "bb",
            "g8": "bn",
            "h8": "br",
            "a7": "bp",
            "b7": "bp",
            "c7": "bp",
            "d7": "bp",
            "e7": "bp",
            "f7": "bp",
            "g7": "bp",
            "h7": "bp",
        }

        positions = FENToImage._fen_to_positions(self.fen_string)
        self.assertEqual(positions, expected_positions)


if __name__ == "__main__":
    unittest.main()
