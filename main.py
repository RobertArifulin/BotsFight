import importlib
import os
import inspect
import importlib.util
from game import Game
from interface import StartWindow


def games_import() -> dict:
    """Возвращает список классов всех игр из папки all_games."""

    games = {}
    path = 'games'
    new_modules = [file for file in os.listdir(path) if file[-3:] == '.py']
    for module in new_modules:
        spec = importlib.util.spec_from_file_location(module[:-3], fr'{path}\{module}')
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        for member in inspect.getmembers(foo, inspect.isclass):
            if Game.__subclasscheck__(member[1]) and member[0] != 'Game':
                games.update({f"{module}-{member[1].__name__}": member[1]})
    return games


def main():
    games = games_import()
    try:
        start_window = StartWindow(games)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
