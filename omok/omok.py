from omok.ai.ai import AI
from omok.core.board import Board
from omok.gui.gui import GUI

def run():
    boardwidth = 32
    boardheight = 20
    board = Board(width=boardwidth, height=boardheight)
    ai = AI(board)
    ai.load(board.WHITE_TURN)
    ai.start()
    GUI(board)
    ai.stop()
    quit(0)