from threading import Lock
from omok.core.rules import Rules
from omok.core.traces import Traces

import random

class Board:
    """Omok game board engine"""
    EMPTY_SLOT = '-' # These three variables must be single character
    BLACK_SLOT = 'B'
    BLACK90_SLOT = 'B90'
    BLACK70_SLOT = 'B70'
    WHITE_SLOT = 'W'
    WHITE10_SLOT = 'W10'
    WHITE30_SLOT = 'W30'

    BLACK_TURN = 10
    BLACK_WIN = 11
    BLACK_MEASURED = 12
    WHITE_TURN = 20
    WHITE_WIN = 21
    WHITE_MEASURED = 22
    DRAW = 30

    INVALID_CALL = 40

    STONE_BLACK90 = 50
    STONE_BLACK70 = 51
    STONE_WHITE30 = 52
    STONE_WHITE10 = 53

    INIT_STATUS = BLACK_TURN
    INIT_STONE_STATUS = STONE_BLACK90

    MAX_MEASUREMENT = 5

    def __init__(self, width=16, height=10, silent=False):
        if height < 5 or width < 5:
            raise ValueError('Board size must be greater than 5x5')
        self.width = width
        self.height = height
        self.silent = silent # if True, blocks all CLI messages
        self.board = None
        self.board_before_measurement = None
        self.empty_slots = None
        self.traces = None
        self.status = None
        self.status_before_measurement = None
        self.stone_status = None
        self.prev_black_stone_status = None
        self.prev_white_stone_status = None
        self.n_black_measurement = 0
        self.n_white_measurement = 0
        self.gui = None
        self.lock = Lock()
        self.reset()
        self.print('Omok engine loaded')

    def __str__(self):
        board_str  = '\nBoard Status: ' + str(self.status)
        board_str += '\nGUI: ' + str(self.gui)
        board_str += '\nSilence Mode: ' + str(self.silent)
        board_str += '\nCurrent State:'
        board_str += self.__repr__()
        return board_str

    def __repr__(self):
        board_repr = '\n'
        for i in range (self.height):
            for j in range(self.width):
                board_repr += self.board[i][j]
            board_repr += '\n'
        board_repr += '\n'
        return board_repr

    def reset(self):
        if not self.lock.acquire(False):
            self.print('Omok board is currently locked')
            return
        self.board = []
        self.empty_slots = set()
        for i in range (self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(Board.EMPTY_SLOT)
                self.empty_slots.add((i, j))
        self.traces = Traces()
        self.status = Board.INIT_STATUS
        self.stone_status = Board.INIT_STONE_STATUS
        self.prev_black_stone_status = None
        self.prev_white_stone_status = None
        self.n_black_measurement = 0
        self.n_white_measurement = 0
        self.clear_gui()
        self.print('Omok board has been reset')
        self.lock.release()

    def _measure_stone(self, board_stat):
        r = random.random()
        if board_stat == Board.EMPTY_SLOT:
            return Board.EMPTY_SLOT
        elif board_stat == Board.BLACK90_SLOT:
            return Board.BLACK_SLOT if r < 0.9 else Board.WHITE_SLOT
        elif board_stat == Board.BLACK70_SLOT:
            return Board.BLACK_SLOT if r < 0.7 else Board.WHITE_SLOT
        elif board_stat == Board.WHITE30_SLOT:
            return Board.BLACK_SLOT if r < 0.3 else Board.WHITE_SLOT
        elif board_stat == Board.WHITE10_SLOT:
            return Board.BLACK_SLOT if r < 0.1 else Board.WHITE_SLOT
        else:
            raise ValueError(f'Invalid board status: {board_stat}')

    def measurement(self):
        if not self.lock.acquire(False):
            self.print('Omok board is currently locked')
            return

        # save current status and board
        self.status_before_measurement = self.status
        self.board_before_measurement = self.board

        self.print('Measuring quantum stones...')

        # NOTE: be careful that the status will be WHITE_MEASURED when BLACK_TURN, and vice versa
        if self.status == Board.BLACK_TURN:
            self.status = Board.WHITE_MEASURED
            self.n_white_measurement += 1
        else:
            assert self.status == Board.WHITE_TURN
            self.status = Board.BLACK_MEASURED
            self.n_black_measurement += 1

        measured_board = []
        for i in range(self.height):
            measured_board.append([])
            for j in range(self.width):
                measured_board[i].append(self._measure_stone(self.board[i][j]))

        self.board = measured_board
        self.update_gui(i=None, j=None)  # set i, j to None to update all slots

        defeat_flag = False
        for i in range(self.height):  # TODO: replace this with a more efficient algorithm
            for j in range(self.width):
                if Rules.is_defeat(measured_board, i, j):
                    defeat_flag = True

                    # NOTE: note that if draw occurs, the player who measured the board wins
                    if self.status == Board.BLACK_MEASURED:
                        self.print('Game over: black wins!')
                        self.status = Board.BLACK_WIN
                    else:
                        assert self.status == Board.WHITE_MEASURED
                        self.print('Game over: white wins!')
                        self.status = Board.WHITE_WIN
                    break
            if defeat_flag:
                break

        if not defeat_flag:
            self.print('Measurement complete')

            # NOTE: Though implemented this way, there is no explicit definition of the rule when both players are no longer be able to measure.
            if self.n_black_measurement >= Board.MAX_MEASUREMENT and self.n_white_measurement >= Board.MAX_MEASUREMENT:
                self.print('Game over: draw!')
                self.status = Board.DRAW

        # update gui when game is over to disable all buttons besides reset button
        if self.status == Board.BLACK_WIN or self.status == Board.WHITE_WIN or self.status == Board.DRAW:
            self.update_gui(i=0, j=0)

        self.lock.release()

    def restoration(self):
        if not self.lock.acquire(False):
            self.print('Omok board is currently locked')
            return

        self.status = self.status_before_measurement
        self.board = self.board_before_measurement
        self.status_before_measurement = None
        self.board_before_measurement = None

        self.update_gui(i=None, j=None)  # set i, j to None to update all slots
        self.print('Stones has been restored to premeasurement state')
        self.lock.release()

    def change_stone_status(self):
        if not self.lock.acquire(False):
            self.print('Omok board is currently locked')
            return

        # switch stone status
        if self.status == Board.BLACK_TURN:
            if self.stone_status == Board.STONE_BLACK90:
                self.stone_status = Board.STONE_BLACK70
            else:
                assert self.stone_status == Board.STONE_BLACK70
                self.stone_status = Board.STONE_BLACK90
        else:
            assert self.status == Board.WHITE_TURN
            if self.stone_status == Board.STONE_WHITE30:
                self.stone_status = Board.STONE_WHITE10
            else:
                assert self.stone_status == Board.STONE_WHITE10
                self.stone_status = Board.STONE_WHITE30

        self.update_gui(0, 0)  # NOTE: no meaning in setting i, j to 0, 0
        self.print(f'Stone status has been changed to {self.stone_status}')
        self.lock.release()

    def place(self, i, j):
        if not self.lock.acquire(False):
            self.print('Omok board is currently locked')
            return Board.INVALID_CALL
        if not self.is_valid_slot(i, j):
            self.lock.release()
            return Board.INVALID_CALL

        if self.status == Board.BLACK_TURN:
            if self.stone_status == Board.STONE_BLACK90:
                self.board[i][j] = Board.BLACK90_SLOT
            else:
                assert self.stone_status == Board.STONE_BLACK70
                self.board[i][j] = Board.BLACK70_SLOT
            self.prev_black_stone_status = self.stone_status
        else:
            assert self.status == Board.WHITE_TURN
            if self.stone_status == Board.STONE_WHITE30:
                self.board[i][j] = Board.WHITE30_SLOT
            else:
                assert self.stone_status == Board.STONE_WHITE10
                self.board[i][j] = Board.WHITE10_SLOT
            self.prev_white_stone_status = self.stone_status

        self.empty_slots.remove((i, j))
        self.traces.push(self.board[i][j], i, j)
        self.print(self.traces.format_trace(self.traces.size(), self.traces.peek()))

        if len(self.empty_slots) == 0:
            self.print('Game over: draw!')
            self.status = Board.DRAW
        else:
            self.status = Board.BLACK_TURN if (self.status == Board.WHITE_TURN) else Board.WHITE_TURN

            # set default stone status considering if the player can use strong stone
            if self.status == Board.BLACK_TURN:
                self.stone_status = Board.STONE_BLACK90 if Rules.can_use_strong_stone(self) else Board.STONE_BLACK70
            else:
                assert self.status == Board.WHITE_TURN
                self.stone_status = Board.STONE_WHITE10 if Rules.can_use_strong_stone(self) else Board.STONE_WHITE30

        self.update_gui(i, j)
        self.lock.release()
        return self.status
    
    def is_valid_slot(self, i, j):
        if self.status == Board.BLACK_WIN or self.status == Board.WHITE_WIN:
            self.print('Game over: ' + ('black' if (self.status == Board.BLACK_WIN) else 'white') + ' wins!')
            return False
        elif self.status == Board.DRAW:
            self.print('Game over: draw!')
            return False
        elif i < 0 or j < 0 or i >= self.height or j >= self.width:
            self.print('Cannot place piece outside the board range: ({}, {})'.format(i, j))
            return False
        elif self.board[i][j] != Board.EMPTY_SLOT:
            self.print('Cannot place piece on a non-empty spot: ({}, {}) already placed with {}'.format(i, j, self.board[i][j]))
            return False
        elif Rules.is_three(self.board, i, j):
            self.print('Cannot place piece on a spot that creates three by three condition')
            return False
        elif self.status == Board.BLACK_TURN or self.status == Board.WHITE_TURN:
            return True
        else:
            self.print('Invalid status code {}'.format(self.status))
            return False

    def load_gui(self, gui):
        self.gui = gui
        self.print('GUI successfully loaded to game engine')

    def update_gui(self, i, j):
        if self.gui != None:
            self.gui.update(i=i, j=j)

    def clear_gui(self):
        if self.gui != None:
            self.gui.update()

    def print(self, message, end='\n'):
        if not self.silent:
            print(message, end=end)