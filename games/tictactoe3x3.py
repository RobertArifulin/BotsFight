from game import Game, Status
from PIL import Image, ImageDraw, ImageFont
from constants import *


class TicTacToe3x3(Game):

    def __init__(self):
        super().__init__()
        self.board = None
        self.win_cords = []

    def game_init(self) -> str:
        self.win_cords = []
        self.board = [[0] * 3 for _ in range(3)]
        self.status = Status.bot1_next
        return self.get_board_string()

    def get_board_string(self) -> str:
        if self.status == Status.bot1_next:
            self.board_string = 'x'
        if self.status == Status.bot2_next:
            self.board_string = '0'
        for line in self.board:
            self.board_string += ' '.join([str(i) for i in line]) + '\n'
        return self.board_string[:-1]

    def bot_made_turn(self, turn: str) -> Status:
        x, y = map(int, turn.split())
        if self.status == Status.bot1_next:
            self.board[y - 1][x - 1] = 1
        elif self.status == Status.bot2_next:
            self.board[y - 1][x - 1] = 2

        return self.change_status()

    def change_status(self):
        columns = [[self.board[j][i] for j in range(3)] for i in range(3)]
        diagonals = [[self.board[i][i] for i in range(3)], [self.board[i][2 - i] for i in range(3)]]
        for i in range(3):
            if all(list(map(lambda x: x == 1, self.board[i]))):
                self.status = Status.bot1_won
                self.win_cords = [(0, i * 140 + 70), (3 * 140, i * 140 + 70)]
                return self.status
            if all(list(map(lambda x: x == 2, self.board[i]))):
                self.status = Status.bot2_won
                self.win_cords = [(0, i * 140 + 70), (3 * 140, i * 140 + 70)]
                return self.status
            if all(list(map(lambda x: x == 1, columns[i]))):
                self.status = Status.bot1_won
                self.win_cords = [(i * 140 + 70, 0), (i * 140 + 70, 3 * 140)]
                return self.status
            if all(list(map(lambda x: x == 2, columns[i]))):
                self.status = Status.bot2_won
                self.win_cords = [(i * 140 + 70, 0), (i * 140 + 70, 3 * 140)]
                return self.status
            if all(list(map(lambda x: x == 1, diagonals[i % 2]))):
                self.status = Status.bot1_won
                if i % 2:
                    self.win_cords = [(3 * 140, 0), (0, 3 * 140)]
                else:
                    self.win_cords = [(0, 0), (3 * 140, 3 * 140)]
                return self.status
            if all(list(map(lambda x: x == 2, diagonals[i % 2]))):
                self.status = Status.bot2_won
                if i % 2:
                    self.win_cords = [(3 * 140, 0), (0, 3 * 140)]
                else:
                    self.win_cords = [(0, 0), (3 * 140, 3 * 140)]
                return self.status
        if all(list(map(lambda x: all(x), self.board))):
            self.status = Status.draw
            return self.status
        if self.status == Status.bot1_next:
            self.status = Status.bot2_next
            return self.status
        if self.status == Status.bot2_next:
            self.status = Status.bot1_next
            return self.status

    def draw_board_image(self) -> Image:
        image = Image.new('RGB', (420, 420), color=(255, 255, 255))
        canvas = ImageDraw.Draw(image)
        for i in range(1, 3):
            canvas.line([140 * i, 0, 140 * i, 420], width=3, fill=BLACK)
            canvas.line([0, 140 * i, 420, 140 * i], width=3, fill=BLACK)
        for i in range(3):
            for j in range(3):
                delta_x = 140 * i
                delta_y = 140 * j
                if self.board[j][i] == 2:
                    canvas.ellipse([5 + delta_x, 5 + delta_y, 135 + delta_x, 135 + delta_y], width=3, fill=WHITE, outline=BLACK)
                elif self.board[j][i] == 1:
                    canvas.line([5 + delta_x, 5 + delta_y, 135 + delta_x, 135 + delta_y], width=3, fill=BLACK)
                    canvas.line([5 + delta_x, 135 + delta_y, 135 + delta_x, 5 + delta_y], width=3, fill=BLACK)
        if self.win_cords:
            x1, y1 = self.win_cords[0]
            x2, y2 = self.win_cords[1]
            canvas.line([x1, y1, x2, y2], width=4, fill=RED)
        return image

