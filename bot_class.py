import importlib
import os
import sys, inspect
import subprocess

class Bot:

    def __init__(self, name):
        self.name = name

    def request_bot(self, game_condition):
        res = subprocess.run([sys.executable, self.name], input=game_condition, capture_output=True)
        bot_response = res.stdout.decode("utf-8")
        return bot_response