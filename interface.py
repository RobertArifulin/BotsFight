import tkinter as tk
from tkinter import filedialog as fd
from constants import *
from PIL import ImageTk, Image


class StartWindow(tk.Frame):

    def __init__(self, games: list):
        super().__init__(background=BG_COLOR)

        self.game_label_text = tk.StringVar()
        self.bot_label_text = tk.StringVar()
        self.bot_label_text.set('Выбранные боты:\n')
        self.games = games
        self.selected_game = ""
        self.selected_bots = []
        self.set_ui()

    def set_ui(self):

        # задаются параметры окна
        w = self.master.winfo_screenwidth()
        h = self.master.winfo_screenheight()
        w = w // 2
        h = h // 2
        w = w - W1_MIN_WIDTH // 2
        h = h - W1_MIN_HEIGHT // 2
        self.master.minsize(W1_MIN_WIDTH, W1_MIN_HEIGHT)
        self.master.geometry(f'{W1_MIN_WIDTH}x{W1_MIN_HEIGHT}+{w}+{h}')
        self.master.title("Турнир Машин")
        self.pack(fill=tk.BOTH, expand=True)

        # создание контейнера frame1
        frame1 = tk.Frame(self, background=BG_COLOR)
        frame1.pack(fill=tk.X)

        # создание надписи "Выберете игру"
        request_game_label = tk.Label(frame1, text="Выберете игру", width=15,
                                      font=W1_FONT, background=BG_COLOR, anchor=tk.W)
        request_game_label.pack(side=tk.LEFT, padx=PADX, pady=PADY)

        # создание надписи с именем выбранной игры
        game_label = tk.Label(frame1, text=0, textvariable=self.game_label_text, font=W1_FONT, background=BG_COLOR)
        game_label.pack()

        # создание listbox с играми
        game_listbox = tk.Listbox(frame1, width=30, height=2, font=W1_FONT)
        for game in self.games:
            game_listbox.insert(tk.END, game)
        game_listbox.bind("<<ListboxSelect>>", self.select)

        # создание scrollbar для listbox с играми
        scroll_listbox = tk.Scrollbar(frame1, command=game_listbox.yview)
        scroll_listbox.pack(side=tk.RIGHT, fill=tk.Y, padx=PADX, pady=PADY)
        game_listbox.pack(fill=tk.X, padx=PADX, expand=True)
        game_listbox.config(yscrollcommand=scroll_listbox.set)

        # !!!
        # создание контейнера frame1
        frame2 = tk.Frame(self, background=BG_COLOR)
        frame2.pack(fill=tk.X)

        request_bot_label = tk.Label(frame2, text="Выберете ботов ", width=15,
                                     font=W1_FONT, background=BG_COLOR, anchor=tk.W)
        request_bot_label.pack(side=tk.LEFT, fill=tk.X, padx=PADX, pady=PADY)

        image = Image.open('images/Windows_Explorer_Icon.png')
        image = image.resize((30, 30))
        self.master.win_explorer = ImageTk.PhotoImage(image)

        file_explorer_button = tk.Button(frame2, command=self.file_explorer_button_press,
                                         image=self.master.win_explorer)
        file_explorer_button.pack(side=tk.LEFT, padx=PADX, pady=PADY)

        self.selected_bots_text = tk.Text(frame2, height=5, font=W1_FONT, background=BG_COLOR)
        self.selected_bots_text.insert(1.0, self.bot_label_text.get())

        scroll_text = tk.Scrollbar(frame2, command=self.selected_bots_text.yview)
        scroll_text.pack(side=tk.RIGHT, fill=tk.Y, padx=PADX, pady=PADY)
        self.selected_bots_text.configure(state='disabled', yscrollcommand=scroll_text.set)
        self.selected_bots_text.pack(side=tk.LEFT, padx=PADX, pady=PADY)

    def select(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.game_label_text.set(value)
        self.selected_game = self.game_label_text.get()

    def file_explorer_button_press(self):
        paths = fd.askopenfilenames(filetypes=[('*', '.py'), ('*', '.exe')])
        for path in paths:
            if path not in self.selected_bots:
                self.selected_bots.append(path)
        s = 'Выбранные боты:\n' + '\n'.join([bot.split('/')[-1] for bot in self.selected_bots])
        self.bot_label_text.set(s)
        self.selected_bots_text.configure(state='normal')
        self.selected_bots_text.delete('1.0', tk.END)
        self.selected_bots_text.replace(0.0, 1.0, self.bot_label_text.get())
        self.selected_bots_text.configure(state='disabled')
