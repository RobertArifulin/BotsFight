import importlib
import os
import sys, inspect
import subprocess


def module_import():
    """Импортирует модули с играми в словарь."""

    all_module = {}
    all_module.update({'bot': importlib.import_module('bot')})
    new_games = [i[:-3] for i in os.listdir() if i == 'gametest.py']
    for game in new_games:
        all_module.update({game: importlib.import_module(game)})

    return all_module


def class_init(module_name, name):
    return inspect.getmembers(all_module[module_name], inspect.isclass)[0][1](name)


all_module = module_import()
bot = class_init('bot', input())
game1 = class_init('gametest', '123')
print(bot.request_bot('12 32'))
game_condition = bytearray(game1.play(), encoding='utf8')

