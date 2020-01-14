from tkinter import *

class OLabel(Label):
    """Tkinter Label that contains location (i, j) info"""
    def __init__(self, master, i, j, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.i = i
        self.j = j

class GUI:
    """Omok GUI created with tkinter"""
    statustext = ["Black's turn", "White's turn", "White wins!", "Black wins!", "Draw!"]
    res_path = "omok/res/"
    img_name = ["black", "white", "empty"]
    img_extension = ".gif"

    def __init__(self, windowtitle, board):
        self.board = board
        
        self.window = Tk()
        self.window.title(windowtitle)

        self.img = []

        for i in range(len(GUI.img_name)):
            self.img.append(PhotoImage(file=GUI.res_path + GUI.img_name[i] + GUI.img_extension))

        self.windowheight = len(self.board.board) * self.img[0].height()
        self.windowwidth = len(self.board.board[0]) * self.img[0].width()

        self.window.geometry(str(self.windowwidth) + "x" + str(self.windowheight+20) + "+100+100")
        self.window.resizable(True, True)

        self.labelframe = Frame(self.window, height=20, bd=0)
        self.labelframe.pack(side="top", fill="x")

        self.gameframe = Frame(self.window, bd=0)
        self.gameframe.pack(expand=True, fill="both")

        self.resetbutton = Button(self.labelframe, text="Reset", command=self.onclick2)
        self.resetbutton.pack(side="left", fill="y")

        self.statuslabel = Label(self.labelframe, text=GUI.statustext[board.status], height=1, width=10)
        self.statuslabel.pack(side="right", fill="y")

        self.board_gui = []

        for i in (range(len(self.board.board))):
            self.board_gui.append([])
            for j in (range(len(self.board.board[0]))):
                self.board_gui[i].append(OLabel(self.gameframe, i=i, j=j, 
                                                bd=0, padx=0, pady=0, 
                                                image=self.img[self.board.board[i][j]], height=self.img[0].height(), width=self.img[0].width()))
                self.board_gui[i][j].bind("<Button-1>", self.onclick1)
                self.board_gui[i][j].grid(row=i, column=j)

        self.board.load_gui(self)

        self.window.mainloop()

    def onclick1(self, event):
        self.board.play(event.widget.i, event.widget.j)

    def onclick2(self):
        self.board.reset()

    def place(self, i, j, flag):
        if flag == 0:
            self.statuslabel["text"] = GUI.statustext[self.board.status]
            self.board_gui[i][j]["image"] = self.img[1 - self.board.status]
        elif flag == 2 or flag == 3:
            self.statuslabel["text"] = GUI.statustext[flag]
            self.board_gui[i][j]["image"] = self.img[3 - self.board.status]
        elif flag == 4:
            self.statuslabel["text"] = GUI.statustext[flag]
            self.board_gui[i][j]["image"] = self.img[5 - self.board.status]

    def clear(self):
        self.statuslabel["text"] = GUI.statustext[self.board.status]
        for i in (range(len(self.board.board))):
            for j in (range(len(self.board.board[0]))):
                self.board_gui[i][j]["image"] = self.img[self.board.board[i][j]]
