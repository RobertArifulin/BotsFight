import sys
import subprocess


class Bot:
    """ Класс Bot используется для связи с исполняемыми файлами - ботами.
        Также может запускать python файлы с ботами.

        Attributes
        ----------
        path : str
            Полный путь до исполняемого файла с ботом.
            Относительный путь тоже возможен, но будьте внимательны с раположением файла!


        Methods
        -------
        request_bot(game_condition)
            Запускает исполняемый файл и передает ему на вход game_condition.
            Получает ответ и возвращает его.
    """
    path: str

    def __init__(self, path: str):
        self.path = path

    def request_bot(self, game_condition: str):
        """ Запускает исполняемый файл и передает ему на вход game_condition.
            Получает ответ и возвращает его.

            Проверяет расширение файла, если это python файл запускает его через интерпретатор.

            Если файла по указанному пути не существует, вызывает ошибку FileNotFoundError.


            Parameters
            ----------
            game_condition : str
                состояние игрового поля на данный момент.
        """

        game_condition = bytearray(game_condition, encoding='utf-8')
        if self.path.split('.')[-1] == 'py':
            res = subprocess.run([sys.executable, self.path], input=game_condition, capture_output=True, check=True)
        else:
            res = subprocess.run(self.path, input=game_condition, capture_output=True, check=True)
        bot_response = res.stdout.decode("utf-8")
        return bot_response
