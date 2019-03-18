from omok_checker import Omok_checker as checker
from omok_gui import *

class Omok_board():
    """Omok game board engine"""
    def __init__(self, height, width):
        if height < 5 or width < 5:
            raise ValueError("Board size must be greater than 5x5")

        self.lock = 0
        # 0 = waiting (unlocked) // 1 = processing (locked)
        # (for synchronization purposes)

        self.status = 0
        # 0 = black's turn // 1 = white's turn // 2 = white wins // 3 = black wins
        # 4 = draw by white // 5 = draw by black // 6 = tracing

        self.omok_board = []
        # -1 = empty // 0 = black // 1 = white

        self.trace = []
        # trace of all movements made by players

        for i in range(height):
            self.omok_board.append([])
            for j in range(width):
                self.omok_board[i].append(-1)

        self.gui = None

        print("Omok engine loaded")

    def play(self, i, j):
        # return value: -1 = ineffective play or significant error // 0 = normal play
        # 2 = white's win // 3 = black's win // 4 = draw by white
        self.lock = 1
        if self.status == 2:
            print("Game over: white wins!")
            return -1
        elif self.status == 3:
            print("Game over: black wins!")
            return -1
        elif self.status == 4:
            print("Game over: draw!")
            return -1
        elif self.status != 0 and self.status != 1:
            print("Error: status attribute has been inappropriately modified; current status value is %d" % self.status)
            return -1
        elif i < 0 or j < 0 or i >= len(self.omok_board) or j >= len(self.omok_board[0]):
            print("Cannot place piece outside the board range: (%d, %d)" % (i, j))
            return -1
        elif self.omok_board[i][j] != -1:
            print("Cannot place piece on a non-empty spot: (%d, %d) already placed with %d" % (i, j, self.omok_board[i][j]))
            return -1
        elif checker.checkthree(self.omok_board, i, j):
            print("Cannot place piece on a spot that creates three by three placement")
            return -1
        else:
            self.omok_board[i][j] = self.status
            self.trace.append((self.status, i, j))
            print("Placed on (%d, %d) by %s" % (i, j, ("white", "black")[self.status == 0]))
            self.status = 1 - self.status

        if checker.checkdefeat(self.omok_board, i, j):
            self.status += 2
            if self.status == 2:
                print("Game over: white wins!")
                flag = 2
            elif self.status == 3:
                print("Game over: black wins!")
                flag = 3
        elif checker.checkdraw(self.omok_board):
            self.status += 4
            print("Game over: draw!")
            flag = 4
        else:
            flag = 0

        self.__update_gui(1, i, j, flag)
        self.lock = 0
        return flag

    def reset(self):
        self.lock = 1
        for i in range (len(self.omok_board)):
            for j in range(len(self.omok_board[0])):
                self.omok_board[i][j] = -1
        self.status = 0
        print("Omok board has been reset")
        self.__update_gui(0)
        self.lock = 0

    def printboard(self):
        print()
        for i in range (len(self.omok_board)):
            for j in range(len(self.omok_board[0])):
                if self.omok_board[i][j] == -1:
                    print("-", end='')
                else:
                    print(self.omok_board[i][j], end='')
            print()
        print()

    def printtrace(self):
        for i in range(len(self.trace)):
            print("%d: (%d, %d) by %s" % ((i + 1), self.trace[i][1], self.trace[i][2], ("white", "black")[self.trace[i][0] == 0]))

    def load_gui(self, gui):
        self.gui = gui
        print("GUI successfully loaded to game engine")

    def __update_gui(self, action, i=None, j=None, flag=None):
        if self.gui == None:
            return
        if action == 0:
            self.gui.clear()
        elif action == 1:
            self.gui.place(i, j, flag)
