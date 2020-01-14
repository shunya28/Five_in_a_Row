
def is_defeat(board, i, j):
    a = count(board, i, j, -1, -1, board[i][j])
    b = count(board, i, j, 1, 1, board[i][j])
    if (a + b - 1) == 5:
        return True
    a = count(board, i, j, -1, 0, board[i][j])
    b = count(board, i, j, 1, 0, board[i][j])
    if (a + b - 1) == 5:
        return True
    a = count(board, i, j, -1, 1, board[i][j])
    b = count(board, i, j, 1, -1, board[i][j])
    if (a + b - 1) == 5:
        return True
    a = count(board, i, j, 0, 1, board[i][j])
    b = count(board, i, j, 0, -1, board[i][j])
    if (a + b - 1) == 5:
        return True

    return False

def is_draw(board):
    for i in range (len(board)):
        for j in range(len(board[0])):
            if board[i][j] == -1:
                return False
    return True

def is_three(board, i, j):
    # TODO: implement checker method for violation of the three and three rule
    return False

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != -1:
                return False
    return True

def count(board, i, j, idir, jdir, color):
    if i < 0 or j < 0 or i >= len(board) or j >= len(board[0]):
        return 0
    if (board[i][j] == color):
        return 1 + count(board, i + idir, j + jdir, idir, jdir, color)
    else:
        return 0