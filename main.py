import importlib
import os
import inspect


def bots_import():
    """Импортирует модули с ботами в словарь."""
    all_bots = {}
    new_bots = [i[:-3] for i in os.listdir() if '.py' in i and i != 'main.py']
    for bot in new_bots:
        all_bots.update({bot: importlib.import_module(bot)})
    return all_bots


def bots_init(module_name, game):
    return inspect.getmembers(all_bots[module_name], inspect.isclass)[0][1](game)


all_bots = bots_import()
bot1 = bots_init('testbot1', '123')
bot2 = bots_init('testbot2', '123')
print(bot1.play())
print(bot2.play())
# print(inspect.getmembers(all_bots['testbot1'], inspect.isclass)[0][1])
