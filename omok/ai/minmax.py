from random import random
from time import sleep

class MinMax:
    @staticmethod
    def temp(board):
        while True:
            (i, j) = (int(board.height * random()), int(board.width * random()))
            if board.board[i][j] == board.EMPTY_SLOT:
                sleep(2)
                return i, j
                break

    @staticmethod
    def decide_next_move(board):
        depth = 2
        area = 2
        decision = MinMax.alphabeta(board, depth, area, -math.inf, math.inf, (True, False)[board.status == 0])[1]
        i = decision.trace[-1][1]
        j = decision.trace[-1][2]
        return (i, j)

    @staticmethod
    def alphabeta(node, depth, area, a, b, maximizing):
        if depth == 0 or node.status == 2 or node.status == 3 or node.status == 4 or node.status == 5:
            return (MinMax.evaluateboard(node), None)
        goodchild = None
        if maximizing:
            for child in MinMax.nextmoveiterator(node, area):
                childvalue = MinMax.alphabeta(child, depth - 1, area, a, b, False)[0]
                if a < childvalue:
                    goodchild = child
                    a = childvalue
                if a >= b:
                    break
            return (a, goodchild)
        else:
            for child in MinMax.nextmoveiterator(node, area):
                childvalue = MinMax.alphabeta(child, depth - 1, area, a, b, True)[0]
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

        for i in range(len(board.board)):
            for j in range(len(board.board[0])):
                if board.board[i][j] == 0 or board.board[i][j] == 1:
                    check = True
                    for k in range(i - area, i + area + 1):
                        for l in range(j - area, j + area + 1):
                            if k >= 0 and k < len(board.board):
                                if l >= 0 and l < len(board.board[0]):
                                    if board.board[k][l] == -1:
                                        possibilities.add((k, l))

        if not check:
            possibilities.add((math.floor(len(board.board) / 2), math.floor(len(board.board[0]) / 2)))

        for position in possibilities:
            newboard = board.duplicate()
            newboard.place(position[0], position[1])
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
        boardvalue = 0

        for i in range(len(board.board)):
            for j in range(len(board.board[0])):
                if board.board[i][j] == 0 or board.board[i][j] == 1:
                    boardvalue += MinMax.evaluatepoint(board, i, j)

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
            pointvalue += MinMax.evaluateline(board, i, j, dir)

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

        color = board.board[i][j]
        weight = (-1, 1)[color == 1]

        if dir == 1:
            dir = ((-1, -1), (1, 1))
        elif dir == 2:
            dir = ((-1, 0), (1, 0))
        elif dir == 3:
            dir = ((-1, 1), (1, -1))
        else:
            dir = ((0, 1), (0, -1))

        count = [[0, 0, 0], [0, 0, 0], [1, 1, 0]]
        # outer list:
        # [first direction count, opposite direction count, total count]
        # innter list:
        # [number of identical stones in row in next 4 spaces until blockage,
        #  number of identical stones in next 4 spaces until blockage,
        #  number of empty spots in next 4 spaces until blockage]
        # 00--1  --> [1, 2] (supposing that the first 0 is the origin)
        # 0-01-  --> [1, 1]
        # 010--  --> [0, 0]

        inrow = True

        for dir_index in range(0, 2):
            for movement in range(1, 5):
                if i + dir[dir_index][0] * movement < 0 or i + dir[dir_index][0] * movement >= len(board.board):
                    break
                if j + dir[dir_index][1] * movement < 0 or j + dir[dir_index][1] * movement >= len(board.board[0]):
                    break
                if board.board[i + dir[dir_index][0] * movement][j + dir[dir_index][1] * movement] == color:
                    if inrow:
                        count[dir_index][0] += 1
                    else:
                        count[dir_index][1] += 1
                elif board.board[i + dir[dir_index][0] * movement][j + dir[dir_index][1] * movement] == -1:
                    inrow = False
                    count[dir_index][2] += 1
                else:
                    break

        for count_index in range(0, 3):
            for dir_index in range(0, 2):
                count[2][count_index] += count[dir_index][count_index]

        if count[2][0] + count[2][1] + count[2][2] < 5 or count[2][0] > 5:
            return 0
        elif count[2][0] == 5:
            return 100000000 * weight
        elif count[2][0] == 4:
            if count[0][2] >= 1 and count[0][2] >= 1:
                return 1000000 * weight
            elif count[2][2] >= 1:
                return 1000 * weight
            else:
                return 0
        elif count[2][0] == 3:
            if count[0][2] >= 1 and count[0][2] >= 1:
                return 1000 * weight
            elif count[2][2] >= 1:
                return 100 * weight
            else:
                return 0
        elif count[2][0] == 2:
            if count[0][2] >= 1 and count[0][2] >= 1:
                return 10 * weight
            elif count[2][2] >= 1:
                return 2 * weight
            else:
                return 0
        elif count[2][0] == 1:
            if count[0][2] >= 1 and count[0][2] >= 1:
                return 10 * weight
            elif count[2][2] >= 1:
                return weight
            else:
                return 0
        else:
            return 0
