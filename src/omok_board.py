from omok_checker import Omok_checker as checker

class Omok_board():
    """Omok game board"""
    def __init__(self, board_height, board_width):
        if board_height < 5 or board_width < 5:
            raise ValueError("Board size must be greater than 5x5")

        self.turn = 0 # 0 = black's turn // 1 = white's turn // 2 = white wins // 3 = black wins // 4 = draw

        self.omok_board = [] # -1 = empty // 0 = black // 1 = white

        for i in range(board_height):
            self.omok_board.append([])
            for j in range(board_width):
                self.omok_board[i].append(-1)

    def play(self, i, j): # returns 0 for ineffective play, -1 for significant error, 1 for normal play, 2 for white's win, 3 for black's win, and 4 for draw
        if self.turn == 2:
            print("Game over: white wins!")
            return 0
        elif self.turn == 3:
            print("Game over: black wins!")
            return 0
        elif self.turn == 4:
            print("Game over: draw!")
            return 0
        elif self.turn != 0 and self.turn != 1:
            print("Error: turn attribute has been inappropriately modified; current turn value is %d" % self.turn)
            return -1
        elif i < 0 or j < 0 or i >= len(self.omok_board) or j >= len(self.omok_board[0]):
            print("Cannot place piece outside the board range: (%d, %d)" % (i, j))
            return 0
        elif self.omok_board[i][j] != -1:
            print("Cannot place piece on a non-empty spot: (%d, %d) already placed with %d" % (i, j, self.omok_board[i][j]))
            return 0
        elif checker.checkthree(self.omok_board, i, j):
            print("Cannot place piece on a spot that creates three by three placement")
            return 0
        else:
            self.omok_board[i][j] = self.turn
            self.turn = 1 - self.turn

        if checker.checkdefeat(self.omok_board, i, j):
            self.turn += 2
            if self.turn == 2:
                print("Game over: white wins!")
                return 2
            elif self.turn == 3:
                print("Game over: black wins!")
                return 3
        elif checker.checkdraw(self.omok_board):
            self.turn = 4
            print("Game over: draw!")
            return 4
        else:
            return 1

    def resetboard(self):
        for i in range (len(self.omok_board)):
            for j in range(len(self.omok_board[0])):
                self.omok_board[i][j] = -1
        self.turn = 0

    def printboard(self):
        for i in range (len(self.omok_board)):
            for j in range(len(self.omok_board[0])):
                if self.omok_board[i][j] == -1:
                    print("-", end='')
                else:
                    print(self.omok_board[i][j], end='')
            print()
