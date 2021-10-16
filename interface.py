from tkinter import *
from tkinter import filedialog as fd
from constants import *
from PIL import ImageTk, Image
import time
from game import Game, Status
from tournament import Tournament
from bot import Bot


class TournamentWindow(Frame):
    """

    """

    def __init__(self, bots_paths: list[str], game: Game, speed: int, game_number: int, origin):
        super().__init__()

        self.window = Toplevel()

        self.bots_paths = bots_paths
        self.game = game
        self.speed = speed
        self.game_number = game_number
        self.origin = origin

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
        self.pack(fill=BOTH, expand=True)

        # создание контейнера frame1
        frame1 = Frame(self.window, background="red")
        frame1.pack(expand=True)

        button = Button(frame1, width=15, height=2, command=self.press,
                             text="Скрыть", font="Times 16")
        button.pack(padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # mainloop
        self.master.mainloop()

    def press(self):
        self.origin.deiconify()
        tournament = Tournament(self.game)
        for bot_path in self.bots_paths:
            tournament.register_bot(bot_path)
        tournament.create_standings()

        results = tournament.tournament()
        print(results)
        self.window.withdraw()


class StartWindow(Frame):
    """ Класс StartWindow рисует начальное окно и обеспечивает передачу данных,
        введенных пользователем, далее по программе.

        Attributes
        ----------
        all_games: list[str]
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
            Отвечает за работу start_tournament_bt.
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
        self.start_tournament_bt = None
        self.selected_bots_text = None
        self.games = games
        self.games_names = list(games.keys())
        self.selected_game_name = ""
        self.selected_game = None
        self.selected_bots = []
        self.selected_speed = 1
        self.selected_game_number = 1
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
        request_game_label = Label(frame1, text="Выберете игру", width=15,
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
        request_bot_label = Label(frame2, text="Выберете ботов ", width=15,
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
        self.selected_bots_text = Text(frame2, height=5, font=W1_FONT, background=BG_COLOR)
        self.selected_bots_text.insert(1.0, self.__bot_label_text.get())

        # создание scrollbar для поля с текстом
        scroll_text = Scrollbar(frame2, command=self.selected_bots_text.yview)
        scroll_text.pack(side=RIGHT, fill=Y, padx=FRAME_PADX, pady=FRAME_PADY)
        self.selected_bots_text.configure(state='disabled', yscrollcommand=scroll_text.set)
        self.selected_bots_text.pack(side=LEFT, padx=FRAME_PADX, pady=FRAME_PADY)

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

        # создание поля ввода для кол-ва партий
        vcmd = (self.master.register(self.number_game_validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        game_number_entry = Entry(frame3, textvariable=self.__game_number_text, validatecommand=vcmd,
                                  validate='key', background=BG_COLOR, font=W1_FONT)
        game_number_entry.grid(row=1, column=3, columnspan=2, padx=GRID_PADX, pady=GRID_PADY)

        # ______________________________
        # Блок 4
        # создание контейнера frame3
        frame4 = Frame(self, background=BG_COLOR)
        frame4.pack(expand=True)

        # создание кнопки начала турнира
        self.start_tournament_bt = Button(frame4, width=15, height=2, command=self.start_tournament_bt_press,
                                          text="Начать Турнир", font="Times 16", state="disable")
        self.start_tournament_bt.pack(padx=FRAME_PADX, pady=FRAME_PADY)

        # ______________________________
        # mainloop
        self.master.mainloop()

    def number_game_validate(self, action, index, value_if_allowed, prior_value,
                             text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                a = int(value_if_allowed)
                self.selected_game_number = a
                return True
            except ValueError:
                return False
        return False

    def start_tournament_bt_press(self):
        self.master.withdraw()
        TournamentWindow(self.selected_bots, self.selected_game, self.selected_speed, self.selected_game_number,
                         self.master)

    def game_speed_scale_select(self, val):
        self.selected_speed = int(float(val))

    def game_number_entry_on(self, val):
        self.selected_game_number = int(val)

    def game_listbox_select(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.__game_label_text.set(value)
        self.selected_game_name = self.__game_label_text.get()
        self.selected_game = self.games[self.selected_game_name]()
        if self.selected_game_name and len(self.selected_bots) > 1:
            self.start_tournament_bt.configure(state="normal")
        else:
            self.start_tournament_bt.configure(state="disable")

    def file_explorer_bt_press(self):
        paths = fd.askopenfilenames(title='Выберете файлы ботов', filetypes=[('*', '.py'), ('*', '.exe')])
        for path in paths:
            if path not in self.selected_bots:
                self.selected_bots.append(path)
        s = 'Выбранные боты:\n' + '\n'.join([bot.split('/')[-1] for bot in sorted(self.selected_bots)])
        self.selected_bots_text.configure(state='normal')
        self.selected_bots_text.delete('1.0', END)
        self.selected_bots_text.replace(0.0, 1.0, s)
        self.selected_bots_text.configure(state='disabled')
        if self.selected_game_name and len(self.selected_bots) > 1:
            self.start_tournament_bt.configure(state="normal")
        else:
            self.start_tournament_bt.configure(state="disable")
