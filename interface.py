import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import scrolledtext
import tkinter.ttk as ttk
from constants import *
from PIL import ImageTk, Image
from game import Game
from tournament import Tournament
from tabulate import tabulate


class TournamentWindow(Frame):
    """
        Класс TournamentWindow - зависимое от StartWindow окно, оно отвечает за отображение процесса игры
        и обеспечивает взаимодействие с бэкендом.

        Attributes
        ----------
        bots_paths: list[str]
            Список путей до файлов с ботами.
        game: Game
            Игра.
        speed: int
            Скорость игры.
        game_number: int
            Количество партий в одной игре.
        origin: Tk
            Окно родитель.
        is_fast: bool
            Флаг режима.
        is_paused: bool
            Флаг паузы.
        board_image: Image
            Картинка игрового поля.
        last_callback_time: float
            Последнее время вызова функции resize.

        Methods
        -------
        create_ui()
            Настраивает окно, создает и настраивет все виджеты.
        close_bt_press()
            Отвечает за работу close_bt.
        pause_bt_press()
            Отвечает за работу __pause_bt.
        game_speed_scale_select()
            Отвечает за работу game_speed_scale.
        display_game()
            Отвечает отрисовку игры.

    """
    window: Toplevel
    bots_paths: list[str]
    game: Game
    game_speed: int
    game_number: int
    origin: Tk
    tournament: Tournament
    is_fast: bool
    is_paused: bool
    board_image: Image
    last_callback_time: float

    def __init__(self, bots_paths: list[str], game: Game, speed: int, game_number: int, is_fast: bool, origin: Tk):
        super().__init__()

        self.window = Toplevel(background=BG_COLOR)

        self.bots_paths = bots_paths
        self.game = game
        self.game.game_init()
        self.is_fast = is_fast
        self.game_speed = speed
        self.board_image = None
        self.game_number = game_number
        self.origin = origin
        self.is_paused = False
        self.last_callback_time = 0

        self.tournament = Tournament(self.game, self.game_number)
        for bot_path in self.bots_paths:
            self.tournament.register_bot(bot_path)
        self.tournament.create_standings()

        self.__status_label_var = StringVar()
        self.__game_title_var = StringVar()
        self.__game_title_var.set(f"{self.tournament.standings[0][0].name} vs\n{self.tournament.standings[0][1].name}")
        self.__status_label_var.set(f"Ход {self.tournament.standings[0][0].name}")

        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.canvas = None
        self.__board_canvas = None
        self.__pause_bt = None

        self.create_ui()

    def create_ui(self):
        # Блок 1
        # задаются параметры окна
        self.last_callback_time = time.time()
        w = self.window.winfo_screenwidth() // 2
        h = self.window.winfo_screenheight() // 2
        w = w - W2_MIN_WIDTH // 2
        h = h - W2_MIN_HEIGHT // 2
        self.window.minsize(W2_MIN_WIDTH, W2_MIN_HEIGHT)
        self.window.geometry(f'{W2_MIN_WIDTH}x{W2_MIN_HEIGHT}+{w}+{h}')
        self.window.title("Турнир Машин")
        self.pack(expand=True, fill=BOTH)
        for i in range(2):
            self.window.grid_columnconfigure(i, weight=1)
            self.window.grid_rowconfigure(i, weight=1)

        # создание контейнера frame1
        self.frame1 = Frame(self.window, background=BG_COLOR)
        self.frame1.grid(row=0, column=0, columnspan=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W + N + S)
        for i in range(2):
            self.frame1.grid_columnconfigure(i, weight=1)
            self.frame1.grid_rowconfigure(i, weight=1)

        # тестовая кнопка выхода
        close_bt = Button(self.frame1, width=12, height=1, command=self.close_bt_press,
                          text="Отмена ", font="Times 16")
        close_bt.grid(row=0, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # тестовая кнопка выхода
        self.__pause_bt = Button(self.frame1, width=12, height=1, command=self.pause_bt_press,
                                 text="Пауза", font="Times 16")
        self.__pause_bt.grid(row=0, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание шкалы скорости
        game_speed_scale = Scale(self.frame1, from_=0, to=10, orient=HORIZONTAL, font=W1_FONT,
                                 command=self.game_speed_scale_select, background=BG_COLOR)
        game_speed_scale.set(self.game_speed)
        game_speed_scale.grid(row=0, column=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание поля с текстом для имен выбранных ботов
        game_speed_label = Label(self.frame1, text="Скорость игры",
                                 font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        game_speed_label.grid(row=1, column=2, padx=GRID_PADX, sticky=E + W + N)

        # ______________________________
        # Блок 2
        # создание контейнера frame2
        self.frame2 = Frame(self.window, background=BG_COLOR)
        self.frame2.grid(row=1, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=W + N + S + E)
        for i in range(3):
            self.frame2.grid_columnconfigure(i, weight=1)
            self.frame2.grid_rowconfigure(i, weight=1)

        # вывод заголовка игры
        game_title_label = Label(self.frame2, text=0, textvariable=self.__game_title_var, width=15,
                                 font=W2_FONT, background=BG_COLOR, anchor=CENTER)
        game_title_label.grid(row=0, column=0, sticky=W + E, pady=5)

        # вывод статуса игры
        status_label = Label(self.frame2, text=0, textvariable=self.__status_label_var, width=15,
                             font=W2_FONT, background=BG_COLOR, anchor=CENTER)
        status_label.grid(row=1, column=0, sticky=W + E, pady=5)

        # ______________________________
        # Блок 3
        # создание контейнера frame3
        self.frame3 = Frame(self.window, background=BG_COLOR)
        self.frame3.grid(row=1, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=E + N + S + W)
        for i in range(3):
            self.frame3.grid_columnconfigure(i, weight=1)
            self.frame3.grid_rowconfigure(i, weight=1)

        self.__board_canvas = Canvas(self.frame3, height=400, width=300)
        self.__board_canvas.pack(expand=True, fill=BOTH)
        self.board_image = self.tournament.game.draw_board_image()
        self.display_board()

        self.window.bind('<Configure>', self.resize)

        # ______________________________
        # mainloop
        self.window.after(10, self.play_game)
        self.window.mainloop()

    def resize(self, _=None):
        cur_time = time.time()
        if (cur_time - self.last_callback_time) > 0.05:
            self.display_board()
            self.last_callback_time = time.time()

    def display_tournament_results(self):
        # создание контейнера frame1
        for i in self.window.winfo_children():
            i.destroy()

        self.frame1 = Frame(self.window, background=BG_COLOR)
        self.frame1.pack(side=TOP, fill=X, padx=GRID_PADX)
        for i in range(2):
            self.frame1.grid_columnconfigure(i, weight=1)
            self.frame1.grid_rowconfigure(i, weight=1)

        # тестовая кнопка выхода
        close_bt = Button(self.frame1, width=12, height=1, command=self.close_bt_press,
                          text="Назад", font="Times 16")
        close_bt.grid(row=0, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)
        # создание поля с текстом "результаты турнира"
        game_speed_label = Label(self.frame1, text="Победы / Ничьи / Поражения",
                                 font='Times 14', background=BG_COLOR, anchor=CENTER)
        game_speed_label.grid(row=0, column=1, padx=GRID_PADX, sticky=E + W)

        self.frame2 = Frame(self.window, background=BG_COLOR)
        self.frame2.pack(side=TOP, fill=BOTH, expand=True, padx=GRID_PADX, pady=GRID_PADY)

        value, headers = self.reformat_results(self.tournament.tournament_results)

        def fixed_map(option):
            return [elm for elm in style.map("Treeview", query_opt=option)
                    if elm[:2] != ("!disabled", "!selected")]

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=('JetBrains Mono', 13))
        style.configure("Treeview.Heading", font=('JetBrains Mono', 13))
        style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))

        tree = ttk.Treeview(self.frame2, column=headers, show='headings', height=len(value) + 1)
        tree.tag_configure('oddrow', background='#D4D4D4')
        for i in range(len(headers) + 1):
            w = self.frame2.winfo_width() // (len(headers) + 1)
            if i == 0:
                tree.column(f"# {i}", anchor=CENTER, width=w)
                tree.heading(f"# {i}", text="")
            else:
                tree.column(f"# {i}", anchor=CENTER, width=w)
                tree.heading(f"# {i}", text=f"{headers[i - 1]}")

        for i in range(len(value)):
            if i % 2 == 0:
                tree.insert('', 'end', text=f"{i}", values=value[i])
            else:
                tree.insert('', 'end', text=f"{i}", values=value[i], tags=("oddrow",))
        tree.pack(side=LEFT, expand=True, fill=BOTH, padx=GRID_PADX, pady=GRID_PADY)

        self.frame3 = Frame(self.window, background=BG_COLOR)
        self.frame3.pack(fill=BOTH, expand=True, padx=GRID_PADX, pady=GRID_PADY)

        results_text = scrolledtext.ScrolledText(self.frame3, wrap="none", font='Times 13',
                                                 height=self.old_text_creator(self.tournament.tournament_results).count("\n") + 1)
        results_text.insert(INSERT, self.old_text_creator(self.tournament.tournament_results))
        results_text.configure(state="disable")
        results_text.pack(side=LEFT, expand=True, fill=X, padx=GRID_PADX, pady=GRID_PADY)

    def create_results_table(self, results: list) -> str:
        value, headers = self.reformat_results(results)
        s = tabulate(value, headers, tablefmt="grid")
        return s

    def reformat_results(self, results: list) -> tuple[list, list]:
        bots_res = {}
        for bot in self.tournament.bots:
            name = bot.name
            bots_res.update({name: [[], [], []]})
        for result in results:
            bot1, res, bot2 = result.split()
            if res == "draw":
                bots_res[bot1][1].append(bot2)
                bots_res[bot2][1].append(bot1)
            else:
                bots_res[bot1][0].append(bot2)
                bots_res[bot2][2].append(bot1)
        headers = [" "]
        headers.extend(list(bots_res.keys()))
        n = len(bots_res)
        value = []
        for i in range(n):
            new_line = [headers[i + 1]]
            for j in range(n):
                if i == j:
                    new_line.append("~~~~~~")
                else:
                    win = bots_res[headers[i + 1]][0].count(headers[j + 1])
                    draw = bots_res[headers[i + 1]][1].count(headers[j + 1])
                    lose = bots_res[headers[i + 1]][2].count(headers[j + 1])
                    new_line.append(f"{win} / {draw} / {lose}")
            value.append(new_line.copy())
        return value, headers

    def old_text_creator(self, results: list) -> str:
        s = ""
        bots_res = {}
        for bot in self.tournament.bots:
            name = bot.name
            bots_res.update({name: [[], [], []]})
        for result in results:
            bot1, res, bot2 = result.split()
            if res == "draw":
                bots_res[bot1][1].append(bot2)
                bots_res[bot2][1].append(bot1)
            else:
                bots_res[bot1][0].append(bot2)
                bots_res[bot2][2].append(bot1)
        best_bots = ['', 0]
        worst_bots = ['', 0]
        for bot in self.tournament.bots:
            name = bot.name

            if len(bots_res[name][0]) % 10 in [2, 3, 4]:
                s += f"Бот {bot.name} победил {len(bots_res[name][0])} раза:\n"
            else:
                s += f"Бот {bot.name} победил {len(bots_res[name][0])} раз:\n"

            set_names = []
            for i in bots_res[name][0]:
                if i not in set_names:
                    set_names.append(i)
            res = dict.fromkeys(set_names, 0)
            while len(set_names):
                key = set_names.pop()
                res[key] = bots_res[name][0].count(key)
            for i in res.keys():
                s += f"{i}: {res[i]}; "
            s = s[:-2]
            s += "\n"

            if len(bots_res[name][0]) > best_bots[1]:
                best_bots[0] = f"{name}\n"
                best_bots[1] = len(bots_res[name][0])
            elif len(bots_res[name][0]) == best_bots[1]:
                best_bots[0] += f"{name}\n"

            if len(bots_res[name][1]) % 10 in [2, 3, 4]:
                s += f"Сыграл вничью {len(bots_res[name][1])} раза:\n"
            else:
                s += f"Сыграл вничью {len(bots_res[name][1])} раз:\n"

            set_names = []
            for i in bots_res[name][1]:
                if i not in set_names:
                    set_names.append(i)
            res = dict.fromkeys(set_names, 0)
            while len(set_names):
                key = set_names.pop()
                res[key] = bots_res[name][1].count(key)
            for i in res.keys():
                s += f"{i}: {res[i]}; "
            s = s[:-2]
            s += "\n"

            if len(bots_res[name][2]) % 10 in [2, 3, 4]:
                s += f"Проиграл {len(bots_res[name][2])} раза:\n"
            else:
                s += f"Проиграл {len(bots_res[name][2])} раз:\n"

            set_names = []
            for i in bots_res[name][2]:
                if i not in set_names:
                    set_names.append(i)
            res = dict.fromkeys(set_names, 0)
            while len(set_names):
                key = set_names.pop()
                res[key] = bots_res[name][2].count(key)
            for i in res.keys():
                s += f"{i}: {res[i]}; "

            if len(bots_res[name][2]) > worst_bots[1]:
                worst_bots[0] = f"{name}\n"
                worst_bots[1] = len(bots_res[name][2])
            elif len(bots_res[name][2]) == worst_bots[1]:
                worst_bots[0] += f"{name}\n"

            s = s[:-2]
            s += '\n--------------------------------------------------------------------------\n'
        best_bots[0] = best_bots[0]
        worst_bots[0] = worst_bots[0][:-1]

        s += f"Лучшие боты с наибольшим количеством побед ({best_bots[1]}):\n{best_bots[0]}\n"
        s += f"Худшие боты с наибольшим количеством поражений ({worst_bots[1]}):\n{worst_bots[0]}"
        return s

    def close_bt_press(self):
        """ Отвечает за работу close_bt. Сворачивает данное окно и разворачивает StartWindow"""
        self.origin.deiconify()
        self.clear_ui()
        self.destroy()
        self.window.withdraw()

    def clear_ui(self):
        for i in self.window.winfo_children():
            i.destroy()

    def pause_bt_press(self):
        """ Отвечает за работу __pause_bt. Останавливает/запускает игру."""
        try:
            if self.is_paused:
                self.is_paused = False
                self.__pause_bt.configure(text="Пауза")
                self.window.after((10 - self.game_speed) * 50 + 10, self.play_game)
            else:
                self.is_paused = True
                self.__pause_bt.configure(text="Продолжить")
        except TclError:
            pass

    def game_speed_scale_select(self, val):
        """ Отвечает за работу game_speed_scale. Присваивает selected_speed значение со шкалы."""
        self.game_speed = int(float(val))

    def play_game(self):
        """ Отвечает за отрисовку игры. Получает результат хода, масштабирует и отрисовывает картинку с полем."""
        try:
            self.board_image, title, res = self.tournament.tournament()
            if res:
                self.__status_label_var.set(res)
                self.__game_title_var.set(title)
                self.display_board()
                if not self.is_paused:
                    if ("Победа" in res or "Ничья" in res or self.game_speed == 0) and not self.is_fast:
                        self.pause_bt_press()
                if not self.is_paused:
                    self.window.after((10 - self.game_speed) * 60 + 20, self.play_game)
            else:
                self.pause_bt_press()
                self.clear_ui()
                self.display_tournament_results()
        except:
            exit(0)

    def display_board(self):
        try:
            image = self.board_image
            height = image.height
            width = image.width
            k = height / width
            if int(k * self.__board_canvas.winfo_width()):
                image = image.resize(
                    (min(self.__board_canvas.winfo_width(), int(k * self.__board_canvas.winfo_height())),
                     min(int(k * self.__board_canvas.winfo_width()), self.__board_canvas.winfo_height())))
            self.window.board = ImageTk.PhotoImage(image)
            self.canvas = self.__board_canvas.create_image(2, 2, anchor='nw', image=self.window.board)
        except Exception:
            pass


class StartWindow(Tk):
    """ Класс StartWindow - основное окно интерфейса, оно рисует начальное окно
        и обеспечивает взаимодействие с бэкендом.

        Attributes
        ----------
        games: list[str]
            Список доступных для выбора имен игр.
        selected_game_name: str
            Имя игры, которую выбрали.
        selected_bots: list
            Список путей до файлов с ботами.

        Methods
        -------
        create_ui()
            Настраивает окно, создает и настраивет все виджеты.
        game_listbox_select()
            Отвечает за работу game_listbox.
        file_explorer_bt_press()
            Отвечает за работу file_explorer_button.
        number_game_entry_select()
            Отвечает за работу number_game_entry.
        start_tournament_bt_press()
            Отвечает за работу __start_tournament_bt.
        delete_bot_bt_press(self):
            Отвечает за работу delete_bot_bt.
        game_speed_scale_select()
            Отвечает за работу game_speed_scale.
        number_game_validate()
            Отвечает за ввод только цифр number_game_entry.
    """
    games: dict
    selected_game_name: str
    selected_game: Game
    selected_bots: list[str]
    selected_speed: int
    selected_game_number: int

    def __init__(self, games: dict):
        super().__init__()

        self.__game_label_text = StringVar()
        self.__bot_label_text = StringVar()
        self.__game_number_text = StringVar()
        self.__game_number_text.set('1')

        self.games = games
        self.games_names = list(games.keys())
        self.selected_game_name = ""
        self.selected_game = Game()
        self.selected_bots = []
        self.selected_speed = 1
        self.selected_game_number = 1
        self.is_fast = False

        self.TournamentWindow = None
        self.frame1 = None
        self.isfast_bt = None
        self.game_speed_scale = None
        self.__start_tournament_bt = None
        self.__selected_bots_lbox = None

        # импорт картинки галочки
        image = Image.open('images/Check_Ico.png')
        image = image.resize((32, 32))
        self.check_png = ImageTk.PhotoImage(image)

        # импорт картинки галочки
        image = Image.open('images/Check_Ico.png')
        image = image.resize((32, 32))
        self.check_png = ImageTk.PhotoImage(image)

        # импорт картинки крестика
        image = Image.open('images/Cross_Ico.png')
        image = image.resize((32, 32))
        self.cross_png = ImageTk.PhotoImage(image)

        self.create_ui()

    def create_ui(self):
        """Настраивает окно, создает и настраивет все виджеты."""

        # Блок 1
        # задаются параметры окна
        w = self.winfo_screenwidth() // 2
        h = self.winfo_screenheight() // 2
        w = w - W1_MIN_WIDTH // 2
        h = h - W1_MIN_HEIGHT // 2
        self.minsize(W1_MIN_WIDTH, W1_MIN_HEIGHT)
        self.geometry(f'{W1_MIN_WIDTH}x{W1_MIN_HEIGHT}+{w}+{h}')
        self.title("Турнир Машин")

        # создание контейнера frame1
        self.frame1 = Frame(self, background=BG_COLOR)
        self.frame1.pack(fill=X)

        for i in range(4):
            self.frame1.grid_rowconfigure(i, weight=1)
        self.frame1.grid_columnconfigure(1, weight=1)

        # создание надписи "Выберете игру"
        request_game_label = Label(self.frame1, text="Выбрать Игру", font=W1_FONT, background=BG_COLOR)
        request_game_label.grid(row=1, column=0, rowspan=2, padx=FRAME_PADX, pady=FRAME_PADY)

        # создание надписи с именем выбранной игры
        game_label = Label(self.frame1, text=0, textvariable=self.__game_label_text, font=W1_FONT, background=BG_COLOR)
        game_label.grid(row=0, column=1, padx=FRAME_PADX, pady=FRAME_PADY)

        # создание надписи "Выбранная игра:"
        selected_game_label = Label(self.frame1, text="Выбранная Игра", font=W1_FONT, background=BG_COLOR)
        selected_game_label.grid(row=0, column=0, padx=FRAME_PADX, pady=FRAME_PADY)

        # создание listbox с играми
        game_listbox = Listbox(self.frame1, width=30, height=LB_HEIGHT, font=W1_FONT)
        for game in self.games_names:
            game_listbox.insert(END, game)
        game_listbox.bind("<<ListboxSelect>>", self.game_listbox_select)

        # создание scrollbar для listbox с играми
        scroll_listbox = Scrollbar(self.frame1, command=game_listbox.yview)
        scroll_listbox.grid(row=1, column=2, rowspan=2, padx=FRAME_PADX, pady=FRAME_PADY, sticky=N + S + W)
        game_listbox.config(yscrollcommand=scroll_listbox.set)
        game_listbox.grid(row=1, column=1, rowspan=2, sticky=E + W, padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # Блок 2
        # создание контейнера frame2
        frame2 = Frame(self, background=BG_COLOR)
        frame2.pack(fill=X)
        for i in range(3):
            frame2.grid_rowconfigure(i, weight=1)
        frame2.grid_columnconfigure(2, weight=1)

        # создание надписи "Выбрать Ботов"
        request_bot_label = Label(frame2, text="Выбрать Ботов", width=15,
                                  font=W1_FONT, background=BG_COLOR)
        request_bot_label.grid(row=1, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E)

        # создание надписи "Удалить Бота"
        delete_bot_label = Label(frame2, text="Удалить Бота", width=15,
                                 font=W1_FONT, background=BG_COLOR)
        delete_bot_label.grid(row=2, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E)

        # импорт картинки проводника
        image = Image.open('images/Windows_Explorer_Icon.png')
        image = image.resize((32, 32))
        win_explorer = ImageTk.PhotoImage(image)
        # создание кнопки вызова проводника
        file_explorer_bt = Button(frame2, command=self.file_explorer_bt_press,
                                  image=win_explorer)
        file_explorer_bt.grid(row=1, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=W)
        # file_explorer_bt.pack(side=LEFT, padx=FRAME_PADX, pady=FRAME_PADY)

        # импорт картинки мусорки
        image = Image.open('images/Delete_Icon.png')
        image = image.resize((32, 32))
        delete_png = ImageTk.PhotoImage(image)
        # создание кнопки удаления бота
        bot_delete_bt = Button(frame2, command=self.delete_bot_bt_press,
                               image=delete_png)
        bot_delete_bt.grid(row=2, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=W)

        # создание поля с текстом для имен выбранных ботов
        self.__selected_bots_lbox = Listbox(frame2, height=LB_HEIGHT, width=23, font=W1_FONT, background=BG_COLOR)

        # создание надписи "Выбранные Боты"
        selected_bots_label = Label(frame2, text="Выбранные Боты", width=15,
                                    font=W1_FONT, background=BG_COLOR)
        selected_bots_label.grid(row=0, column=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание scrollbar для поля с текстом
        scroll_text = Scrollbar(frame2, command=self.__selected_bots_lbox.yview)
        scroll_text.grid(row=1, column=3, rowspan=2, padx=GRID_PADX, pady=GRID_PADY, sticky=N + S)
        self.__selected_bots_lbox.configure(yscrollcommand=scroll_text.set)
        self.__selected_bots_lbox.grid(row=1, column=2, rowspan=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # ______________________________
        # Блок 3
        # создание контейнера frame3
        frame3 = Frame(self, height=2, background=BG_COLOR)
        frame3.pack(fill=BOTH)

        # create the center widgets
        for i in range(2):
            frame3.grid_rowconfigure(i, weight=1)
            frame3.grid_columnconfigure(i, weight=1)
        frame3.grid_columnconfigure(2, weight=1)

        # создание поля с текстом для имен выбранных ботов
        game_speed_label = Label(frame3, text="Скорость Игры",
                                 font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        game_speed_label.grid(row=0, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание шкалы скорости
        self.game_speed_scale = Scale(frame3, from_=0, to=10, orient=HORIZONTAL, font=W1_FONT,
                                      command=self.game_speed_scale_select, background=BG_COLOR)
        self.game_speed_scale.set(1)
        self.game_speed_scale.grid(row=1, column=0, padx=GRID_PADX, pady=GRID_PADY)

        isfast_label = Label(frame3, text="Быстрый Режим", font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        isfast_label.grid(row=0, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание чек-кнопки
        self.isfast_bt = Button(frame3, width=32, height=32, command=self.isfast_bt_press,
                                background=BG_COLOR, image=self.cross_png)
        self.isfast_bt.grid(row=1, column=1, padx=GRID_PADX, pady=GRID_PADY)

        # создание поля с текстом для имен выбранных ботов
        game_number_label = Label(frame3, text="Кол-во Партий",
                                  font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        game_number_label.grid(row=0, column=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание шкалы кол-ва игр
        game_number_entry = Scale(frame3, from_=1, to=10, orient=HORIZONTAL, font=W1_FONT,
                                  command=self.game_number_scale_select, background=BG_COLOR)
        game_number_entry.grid(row=1, column=2, padx=GRID_PADX, pady=GRID_PADY)

        # ______________________________
        # Блок 4
        # создание контейнера frame3
        frame4 = Frame(self, background=BG_COLOR)
        frame4.pack(fill=BOTH, expand=True)

        # создание кнопки начала турнира
        self.__start_tournament_bt = Button(frame4, width=15, height=2, command=self.start_tournament_bt_press,
                                            text="Начать Турнир", font="Times 16", state="disable")
        self.__start_tournament_bt.pack(expand=True, padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # mainloop
        self.mainloop()

    def start_tournament_bt_press(self):
        """ Отвечает за работу __start_tournament_bt. Сворачивает данное окно, создает TournamentWindow."""
        self.withdraw()
        self.TournamentWindow = None
        try:
            self.TournamentWindow = TournamentWindow(self.selected_bots, self.selected_game, self.selected_speed,
                                                     self.selected_game_number, self.is_fast, self)
        except KeyboardInterrupt:
            exit(0)

    def isfast_bt_press(self):
        """ Отвечает за работу __is_fast_bt. Сворачивает данное окно, создает TournamentWindow."""
        if self.is_fast:
            self.is_fast = False
            self.isfast_bt.configure(image=self.cross_png)
        else:
            self.is_fast = True
            self.game_speed_scale.set(10)
            self.isfast_bt.configure(image=self.check_png)

    def game_speed_scale_select(self, val):
        """ Отвечает за работу game_speed_scale. Присваивает selected_speed значение со шкалы."""
        self.selected_speed = int(val)

    def game_number_scale_select(self, val):
        """ Отвечает за работу game_number_entry. Присваивает selected_game_number значение со шкалы."""
        self.selected_game_number = int(val)

    def game_listbox_select(self, val):
        """ Отвечает за работу game_listbox. Присваивает __game_label_text имя выбранной игры.
            Проверяет, достаточно ли данных для начала турнира."""
        try:
            sender = val.widget
            idx = sender.curselection()
            value = sender.get(idx)
            self.__game_label_text.set(value)
            self.selected_game_name = self.__game_label_text.get()
            self.selected_game = self.games[self.selected_game_name]()
            if self.selected_game_name and len(self.selected_bots) > 1:
                self.__start_tournament_bt.configure(state="normal")
            else:
                self.__start_tournament_bt.configure(state="disable")
        except TclError:
            pass

    def delete_bot_bt_press(self):
        """ Отвечает за работу delete_bot_bt. Удаляет выранного бота. Обновляет виджет."""
        deleted_bots = self.__selected_bots_lbox.curselection()

        if deleted_bots:
            self.selected_bots.pop(deleted_bots[0])
            self.selected_bots.sort()

            s = [bot.split('/')[-1] for bot in self.selected_bots]
            self.__selected_bots_lbox.delete(0, END)
            for i in s:
                self.__selected_bots_lbox.insert(END, i)

            if self.selected_game_name and len(self.selected_bots) > 1:
                self.__start_tournament_bt.configure(state="normal")
            else:
                self.__start_tournament_bt.configure(state="disable")

    def file_explorer_bt_press(self):
        """ Отвечает за работу file_explorer_bt. Выводит имена выбранных ботов. Удаляет повторения.
            Проверяет, достаточно ли данных для начала турнира."""
        paths = fd.askopenfilenames(title='Выберете файлы ботов',
                                    filetypes=[('*', '.py'), ('*', '.exe'), ('*', '.pyw')])
        l = self.__selected_bots_lbox.get(0, END)
        for path in paths:
            if path not in self.selected_bots and path.split("/")[-1] not in l:
                self.selected_bots.append(path)
        self.selected_bots.sort()

        self.__selected_bots_lbox.delete(0, END)
        s = [bot.split('/')[-1] for bot in self.selected_bots]
        for i in s:
            self.__selected_bots_lbox.insert(END, i)

        if self.selected_game_name and len(self.selected_bots) > 1:
            self.__start_tournament_bt.configure(state="normal")
        else:
            self.__start_tournament_bt.configure(state="disable")
