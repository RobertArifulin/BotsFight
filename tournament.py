from game import Game, Status
from bot import Bot
from PIL import Image


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

        display_game()
            Выводит картинку игрового поля, которую предоставила игра.


    """
    game: Game
    bots: list[Bot]
    standings: list[tuple[Bot, Bot]]
    tournament_results: list
    pair: tuple[Bot, Bot]

    def __init__(self, game: Game):
        self.game = game
        self.bots = []
        self.standings = []
        self.tournament_results = []

    def register_bot(self, path: str):
        """ Добовляет бота в bots по пути его path.
            Если файл бота не найден, то вызывает ошибку."""

        self.bots.append(Bot(path))

    def create_standings(self):
        """ Создает список пар ботов, по которуму пройдут игры."""

        for i, bot1 in enumerate(self.bots[:-1]):
            for j, bot2 in enumerate(self.bots[i + 1:]):
                self.standings.append((bot1, bot2))

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
                status = self.game.bot_made_turn(bot_turn)
                return status

            elif status == Status.bot2_next:
                bot_turn = bot2.request_bot(self.game.get_board_string())
                status = self.game.bot_made_turn(bot_turn)
                return status
        return status

    def tournament(self):
        """ Для каждой пары (pair) из standings проводит play().
            Результат добовляет в tournament_results.
            После проведения всех игр возвращает результаты турнира - tournament_results.
        """
        if len(self.tournament_results) == len(self.standings):
            return None, False
        pair = self.standings[len(self.tournament_results)]
        res = self.turn(pair, self.game.get_status())
        if res == Status.bot1_won:
            self.tournament_results.append(f"{pair[0].name} won")
            self.game.game_init()
        elif res == Status.bot2_won:
            self.tournament_results.append(f"{pair[1].name} won")
            self.game.game_init()
        elif res == Status.draw:
            self.tournament_results.append(f"draw between {pair[0].name} and {pair[1].name}")
            self.game.game_init()
        image = self.game.draw_board_image()
        return image, res
