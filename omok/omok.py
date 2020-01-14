from omok.ai.ai import AI
from omok.core.board import Board
from omok.gui.gui import GUI

def run():
    windowtitle = "Omok"
    boardheight = 20
    boardwidth = 30

    board = Board(boardheight, boardwidth)
    #ai0 = AI(board, 0)
    ai1 = AI(board, 1)
    gui = GUI(windowtitle, board)