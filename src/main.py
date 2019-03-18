from omok_board import *
from omok_gui import *
from omok_ai import *

windowtitle = "Omok"
boardheight = 25
boardwidth = 25

board = Omok_board(boardheight, boardwidth)
ai = Omok_ai(board, 1)
gui = Omok_gui(windowtitle, board)
