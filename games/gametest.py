import importlib.util
import inspect

spec = importlib.util.spec_from_file_location('Game', r'C:\Users\rober\PycharmProjects\BotsFight\game.py')
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
Game = [i for i in inspect.getmembers(foo, inspect.isclass) if i[0] == 'Game'][0][1]


class game1(Game):

    def __init__(self, name):
        self.name = name
        self.board = [[0] * 5 for _ in range(5)]

    def play(self):
        return '1 2'
