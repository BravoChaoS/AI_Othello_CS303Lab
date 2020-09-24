import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
def shift_i(x, y, drc):
    return x + drc[0], y + drc[1]


class AI(object):

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size

        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your
        # decision .
        self.candidate_list = []
        self.drc = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def is_inboard(self, x, y):
        return 0 <= x < self.chessboard_size and 0 <= y < self.chessboard_size

    def is_valid(self, chessboard, x, y):
        check = False
        for drc in self.drc:
            ix, iy = shift_i(x, y, drc)
            if self.is_inboard(ix, iy) and chessboard[ix][iy] == 0 - self.color:
                while self.is_inboard(ix, iy) and chessboard[ix][iy] == 0 - self.color:
                    ix, iy = shift_i(ix, iy, drc)
                if self.is_inboard(ix, iy) and chessboard[ix][iy] == self.color:
                    check = True
                    break
        return check

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for x, y in idx:
            if self.is_valid(chessboard, x, y):
                self.candidate_list.append((x, y))
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candidate_list,
        # we will choose the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return a empty list.
