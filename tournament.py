from game import Game, Status
from bot import Bot


class Tournament:
    """ Класс Tournament является связующим звеном между игрой и ботами.
        Он регестрирует новых ботов и проводит поединки каждого бота с каждым в выбранной игре.
        Во время игр он выводит картинку поля, которую ему дает игра.
        После всех матчей выводит результаты турнира.

        Attributes
        ----------
        game: Game
            игра, в которую играют боты
        bots: list[Bot]
            боты, которые будут участвовать в турнире
        standings: list[tuple[Bot, Bot]]
            турнирная таблица - просто попарный список ботов, где каждый сыгрет с каждым
        tournament_results: list
            результаты турнира



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

    def play(self, pair: tuple[Bot, Bot]) -> Status:
        """ Проводит игру между двумя ботами.
            Отрисовывает поле вызовом display_game().
            Возвращает результат битвы."""

        bot1 = pair[0]
        bot2 = pair[1]
        status = self.game.get_status()

        print('start')
        print(self.game.get_board_string())
        print('-----------------------')

        while status not in [Status.bot1_won, Status.bot2_won, Status.draw]:
            if status == Status.bot1_next:
                bot_turn = bot1.request_bot(self.game.get_board_string())
                self.display_game(self.game.draw_board_image())
                status = self.game.bot_made_turn(bot_turn)

                print('after bot1')
                print(self.game.get_board_string())
                print('-----------------------')

            elif status == Status.bot2_next:
                bot_turn = bot2.request_bot(self.game.get_board_string())
                self.display_game(self.game.draw_board_image())
                status = self.game.bot_made_turn(bot_turn)

                print('after bot2')
                print(self.game.get_board_string())
                print('-----------------------')

        print('final')
        print(self.game.get_board_string())
        print('-----------------------')
        return status

    def tournament(self):
        """ Для каждой пары (pair) из standings проводит play().
            Результат добовляет в tournament_results.
            После проведения всех игр возвращает результаты турнира - tournament_results."""

        for pair in self.standings:
            res = self.play(pair)
            self.tournament_results.append(res)
        return self.tournament_results

    def display_game(self, image):
        """ Выводит картинку игрового поля, которую предоставила игра."""

        pass

