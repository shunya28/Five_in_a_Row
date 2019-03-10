from omok_board import *
from omok_gui import *

boardheight = 25
boardwidth = 25
windowtitle = "Omok"

board = Omok_board(boardheight, boardwidth)
board_gui = Omok_gui(windowtitle, board)
board.load_gui(board_gui)
