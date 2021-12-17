from game import Game, Status
from PIL import Image, ImageDraw, ImageFont
from constants import *
import random


class Matches(Game):

    def __init__(self):
        super().__init__()
        self.matches = 0
        self.allowed_takes = []
        self.start_count = 0
        self.prev_count = 0
        self.status = Status.bot1_next

    def game_init(self) -> str:
        self.allowed_takes = [i for i in range(1, random.randint(3, 5))]
        self.matches = random.randint(self.allowed_takes[-1] * 2, 11)
        self.start_count = self.matches
        self.prev_count = self.matches
        return f"{self.matches} {self.allowed_takes[-1]}"

    def get_board_string(self) -> str:
        return f"{self.matches} {self.allowed_takes[-1]}"

    def bot_made_turn(self, turn: str) -> Status:
        try:
            take = int(turn)
        except:  # Проверки на корректность хода
            if self.status == Status.bot1_next:
                return Status.bot2_won
            else:
                return Status.bot1_won
        if take not in self.allowed_takes:
            if self.status == Status.bot1_next:
                return Status.bot2_won
            else:
                return Status.bot1_won

        self.prev_count = self.matches
        self.matches = max(self.matches - take, 0)

        if self.matches == 0:
            if self.status == Status.bot1_next:
                self.status = Status.bot1_won
            elif self.status == Status.bot2_next:
                self.status = Status.bot2_won
        if self.status == Status.bot1_next:
            self.status = Status.bot2_next
        elif self.status == Status.bot2_next:
            self.status = Status.bot1_next
        return self.status

    def draw_board_image(self) -> Image:
        image = Image.new('RGB', (420, 420), color=(255, 255, 255))
        match = Image.open(r"C:\Users\rober\PycharmProjects\BotsFight\images\match.png")
        match = match.resize((40, 80))
        delta = 420 // self.start_count
        for i in range(self.matches):
            image.paste(match, (i * delta + 10, 10))
        canvas = ImageDraw.Draw(image)
        font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=30)
        if self.status == Status.bot1_next:
            canvas.text((10, 90), f"Бот 1 взял {self.prev_count - self.matches} спичек.", fill='#000000', font=font)
        if self.status == Status.bot2_next:
            canvas.text((10, 90), f"Бот 2 взял {self.prev_count - self.matches} спичек.", fill='#000000', font=font)
        if self.status == Status.bot1_won:
            canvas.text((10, 90), f"Бот 1 победил взяв {self.prev_count - self.matches} спичек.", fill='#000000', font=font)
        if self.status == Status.bot2_won:
            canvas.text((10, 90), f"Бот 2 победил взяв {self.prev_count - self.matches} спичек.", fill='#000000', font=font)
        return image
