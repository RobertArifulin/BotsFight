import importlib
import os
import inspect
import importlib.util
from bot import Bot
from game import Game, Status
from  tournament import Tournament


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


def main():
    games = games_import()
    print(games)
    game = games[0]()
    tournament = Tournament(game)
    tournament.register_bot(r'C:\Users\rober\PycharmProjects\BotsFight\bots\bottest1.py')
    tournament.register_bot(r'C:\Users\rober\PycharmProjects\BotsFight\bots\bottest2.py')
    tournament.create_standings()
    results = tournament.tournament()
    print(results[0])


if __name__ == '__main__':
    main()
