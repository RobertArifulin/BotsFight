from enum import Enum
from PIL import Image


class Status(Enum):
    """ Класс Status - enum класс, который является набором статусов игры с уникальными значениями."""

    bot1_next = 1
    bot2_next = 2
    bot1_won = 3
    bot2_won = 4
    draw = 5


class Game:
    """ Класс Game - виртуальный класс, дающий базовый интерфейс, через который игры будут взаимодействовать с
        платформой.


        Attributes
        ----------
        board_string : str
            Состояние игрового поля.
        status : Status
            Статус игры.


        Methods
        -------
        game_init()
            Возвращает состояние поля.
            Происходит создание новой игры, поля для нее и т.д.

        get_board_string()
            Возвращает состояние поля.

        get_status()
            Возвращает статус игры (Первый ходит, Второй победил и т.д.).

        bot_made_turn(turn)
            На основе хода (turn) бота изменяет состояние поля и возвращает статус игры.

        draw_board_image()
            Отрисовывает игру.

    """

    status: Status
    board_string: str
    name: str
    description: str
    author: str
    turn: str

    def __init__(self):
        self.board_string = ""
        self.status = Status.bot1_next

    def game_init(self) -> str:
        """ Возвращает состояние поля.
            Происходит создание новой игры: начальные условия, поля для нее и т.д."""

        return self.board_string

    def get_board_string(self) -> str:
        """ Возвращает состояние поля."""

        return self.board_string

    def get_status(self) -> Status:
        """ Возвращает статус игры (Первый ходит, Второй победил и т.д.)."""

        return self.status

    def bot_made_turn(self, turn: str) -> Status:
        """ На основе хода бота изменяет состояние поля и возвращает статус игры."""

        return self.status

    def draw_board_image(self) -> Image:
        """ Отрисовывает игру."""

        return Image
