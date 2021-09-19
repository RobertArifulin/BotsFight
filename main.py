import importlib
import os
import sys, inspect
import subprocess



def bots_import():
    """Импортирует модули с ботами в словарь."""
    all_bots = {}
    new_bots = [i[:-3] for i in os.listdir() if '.py' in i and i != 'main.py' and i != 'gametest.py']
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

res = subprocess.run([sys.executable, 'gametest.py'], input=b'1 2', capture_output=True)
print(str(res.stdout))
print(res.stderr)