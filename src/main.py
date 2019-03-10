from omok_board import *
from omok_gui import *
import time

windowtitle = "Omok"
boardheight = 25
boardwidth = 25

board = Omok_board(boardheight, boardwidth)
board_gui = Omok_gui(windowtitle, board)
board.load_gui(board_gui)
