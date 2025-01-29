from typing import Optional
import io

from chess import pgn

def pgn_to_fen(pgn_string: str) -> Optional[str]:
    """
    Extract the final position FEN from a PGN string.

    Args:
        pgn_string (str): The PGN string containing the chess game.

    Returns:
        str: The FEN representation of the final position.
    """
    game = pgn.read_game(io.StringIO(pgn_string))

    if game is None: 
        return None  
    
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)

    return board.fen()
