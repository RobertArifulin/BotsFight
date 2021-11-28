import time
import tkinter
from tkinter import *
from tkinter import filedialog as fd
from tkinter import scrolledtext
from constants import *
from PIL import ImageTk, Image
from game import Game, Status
from tournament import Tournament


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
        origin
            Окно родитель.


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
    is_paused: bool
    tournament: Tournament

    def __init__(self, bots_paths: list[str], game: Game, speed: int, game_number: int, origin: Tk):
        super().__init__()

        self.window = Toplevel(background=BG_COLOR)

        self.bots_paths = bots_paths
        self.game = game
        self.game.game_init()
        self.game_speed = speed
        self.game_number = game_number
        self.origin = origin
        self.is_paused = False

        self.tournament = Tournament(self.game)
        for bot_path in self.bots_paths:
            self.tournament.register_bot(bot_path)
        self.tournament.create_standings()

        self.__status_label_var = StringVar()
        self.__game_title_var = StringVar()
        self.__game_title_var.set(f"{self.tournament.standings[0][0].name} vs\n{self.tournament.standings[0][1].name}")
        self.__status_label_var.set(f"Ход {self.tournament.standings[0][0].name}")

        self.create_ui()

    def create_ui(self):
        # Блок 1
        # задаются параметры окна
        w = self.window.winfo_screenwidth() // 2
        h = self.window.winfo_screenheight() // 2
        w = w - W1_MIN_WIDTH // 2
        h = h - W1_MIN_HEIGHT // 2
        self.window.minsize(W2_MIN_WIDTH, W2_MIN_HEIGHT)
        self.window.geometry(f'{W1_MIN_WIDTH}x{W1_MIN_HEIGHT}+{w}+{h}')
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
                                 text="Стоп", font="Times 16")
        self.__pause_bt.grid(row=0, column=1, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание шкалы скорости
        game_speed_scale = Scale(self.frame1, from_=1, to=10, orient=HORIZONTAL, font=W1_FONT,
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

        # ______________________________
        # mainloop
        self.window.after(10, self.display_game)
        self.window.mainloop()

    def display_tournament_results(self):
        # создание контейнера frame1
        w = self.window.winfo_screenwidth() // 2
        h = self.window.winfo_screenheight() // 2
        w = w - W1_MIN_WIDTH // 2
        h = h - W1_MIN_HEIGHT // 2

        self.frame1 = Frame(self.window, background=BG_COLOR)
        self.frame1.pack(fill=X, padx=GRID_PADX, pady=GRID_PADY, expand=True)
        for i in range(2):
            self.frame1.grid_columnconfigure(i, weight=1)
            self.frame1.grid_rowconfigure(i, weight=1)

        # тестовая кнопка выхода
        close_bt = Button(self.frame1, width=12, height=1, command=self.close_bt_press,
                          text="Назад", font="Times 16")
        close_bt.grid(row=0, column=0, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)
        # создание поля с текстом для имен выбранных ботов
        game_speed_label = Label(self.frame1, text="Результаты Турнира:",
                                 font=W2_FONT, background=BG_COLOR, anchor=CENTER)
        game_speed_label.grid(row=0, column=1, padx=GRID_PADX, sticky=E + W)

        self.frame2 = Frame(self.window, background=BG_COLOR)
        self.frame2.pack(fill=BOTH, expand=True, padx=GRID_PADX, pady=GRID_PADY)

        results_text = scrolledtext.ScrolledText(self.frame2, font=W2_FONT)
        results_text.insert(INSERT, self.create_results_text(self.tournament.tournament_results))
        results_text.pack(side=LEFT, expand=True)

        results_scroll = Scrollbar(self.frame2, command=results_text.yview)
        results_scroll.pack(side=RIGHT, fill=Y, padx=FRAME_PADX, pady=FRAME_PADY)
        results_text.configure(state='disabled', yscrollcommand=results_scroll.set)

    def create_results_text(self, results: list) -> str:
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
        best_bots = ['', -1]
        worst_bots = ['', -1]
        for bot in self.tournament.bots:
            name = bot.name

            if len(bots_res[name][0]) % 10 in [2, 3, 4]:
                s += f"Бот {bot.name} победил {len(bots_res[name][0])} раза:\n"
            else:
                s += f"Бот {bot.name} победил {len(bots_res[name][0])} раз:\n"
            for i in bots_res[name][0]:
                s += f"{i}; "
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
            for i in bots_res[name][1]:
                s += f"{i}; "
            s = s[:-2]
            s += "\n"

            if len(bots_res[name][2]) % 10 in [2, 3, 4]:
                s += f"Проиграл {len(bots_res[name][2])} раза:\n"
            else:
                s += f"Проиграл {len(bots_res[name][2])} раз:\n"
            for i in bots_res[name][2]:
                s += f"{i}; "

            if len(bots_res[name][2]) > worst_bots[1]:
                worst_bots[0] = f"{name}\n"
                worst_bots[1] = len(bots_res[name][2])
            elif len(bots_res[name][2]) == worst_bots[1]:
                worst_bots[0] += f"{name}\n"

            s = s[:-2]
            s += '\n--------------------------------------------------------------------------\n'
        best_bots[0] = best_bots[0]
        worst_bots[0] = worst_bots[0][:-1]
        s += f"Лучшие боты с наибольшим количеством побед - {best_bots[1]}:\n{best_bots[0]}\n"
        s += f"Худшие боты с наибольшим количеством поражений - {worst_bots[1]}:\n{worst_bots[0]}"
        return s

    def close_bt_press(self):
        """ Отвечает за работу close_bt. Сворачивает данное окно и разворачивает StartWindow"""
        self.origin.deiconify()
        self.window.withdraw()

    def clear_ui(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.display_tournament_results()

    def pause_bt_press(self):
        """ Отвечает за работу __pause_bt. Останавливает/запускает игру."""
        try:
            if self.is_paused:
                self.is_paused = False
                self.__pause_bt.configure(text="Стоп")
                self.window.after((10 - self.game_speed) * 50 + 10, self.display_game)
            else:
                self.is_paused = True
                self.__pause_bt.configure(text="Старт")
        except tkinter.TclError:
            pass

    def game_speed_scale_select(self, val):
        """ Отвечает за работу game_speed_scale. Присваивает selected_speed значение со шкалы."""
        self.game_speed = int(float(val))

    def display_game(self):
        """ Отвечает за отрисовку игры. Получает результат хода, масштабирует и отрисовывает картинку с полем."""
        image, title, res = self.tournament.tournament()
        if res:
            self.__status_label_var.set(res)
            self.__game_title_var.set(title)
            height = image.height
            width = image.width
            if int(height / width * self.__board_canvas.winfo_width()):
                image = image.resize((self.__board_canvas.winfo_width(),
                                      min(int(height / width * self.__board_canvas.winfo_width()),
                                          self.__board_canvas.winfo_height())))
            self.window.board = ImageTk.PhotoImage(image)
            image = self.__board_canvas.create_image(2, 2, anchor='nw', image=self.window.board)
            self.__board_canvas.pack(expand=True, fill=BOTH)
            if not self.is_paused:
                self.window.after((10 - self.game_speed) * 50 + 20, self.display_game)
        else:
            self.pause_bt_press()
            self.clear_ui()


class StartWindow(Frame):
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
        super().__init__(background=BG_COLOR)

        self.__game_label_text = StringVar()
        self.__bot_label_text = StringVar()
        self.__game_number_text = StringVar()
        self.__bot_label_text.set('Выбранные боты:\n')
        self.__game_number_text.set('1')

        self.games = games
        self.games_names = list(games.keys())
        self.selected_game_name = ""
        self.selected_game = Game()
        self.selected_bots = []
        self.selected_speed = 1
        self.selected_game_number = 1

        self.TournamentWindow = None

        self.create_ui()

    def create_ui(self):
        """Настраивает окно, создает и настраивет все виджеты."""

        # Блок 1
        # задаются параметры окна
        w = self.master.winfo_screenwidth() // 2
        h = self.master.winfo_screenheight() // 2
        w = w - W1_MIN_WIDTH // 2
        h = h - W1_MIN_HEIGHT // 2
        self.master.minsize(W1_MIN_WIDTH, W1_MIN_HEIGHT)
        self.master.geometry(f'{W1_MIN_WIDTH}x{W1_MIN_HEIGHT}+{w}+{h}')
        self.master.title("Турнир Машин")
        self.pack(fill=BOTH, expand=True)

        # создание контейнера frame1
        frame1 = Frame(self, background=BG_COLOR)
        frame1.pack(fill=X)

        # создание надписи "Выберете игру"
        request_game_label = Label(frame1, text="Выберите игру", width=15,
                                   font=W1_FONT, background=BG_COLOR, anchor=W)
        request_game_label.pack(side=LEFT, padx=FRAME_PADX, pady=FRAME_PADY)

        # создание надписи с именем выбранной игры
        game_label = Label(frame1, text=0, textvariable=self.__game_label_text, font=W1_FONT, background=BG_COLOR)
        game_label.pack()

        # создание listbox с играми
        game_listbox = Listbox(frame1, width=30, height=2, font=W1_FONT)
        for game in self.games_names:
            game_listbox.insert(END, game)
        game_listbox.bind("<<ListboxSelect>>", self.game_listbox_select)

        # создание scrollbar для listbox с играми
        scroll_listbox = Scrollbar(frame1, command=game_listbox.yview)
        scroll_listbox.pack(side=RIGHT, fill=Y, padx=FRAME_PADX, pady=FRAME_PADY)
        game_listbox.pack(fill=X, padx=FRAME_PADX, expand=True)
        game_listbox.config(yscrollcommand=scroll_listbox.set)

        # ______________________________
        # Блок 2
        # создание контейнера frame2
        frame2 = Frame(self, background=BG_COLOR)
        frame2.pack(fill=X)

        # создание надписи "Выберете ботов"
        request_bot_label = Label(frame2, text="Выберите ботов ", width=15,
                                  font=W1_FONT, background=BG_COLOR, anchor=W)
        request_bot_label.pack(side=LEFT, fill=X, padx=FRAME_PADX, pady=FRAME_PADY)

        # импорт картинки проводника
        image = Image.open('images/Windows_Explorer_Icon.png')
        image = image.resize((30, 30))
        self.master.win_explorer = ImageTk.PhotoImage(image)
        # создание кнопки вызова проводника
        file_explorer_bt = Button(frame2, command=self.file_explorer_bt_press,
                                  image=self.master.win_explorer)
        file_explorer_bt.pack(side=LEFT, padx=FRAME_PADX, pady=FRAME_PADY)

        # создание поля с текстом для имен выбранных ботов
        self.__selected_bots_text = Text(frame2, height=5, font=W1_FONT, background=BG_COLOR)
        self.__selected_bots_text.insert(1.0, self.__bot_label_text.get())

        # создание scrollbar для поля с текстом
        scroll_text = Scrollbar(frame2, command=self.__selected_bots_text.yview)
        scroll_text.pack(side=RIGHT, fill=Y, padx=FRAME_PADX, pady=FRAME_PADY)
        self.__selected_bots_text.configure(state='disabled', yscrollcommand=scroll_text.set)
        self.__selected_bots_text.pack(side=LEFT, padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # Блок 3
        # создание контейнера frame3
        frame3 = Frame(self, height=2, background=BG_COLOR)
        frame3.pack(fill=BOTH)

        # create the center widgets
        frame3.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(3, weight=1)

        # создание поля с текстом для имен выбранных ботов
        game_speed_label = Label(frame3, text="Скорость игры",
                                 font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        game_speed_label.grid(row=0, column=0, columnspan=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание поля с текстом для имен выбранных ботов
        game_number_label = Label(frame3, text="Кол-во партий",
                                  font=W1_FONT, background=BG_COLOR, anchor=CENTER)
        game_number_label.grid(row=0, column=3, columnspan=2, padx=GRID_PADX, pady=GRID_PADY, sticky=E + W)

        # создание шкалы скорости
        game_speed_scale = Scale(frame3, from_=1, to=10, orient=HORIZONTAL, font=W1_FONT,
                                 command=self.game_speed_scale_select, background=BG_COLOR)
        game_speed_scale.grid(row=1, column=0, columnspan=2, padx=GRID_PADX, pady=GRID_PADY)

        # создание шкалы кол-ва игр
        game_number_entry = Scale(frame3, from_=1, to=10, orient=HORIZONTAL, font=W1_FONT,
                                  command=self.game_number_scale_select, background=BG_COLOR)
        game_number_entry.grid(row=1, column=3, columnspan=2, padx=GRID_PADX, pady=GRID_PADY)

        # ______________________________
        # Блок 4
        # создание контейнера frame3
        frame4 = Frame(self, background=BG_COLOR)
        frame4.pack(expand=True)

        # создание кнопки начала турнира
        self.__start_tournament_bt = Button(frame4, width=15, height=2, command=self.start_tournament_bt_press,
                                            text="Начать Турнир", font="Times 16", state="disable")
        self.__start_tournament_bt.pack(padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # mainloop
        self.master.mainloop()

    def start_tournament_bt_press(self):
        """ Отвечает за работу __start_tournament_bt. Сворачивает данное окно, создает TournamentWindow."""
        self.master.withdraw()
        if self.TournamentWindow is not None:
            self.TournamentWindow.destroy()
        self.TournamentWindow = TournamentWindow(self.selected_bots, self.selected_game, self.selected_speed, self.selected_game_number,
                                                 self.master)

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

    def file_explorer_bt_press(self):
        """ Отвечает за работу file_explorer_bt. Выводит имена выбранных ботов. Удаляет повторения.
            Проверяет, достаточно ли данных для начала турнира."""
        paths = fd.askopenfilenames(title='Выберете файлы ботов',
                                    filetypes=[('*', '.py'), ('*', '.exe'), ('*', '.pyw')])

        for path in paths:
            if path not in self.selected_bots:
                self.selected_bots.append(path)
            else:
                self.selected_bots.remove(path)

        s = 'Выбранные боты:\n' + '\n'.join([bot.split('/')[-1] for bot in sorted(self.selected_bots)])
        self.__selected_bots_text.configure(state='normal')
        self.__selected_bots_text.delete('1.0', END)
        self.__selected_bots_text.replace(0.0, 1.0, s)
        self.__selected_bots_text.configure(state='disabled')

        if self.selected_game_name and len(self.selected_bots) > 1:
            self.__start_tournament_bt.configure(state="normal")
        else:
            self.__start_tournament_bt.configure(state="disable")
