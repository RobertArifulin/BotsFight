import importlib
import os
import sys, inspect
import subprocess


def game_import():
    """Импортирует модули с играми в словарь."""

    all_games = {}
    new_games = [i[:-3] for i in os.listdir() if i[:4] == 'game']
    for game in new_games:
        all_games.update({game: importlib.import_module(game)})
    return all_games


def bot_import():
    new_bots = [i[:-3] for i in os.listdir() if i[:4] == 'Bot']
    for bot in new_bots:
        all_bots.update({bot: importlib.import_module(bot)})
    return all_bots


def class_init(module_name, name):
    return inspect.getmembers(all_games[module_name], inspect.isclass)[0][1](name)


all_games = game_import()
all_bots = bot_import()
game1 = class_init('gametest', '123')
print(game1.play())
game_condition = bytearray(game1.play(), encoding='utf8')

