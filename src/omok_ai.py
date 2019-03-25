import math
import time
from threading import Thread
from omok_board import Omok_board

class Omok_ai:
    """Omok AI based on alpha-beta pruning algorithm"""
    # TODO: fix errors, implement machine learning to improve AI
    cnt = 0
    evaltime = 0
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
        depth = 2
        area = 3
        decision = Omok_ai.alphabeta(board, depth, area, -math.inf, math.inf, (True, False)[board.status == 0])[1]
        i = decision.trace[-1][1]
        j = decision.trace[-1][2]
        print("took " + str(Omok_ai.cnt) + " evaluations")
        print("each eval takes average of " + str(Omok_ai.evaltime / Omok_ai.cnt) + " seconds")
        Omok_ai.cnt = 0
        return (i, j)

    @staticmethod
    def alphabeta(node, depth, area, a, b, maximizing):
        if depth == 0 or node.status == 2 or node.status == 3 or node.status == 4 or node.status == 5:
            return (Omok_ai.evaluateboard(node), None)
        goodchild = None
        if maximizing:
            for child in Omok_ai.nextmoveiterator(node, area):
                childvalue = Omok_ai.alphabeta(child, depth - 1, area, a, b, False)[0]
                if a < childvalue:
                    goodchild = child
                    a = childvalue
                if a >= b:
                    break
            return (a, goodchild)
        else:
            for child in Omok_ai.nextmoveiterator(node, area):
                childvalue = Omok_ai.alphabeta(child, depth - 1, area, a, b, True)[0]
                if b > childvalue:
                    goodchild = child
                    b = childvalue
                if a >= b:
                    break
            return (b, goodchild)

    @staticmethod
    def nextmoveiterator(board, area):
        """Iterates every possible next move in given area"""
        possibilities = set({})
        check = False

        for i in range(len(board.omok_board)):
            for j in range(len(board.omok_board[0])):
                if board.omok_board[i][j] == 0 or board.omok_board[i][j] == 1:
                    check = True
                    for k in range(i - area, i + area + 1):
                        for l in range(j - area, j + area + 1):
                            if k >= 0 and k < len(board.omok_board):
                                if l >= 0 and l < len(board.omok_board[0]):
                                    if board.omok_board[k][l] == -1:
                                        possibilities.add((k, l))

        if not check:
            possibilities.add((math.floor(len(board.omok_board) / 2), math.floor(len(board.omok_board[0]) / 2)))

        for position in possibilities:
            newboard = board.duplicate()
            newboard.play(position[0], position[1])
            yield newboard

    @staticmethod
    def evaluateboard(board):
        """
        Returns a value that represents the advantageousness of current board status
        Smaller value denotes the board is more in favor of black, and vice versa

        Evaluation is based on
        1. How many 5-in-a-row is achievable in current state
        2. For each achievable 5-in-a-row,
            a. How many stones are already placed
            b. Whether it is achievable both ways
            c. How much blockage is present and how close they are
        """
        start = time.time()
        boardvalue = 0

        for i in range(len(board.omok_board)):
            for j in range(len(board.omok_board[0])):
                if board.omok_board[i][j] == 0 or board.omok_board[i][j] == 1:
                    boardvalue += Omok_ai.evaluatepoint(board, i, j)
        Omok_ai.cnt += 1
        end = time.time()
        Omok_ai.evaltime += end - start
        return boardvalue

    @staticmethod
    def evaluatepoint(board, i, j):
        """
        Returns a value that represents the advantageousness of current point
        Smaller value denotes the point is more in favor of black, and vice versa

        Evaluation is based on
        1. How many 5-in-a-row is achievable at current point
        2. For each achievable 5-in-a-row,
            a. How many stones are already placed
            b. Whether it is achievable both ways
            c. How much blockage is present and how close they are

        Note that dir value refers to the following:
        1 = diagonal (left top to right bottom)
        2 = vertical
        3 = diagonal (right top to left bottom)
        4 = horizontal
        """
        pointvalue = 0

        for dir in range(1, 5):
            pointvalue += Omok_ai.evaluateline(board, i, j, dir)

        return pointvalue

    @staticmethod
    def evaluateline(board, i, j, dir):
        """
        Returns a value that represents the advantageousness of current 9-space line
        Smaller value denotes the line is more in favor of black, and vice versa

        Evaluation is based on
        1. Whether a 5-in-a-row is achievable in current line, and if so,
            a. How many stones are already placed
            b. Whether it is achievable both ways
            c. How much blockage is present and how close they are

        Note that dir value refers to the following:
        1 = diagonal (left top to right bottom)
        2 = vertical
        3 = diagonal (right top to left bottom)
        4 = horizontal
        """
        if dir != 1 and dir != 2 and dir != 3 and dir != 4:
            raise ValueError("Wrong dir value")

        linevalue = 0
        color = board.omok_board[i][j]
        weight = (-1, 1)[color == 1]

        dir1 = (-1, -1)
        dir2 = (1, 1)

        dir1count = [0, 0, 0]
        dir2count = [0, 0, 0]
        # [number of identical stones in row in next 4 spaces until blockage,
        #  number of identical stones in next 4 spaces until blockage,
        #  number of empty spots in next 4 spaces until blockage]
        # 00--1  --> [1, 2] (supposing that the first 0 is the origin)
        # 0-01-  --> [1, 1]
        # 010--  --> [0, 0]

        if dir == 2:
            dir1 = (-1, 0)
            dir2 = (1, 0)
        elif dir == 3:
            dir1 = (-1, 1)
            dir2 = (1, -1)
        elif dir == 4:
            dir1 = (0, 1)
            dir2 = (0, -1)

        inrow = True

        for movement in range(1, 5):
            if i + dir1[0] * movement < 0 or i + dir1[0] * movement >= len(board.omok_board):
                break
            if j + dir1[1] * movement < 0 or j + dir1[1] * movement >= len(board.omok_board[0]):
                break
            if board.omok_board[i + dir1[0] * movement][j + dir1[1] * movement] == color:
                if inrow:
                    dir1count[0] += 1
                else:
                    dir1count[1] += 1
            elif board.omok_board[i + dir1[0] * movement][j + dir1[1] * movement] == -1:
                inrow = False
                dir1count[2] += 1
            else:
                break
        for movement in range(1, 5):
            if i + dir2[0] * movement < 0 or i + dir2[0] * movement >= len(board.omok_board):
                break
            if j + dir2[1] * movement < 0 or j + dir2[1] * movement >= len(board.omok_board[0]):
                break
            if board.omok_board[i + dir2[0] * movement][j + dir2[1] * movement] == color:
                if inrow:
                    dir2count[0] += 1
                else:
                    dir2count[1] += 1
            elif board.omok_board[i + dir2[0] * movement][j + dir2[1] * movement] == -1:
                inrow = False
                dir2count[2] += 1
            else:
                break

        count = (1 + dir1count[0] + dir2count[0], 1 + dir1count[1] + dir2count[1], dir1count[2] + dir2count[2])

        # TODO: implement proper values
        if count[1] + count[2] < 5:
            return 0
        elif count[0] == 5:
            return 10000 * weight
        elif count[0] == 4:
            if dir1count[2] >= 1 and dir2count[2] >= 1:
                return 10000 * weight
            elif count[2] >= 1:
                return 50 * weight
            else:
                return 0
        elif count[0] == 3:
            return 4 * count[1] * count[2] * weight
        elif count[0] == 2:
            return 2 * count[1] * count[2] * weight
        else:
            return count[1] * count[2] * weight
