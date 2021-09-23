import importlib
import os
import inspect
import importlib.util
from bot import Bot
from game import Game


def games_import() -> list:
    """Возвращает список классов всех игр из папки games."""

    games = []
    path = 'games'
    new_modules = [file for file in os.listdir(path) if file[-3:] == '.py']
    for module in new_modules:
        spec = importlib.util.spec_from_file_location(module[:-3], f'{path}\{module}')
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        for member in inspect.getmembers(foo, inspect.isclass):
            if Game.__subclasscheck__(member[1]) and member[0] != 'Game':
                games.append(member[1])
    return games


games = games_import()
print(games)
game = games[0]()
game_cond = game.get_board_string()
bot1 = Bot(r'C:\Users\rober\PycharmProjects\BotsFight\bots\bottest1.py')
print(bot1.request_bot(game_cond))
