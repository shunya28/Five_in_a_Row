class Rules:
    @staticmethod
    def is_defeat(board, i, j):
        direction1 = Rules.count(board, i, j, -1, -1, board[i][j], 0)
        direction2 = Rules.count(board, i, j, 1, 1, board[i][j], 0)
        if (direction1 + direction2 - 1) == 5:
            return True
        direction1 = Rules.count(board, i, j, -1, 0, board[i][j], 0)
        direction2 = Rules.count(board, i, j, 1, 0, board[i][j], 0)
        if (direction1 + direction2 - 1) == 5:
            return True
        direction1 = Rules.count(board, i, j, -1, 1, board[i][j], 0)
        direction2 = Rules.count(board, i, j, 1, -1, board[i][j], 0)
        if (direction1 + direction2 - 1) == 5:
            return True
        direction1 = Rules.count(board, i, j, 0, 1, board[i][j], 0)
        direction2 = Rules.count(board, i, j, 0, -1, board[i][j], 0)
        if (direction1 + direction2 - 1) == 5:
            return True
        return False

    @staticmethod
    def is_three(board, i, j):
        # TODO: implement checker method for violation of three by three rule
        return False

    @staticmethod
    def count(board, i, j, i_direction, j_direction, player, depth):
        if i < 0 or j < 0 or i >= len(board) or j >= len(board[0]):
            return 0
        elif depth >= 6:
            return 0
        elif (board[i][j] == player):
            return 1 + Rules.count(board, i + i_direction, j + j_direction, 
                                    i_direction, j_direction, player, depth + 1)
        else:
            return 0