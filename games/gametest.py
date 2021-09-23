import importlib.util
import inspect
from game import Game


class GameTest(Game):

    def __init__(self):
        super().__init__()
        self.board = [[0] * 5 for _ in range(10)]

    def get_board_string(self) -> str:
        return f'{len(self.board)} {len(self.board[0])}'
