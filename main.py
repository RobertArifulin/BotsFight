import importlib
import os
import inspect
import importlib.util
from game import Game, Status
from tournament import Tournament
import tkinter as tk
from tkinter import filedialog as fd
from interface import StartWindow
from constants import *


def games_import() -> dict:
    """Возвращает список классов всех игр из папки all_games."""

    games = {}
    path = 'games'
    new_modules = [file for file in os.listdir(path) if file[-3:] == '.py']
    for module in new_modules:
        spec = importlib.util.spec_from_file_location(module[:-3], f'{path}\{module}')
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        for member in inspect.getmembers(foo, inspect.isclass):
            if Game.__subclasscheck__(member[1]) and member[0] != 'Game':
                games.update({f"{module}-{member[1].__name__}": member[1]})
    return games


def test_tournament():
    bots_paths = []
    path = fd.askopenfilenames(filetypes=[('*', '.py'), ('*', '.exe'), ('*', '.pyw')])
    bots_paths.extend(path)
    print(bots_paths)

    games = games_import()
    game_names = list(games.keys())
    print(games, game_names)
    game_name = game_names[0]
    game = games[game_name]()
    tournament = Tournament(game)

    tournament.register_bot(bots_paths[0])
    tournament.register_bot(bots_paths[1])

    tournament.create_standings()
    results = tournament.tournament()
    print(results[0])


def main():
    games = games_import()
    game_names = list(games.keys())
    start_window = StartWindow(games)


if __name__ == '__main__':
    main()
