from game import Game, Status
from PIL import Image, ImageDraw, ImageFont


class GameTest(Game):

    def __init__(self):
        super().__init__()
        self.board = None

    def game_init(self) -> str:
        self.board = [[0] * 5 for _ in range(5)]
        self.status = Status.bot1_next
        return self.get_board_string()

    def get_board_string(self) -> str:
        self.board_string = ''
        for line in self.board:
            self.board_string += ' '.join([str(i) for i in line]) + '\n'
        return self.board_string[:-1]

    def bot_made_turn(self, turn: str) -> Status:
        MAX = 20
        for i in range(len(self.board)):
            y, number = map(int, turn.split())
            self.board[y - 1][i] = number

        if sum([self.board[i][0] for i in range(5)]) >= MAX > sum([self.board[i][1] for i in range(5)]):
            self.status = Status.bot1_won
            return self.status

        elif sum([self.board[i][1] for i in range(5)]) >= MAX:
            self.status = Status.bot2_won
            return self.status

        elif sum([self.board[i][1] for i in range(5)]) == sum([self.board[i][0] for i in range(5)]) >= MAX:
            self.status = Status.draw
            return self.status

        elif self.status == Status.bot1_next:
            self.status = Status.bot2_next
            return self.status

        else:
            self.status = Status.bot1_next
            return self.status

    def draw_board_image(self) -> Image:
        image = Image.new('RGB', (400, 300), color=(255, 255, 255))
        canvas = ImageDraw.Draw(image)
        text = self.get_board_string()
        font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=30)
        canvas.text((10, 10), text, fill='#000000', font=font)
        return image
