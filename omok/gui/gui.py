from tkinter import Tk, Frame, Label, Button, PhotoImage
from omok.core.board import Board
from omok.gui.omokslot import OmokSlot
from omok.core.rules import Rules

class GUI:
    """Omok GUI created with tkinter"""
    status_text = {Board.BLACK_TURN: "Black's turn",
                   Board.BLACK_WIN: 'Black wins!',
                   Board.BLACK_MEASURED: 'Black measured',
                   Board.WHITE_TURN: "White's turn",
                   Board.WHITE_WIN: 'White wins!',
                   Board.WHITE_MEASURED: "White measured",
                   Board.DRAW: 'Draw!'}
    stone_status_text = {Board.STONE_BLACK90: "Stone: 90",
                         Board.STONE_BLACK70: "Stone: 70",
                         Board.STONE_WHITE30: "Stone: 30",
                         Board.STONE_WHITE10: "Stone: 10"}
    res_path = 'omok/res/'
    img_name = {Board.EMPTY_SLOT: 'empty.gif',
                Board.BLACK_SLOT: 'black.gif',
                Board.BLACK90_SLOT: 'black90.gif',
                Board.BLACK70_SLOT: 'black70.gif',
                Board.WHITE_SLOT: 'white.gif',
                Board.WHITE10_SLOT: 'white10.gif',
                Board.WHITE30_SLOT: 'white30.gif'}

    def __init__(self, board, windowtitle='Quantum Gomoku'):
        self.board = board
        self.board.lock.acquire()
        
        self.window = Tk()
        self.window.title(windowtitle)

        self.img = {}
        for key, name in GUI.img_name.items():
            self.img[key] = PhotoImage(file=GUI.res_path + name)

        self.windowheight = self.board.height * self.img[Board.EMPTY_SLOT].height()
        self.windowwidth = self.board.width * self.img[Board.EMPTY_SLOT].width()

        self.window.geometry(str(self.windowwidth) + 'x' + str(self.windowheight+20) + '+100+100')
        self.window.resizable(True, True)

        self.labelframe = Frame(self.window, height=20, bd=0)
        self.labelframe.pack(side='top', fill='x')

        self.resetbutton = Button(self.labelframe, text='Reset', command=self.board.reset)
        self.resetbutton.pack(side='left', fill='y')

        self.statuslabel = Label(self.labelframe, text=GUI.status_text[self.board.status], height=1, width=13)
        self.statuslabel.pack(side='right', fill='y')

        self.stonestatuslabel = Label(self.labelframe, text=GUI.stone_status_text[self.board.stone_status], height=1, width=10)
        self.stonestatuslabel.pack(side='right', fill='y')

        self.changestonestatusbutton = Button(self.labelframe, text='Change Stone', command=self.board.change_stone_status)
        self.changestonestatusbutton.pack(side='right', fill='y')

        measurement_label_text = 'Measurement remaining: Black ' + str(self.board.MAX_MEASUREMENT) + ' / White ' + str(self.board.MAX_MEASUREMENT)
        self.measurementlabel = Label(self.labelframe, text=measurement_label_text, height=1, width=35)
        self.measurementlabel.pack(side='right', fill='y')

        self.restorationbutton = Button(self.labelframe, text='Restore', command=self.board.restoration, state='disabled')
        self.restorationbutton.pack(side='right', fill='y')

        self.measurementbutton = Button(self.labelframe, text='Measure', command=self.board.measurement)
        self.measurementbutton.pack(side='right', fill='y')

        self.gameframe = Frame(self.window, bd=0)
        self.gameframe.pack(expand=True, fill='both')

        self.board_gui = []
        for i in range(self.board.height):
            self.board_gui.append([])
            for j in range(self.board.width):
                self.board_gui[i].append(OmokSlot(self.gameframe, i=i, j=j, bd=0, padx=0, pady=0, 
                                                  image=self.img[self.board.board[i][j]], 
                                                  height=self.img[self.board.board[i][j]].height(), 
                                                  width=self.img[self.board.board[i][j]].width()))
                self.board_gui[i][j].bind('<Button-1>', lambda x: self.board.place(x.widget.i, x.widget.j))
                self.board_gui[i][j].grid(row=i, column=j)

        self.board.load_gui(self)
        self.board.lock.release()
        self.window.mainloop()

    def update(self, i=None, j=None):
        self.statuslabel['text'] = GUI.status_text[self.board.status]
        self.stonestatuslabel['text'] = GUI.stone_status_text[self.board.stone_status]
        self.changestonestatusbutton['state'] = 'normal' if Rules.can_use_strong_stone(self.board) else 'disabled'
        self.measurementbutton['state'] = 'normal'
        self.restorationbutton['state'] = 'disabled'

        black_remaining_measurement = self.board.MAX_MEASUREMENT - self.board.n_black_measurement
        white_remaining_measurement = self.board.MAX_MEASUREMENT - self.board.n_white_measurement
        self.measurementlabel['text'] = 'Measurement remaining: Black ' + str(black_remaining_measurement) + ' / White ' + str(white_remaining_measurement)

        # NOTE: be careful that the status will be WHITE_MEASURED when BLACK_TURN, and vice versa
        if (black_remaining_measurement <= 0 and self.board.status == Board.WHITE_TURN) \
                or (white_remaining_measurement <= 0 and self.board.status == Board.BLACK_TURN):
            self.measurementbutton['state'] = 'disabled'
        else:  # when current player can measure
            if self.board.status == Board.BLACK_MEASURED or self.board.status == Board.WHITE_MEASURED:
                self.restorationbutton['state'] = 'normal'
                self.measurementbutton['state'] = 'disabled'

        # disable all button besides reset button when game is over
        if self.board.status == Board.BLACK_WIN or self.board.status == Board.WHITE_WIN or self.board.status == Board.DRAW:
            self.changestonestatusbutton['state'] = 'disabled'
            self.measurementbutton['state'] = 'disabled'
            self.restorationbutton['state'] = 'disabled'

        if i == None or j == None:
            for i in range(self.board.height):
                for j in range(self.board.width):
                    self.board_gui[i][j]['image'] = self.img[self.board.board[i][j]]
        else:
            self.board_gui[i][j]['image'] = self.img[self.board.board[i][j]]