import importlib
import os
import inspect
import importlib.util


def module_import(path: str):
    """Импортирует py модули из директории по пути path с играми и/или ботами в словарь."""

    modules = {}
    new_modules = [i for i in os.listdir(path) if i[-3:] == '.py' and (i[:4] == 'game' or i[:3] == 'bot')]
    for module in new_modules:
        spec = importlib.util.spec_from_file_location(module[:-3], f'{path}\{module}')
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        modules.update({module[:-3]: foo})

    return modules


def class_init(module_name, name):
    return [i for i in inspect.getmembers(all_modules[module_name], inspect.isclass) if i[0] == name][0][1]
    # return inspect.getmembers(all_modules[module_name], inspect.isclass)[0][1](name)


all_modules = {}
all_modules.update({'bot': importlib.import_module('bot')})
all_modules.update({'game': importlib.import_module('game')})
all_modules.update(module_import('games'))
all_modules.update(module_import('.'))
print(all_modules, 1)
bot = class_init('bot', input())
game1 = class_init('gametest', '123')
# print(bot.request_bot('12 32'))
# game_condition = bytearray(game1.play(), encoding='utf8')
# СПРОСИТЬ ПРО АВТОЗАПУС МОДУЛЕЙ ПИТОНА.