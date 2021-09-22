from enum import Enum


class Game:
    """ Класс Game - виртуальный класс, дающий базовый интерфейс, через который игры будут взаимодействовать с
        платформой.


        Attributes
        ----------
        board_string : str
            состояние игрового поля
        status : Status
            статус игры


        Methods
        -------
        get_board_string()
            Возвращает состояние поля.

        get_status()
            Возвращает статус игры (Первый ходит, Второй победил и т.д.).

        bot_made_turn()
            На основе хода бота изменяет состояние поля и возвращает статус игры.

        draw_board_image()
            Отрисовывает игру.

    """

    def __init__(self):
        self.board_string = None
        self.status = None

    def get_board_string(self) -> str:
        """ Возвращает состояние поля."""

        return self.board_string

    def get_status(self) -> int:
        """ Возвращает статус игры (Первый ходит, Второй победил и т.д.)."""

        return self.status

    def bot_made_turn(self) -> int:
        """ На основе хода бота изменяет состояние поля и возвращает статус игры."""

        return self.status

    def draw_board_image(self) -> None:
        """ Отрисовывает игру."""

        return None


class Status(Enum):
    """ Класс Status - enum класс, который является набором статусов игры с уникальными значениями."""

    bot1_next = 1
    bot2_next = 2
    bot1_won = 3
    bot2_won = 4
    draw = 5
