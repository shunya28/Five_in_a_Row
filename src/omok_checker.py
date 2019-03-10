class Omok_checker:
    """Checks for conclusion of game or violation of rules"""
    @staticmethod
    def checkdefeat(board, i, j):
        a = Omok_checker.__checkdefeat_r(board, i, j, -1, -1, board[i][j])
        b = Omok_checker.__checkdefeat_r(board, i, j, 1, 1, board[i][j])
        if (a + b - 1) == 5:
            return True
        a = Omok_checker.__checkdefeat_r(board, i, j, -1, 0, board[i][j])
        b = Omok_checker.__checkdefeat_r(board, i, j, 1, 0, board[i][j])
        if (a + b - 1) == 5:
            return True
        a = Omok_checker.__checkdefeat_r(board, i, j, -1, 1, board[i][j])
        b = Omok_checker.__checkdefeat_r(board, i, j, 1, -1, board[i][j])
        if (a + b - 1) == 5:
            return True
        a = Omok_checker.__checkdefeat_r(board, i, j, 0, 1, board[i][j])
        b = Omok_checker.__checkdefeat_r(board, i, j, 0, -1, board[i][j])
        if (a + b - 1) == 5:
            return True

        return False

    @staticmethod
    def __checkdefeat_r(board, i, j, idir, jdir, color):
        if i < 0 or j < 0 or i >= len(board) or j >= len(board[0]):
            return 0
        if (board[i][j] == color):
            return 1 + Omok_checker.__checkdefeat_r(board, i + idir, j + jdir, idir, jdir, color)
        else:
            return 0

    @staticmethod
    def checkdraw(board):
        for i in range (len(board)):
            for j in range(len(board[0])):
                if board[i][j] == -1:
                    return False
        return True

    @staticmethod
    def checkthree(board, i, j):
        # TODO: implement checker method for violation of the three and three rule
        return False
