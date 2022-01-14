import copy
from game import Game, Status
from bot import Bot
from PIL import Image
from constants import ERROR


class Tournament:
    """ Класс Tournament является связующим звеном между игрой и ботами.
        Он регестрирует новых ботов и проводит поединки каждого бота с каждым в выбранной игре.
        Во время игр он выводит картинку поля, которую ему дает игра.
        После всех матчей выводит результаты турнира.

        Attributes
        ----------
        game: Game
            Игра, в которую играют боты.
        bots: list[Bot]
            Боты, которые будут участвовать в турнире.
        standings: list[tuple[Bot, Bot]]
            Турнирная таблица - просто попарный список ботов, где каждый сыгрет с каждым.
        tournament_results: list
            Результаты турнира.
        game_number: int
            Количество партий между 2 ботами.


        Methods
        -------
        register_bot(path)
            Добовляет бота в bots по пути его path.
            Если файл бота не найден, то вызывает ошибку.

        create_standings()
            Создает список пар ботов, по которуму пройдут игры.

        game_init()
            Вызывает функцию game_init() у game.

        play(pair)
            Проводит игру между двумя ботами.
            Отрисовывает поле вызовом display_game().
            Возвращает результат битвы.


        tournament()
            Для каждой пары (pair) из standings проводит play().
            Результат добовляет в tournament_results.
            После проведения всех игр возвращает результаты турнира - tournament_results.

        create_text()
            Создает описание происходящих в партии событий.
    """
    game: Game
    bots: list[Bot]
    standings: list[tuple[Bot, Bot]]
    tournament_results: list
    pair: tuple[Bot, Bot]
    game_number: int

    def __init__(self, game: Game, game_number: int):
        self.first_move = 2
        self.game = game
        self.bots = []
        self.standings = []
        self.tournament_results = []
        self.game_number = game_number

    def register_bot(self, path: str):
        """ Добовляет бота в bots по пути его path.
            Если файл бота не найден, то вызывает ошибку."""

        self.bots.append(Bot(path))

    def create_standings(self):
        """ Создает список пар ботов, по которуму пройдут игры."""

        for i, bot1 in enumerate(self.bots[:-1]):
            for j, bot2 in enumerate(self.bots[i + 1:]):
                for n in range(self.game_number):
                    if not n % 2:
                        self.standings.append((copy.copy(bot1), copy.copy(bot2)))
                    else:
                        self.standings.append((copy.copy(bot2), copy.copy(bot1)))

    def game_init(self) -> str:
        """ Вызывает функцию game_init() у game."""

        return self.game.game_init()

    def turn(self, pair: tuple[Bot, Bot], status: Status) -> Status:
        """

        """
        bot1 = pair[0]
        bot2 = pair[1]

        if status not in [Status.bot1_won, Status.bot2_won, Status.draw]:
            if status == Status.bot1_next:
                bot_turn = bot1.request_bot(self.game.get_board_string())
                if bot_turn == ERROR:
                    status = Status.bot2_won
                else:
                    status = self.game.bot_made_turn(bot_turn)
                return status

            elif status == Status.bot2_next:
                bot_turn = bot2.request_bot(self.game.get_board_string())
                if bot_turn == ERROR:
                    status = Status.bot1_won
                else:
                    status = self.game.bot_made_turn(bot_turn)
                return status
        return status

    def tournament(self) -> tuple[Image, str, str]:
        """ Для каждой пары (pair) из standings проводит play().
            Результат добовляет в tournament_results.
            После проведения всех игр возвращает результаты турнира - tournament_results.
        """
        if len(self.tournament_results) == len(self.standings):
            image = self.game.draw_board_image()
            return image, '', ''

        pair = self.standings[len(self.tournament_results)]

        if self.first_move:
            image = self.game.draw_board_image()
            res = self.create_text(Status.bot1_next, pair)
            self.first_move -= 1
            return image, res[0], res[1]

        try:
            res = self.turn(pair, self.game.get_status())
        except:
            res = self.game.get_status()
            if res == Status.bot1_next:
                res = Status.bot2_won0
            elif res == Status.bot2_next:
                res = Status.bot1_won

        image = self.game.draw_board_image()
        if res == Status.bot1_won:
            self.tournament_results.append(f"{pair[0].name} defeated {pair[1].name}")
            self.game_init()
            self.first_move = 1
        elif res == Status.bot2_won:
            self.tournament_results.append(f"{pair[1].name} defeated {pair[0].name}")
            self.game_init()
            self.first_move = 1
        elif res == Status.draw:
            self.tournament_results.append(f"{pair[0].name} draw {pair[1].name}")
            self.game_init()
            self.first_move = 1
        res = self.create_text(res, pair)
        return image, res[0], res[1]

    def create_text(self, res: Status, pair: tuple[Bot, Bot]) -> tuple[str, str]:
        """
        Создает описание происходящих в партии событий.
        """
        title = f"{pair[0].name}\nvs\n{pair[1].name}"
        if res == Status.bot1_won:
            status = f"Победа\n{pair[0].name}!"
        elif res == Status.bot2_won:
            status = f"Победа\n{pair[1].name}!"
        elif res == Status.draw:
            status = f"Ничья между\n{pair[0].name} и\n{pair[1].name}!"
        elif res == Status.bot1_next:
            status = f"Ход\n{pair[0].name}"
        else:
            status = f"Ход\n{pair[1].name}"
        return title, status
