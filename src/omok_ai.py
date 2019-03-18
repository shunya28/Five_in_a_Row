import time
from threading import Thread
from omok_board import Omok_board
from omok_checker import Omok_checker as checker

class Omok_ai:
    """AI that plays omok"""
    def __init__(self, board, color):
        if type(board) is not Omok_board or (color != 0 and color != 1):
            raise ValueError("Class constructor must receive valid arguments")

        self.board = board
        self.color = color # 0 = AI plays as black // 1 = AI plays as white
        self.switch = 0 # 0 = AI off // 1 = AI on
        self.thread = None

        print("Omok AI loaded")

        self.start()

    def start(self):
        if self.thread != None:
            print("AI is already running")
            return

        self.switch = 1
        self.thread = Thread(target=self.play)
        self.thread.start()
        print("Omok AI started")

    def stop(self):
        if self.thread == None:
            print("There is no AI running")
            return

        self.switch = 0
        self.thread.join()
        self.thread = None
        print("Omok AI stopped")

    def play(self):
        while self.switch:
            if self.board.lock == 0 and self.board.status == self.color:
                (i, j) = Omok_ai.calculate(self.board)
                print("AI: ", end='')
                self.board.play(i, j)
            else:
                time.sleep(0.1)

    @staticmethod
    def calculate(board):
        i = 0
        j = 0
        return (i, j)
