from tkinter import *

class Omok_gui:
    """Sets omok gui using tkinter and contains board status"""
    window_title = "Omok"
    window_width = 500
    turn_text = ["Black's turn", "White's turn", "Black wins!", "White wins!"]
    res_path = "../res/"
    img_name = ["black", "white", "empty"]
    img_extension = ".gif"

    def __init__(self):
        self.turn = 0

        self.window = Tk()
        self.window.title(Omok_gui.window_title)
        self.window.geometry(str(Omok_gui.window_width) + "x" + str(Omok_gui.window_width+20) + "+100+100")
        self.window.resizable(False, False)

        self.label_frame = Frame(self.window, bd=0)
        self.label_frame.pack(side="top", fill="x")

        self.game_frame = Frame(self.window, bd=0)
        self.game_frame.pack(expand=True, fill="both")

        self.reset_button = Button(self.label_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", fill="y")

        self.turn_label = Label(self.label_frame, text=Omok_gui.turn_text[self.turn], height=1, width=10)
        self.turn_label.pack(side="right", fill="y")

        self.img = []

        for i in range(len(Omok_gui.img_name)):
            self.img.append(PhotoImage(file=Omok_gui.res_path + Omok_gui.img_name[i] + Omok_gui.img_extension))

        self.board = []
        self.board_size = int(Omok_gui.window_width/self.img[0].width())

        for i in (range(self.board_size)):
            self.board.append([])
            for j in (range(self.board_size)):
                self.board[i].append(Label(self.game_frame, text = "2", image=self.img[2], height=self.img[0].height(), width=self.img[0].width(), bd=0, padx=0, pady=0))
                self.board[i][j].bind("<Button-1>", self.onclick)
                self.board[i][j].grid(row=i, column=j)

        #window.mainloop()

    def onclick(self, event):
        event.widget["text"] = str(self.turn)
        event.widget["image"] = self.img[self.turn]
        event.widget.bind("<Button-1>", self.disable)
        self.turn = 1 - self.turn
        self.turn_label["text"] = Omok_gui.turn_text[self.turn]

    def disable(self, event):
        pass

    def reset(self):
        self.turn = 0
        self.turn_label["text"] = Omok_gui.turn_text[self.turn]
        for i in (range(self.board_size)):
            for j in (range(self.board_size)):
                self.board[i][j]["text"] = "2"
                self.board[i][j]["image"] = self.img[2]
                self.board[i][j].bind("<Button-1>", self.onclick)

omok = Omok_gui()
