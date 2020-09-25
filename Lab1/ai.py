import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
SEARCH_DEPTH = 15
random.seed(time.time())


# don't change the class name
def shift_i(x, y, drc):
    return x + drc[0], y + drc[1]


def adv_color(color):
    return 0 - color


class AI(object):
    drc = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    CORNER_WEIGHT = 10
    STAR_WEIGHT = -10

    # pnt = [[10, -5, 4, 3, 3, 4, -5, 10],
    #        [-5, -10, 0, 0, 0, 0, -10, -5],
    #        [4, 0, 0, 0, 0, 0, 0, 4],
    #        [3, 0, 0, 0, 0, 0, 0, 3],
    #        [3, 0, 0, 0, 0, 0, 0, 3],
    #        [4, 0, 0, 0, 0, 0, 0, 4],
    #        [-5, -10, 0, 0, 0, 0, -10, -5],
    #        [10, -5, 4, 3, 3, 4, -5, 10]]

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

    def rev_drc(self, i):
        return self.drc[(i + 4) % 8]

    def is_inboard(self, x, y):
        return 0 <= x < self.chessboard_size and 0 <= y < self.chessboard_size

    def is_valid(self, chessboard, color, x, y):
        check = False
        for drc in self.drc:
            ix, iy = shift_i(x, y, drc)
            if self.is_inboard(ix, iy) and chessboard[ix][iy] == adv_color(color):
                while self.is_inboard(ix, iy) and chessboard[ix][iy] == adv_color(color):
                    ix, iy = shift_i(ix, iy, drc)
                if self.is_inboard(ix, iy) and chessboard[ix][iy] == color:
                    check = True
                    break
        return check

    def get_valid_moves(self, chessboard, color):
        valid_moves = []
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for x, y in idx:
            if self.is_valid(chessboard, color, x, y):
                valid_moves.append((x, y))
        return valid_moves

    def move(self, chessboard, color, x, y):
        # cnt = 0
        chessboard[x][y] = color
        for i in range(0, len(self.drc)):
            ix, iy = shift_i(x, y, self.drc[i])
            if self.is_inboard(ix, iy) and chessboard[ix][iy] == adv_color(color):
                while self.is_inboard(ix, iy) and chessboard[ix][iy] == adv_color(color):
                    ix, iy = shift_i(ix, iy, self.drc[i])
                if self.is_inboard(ix, iy) and chessboard[ix][iy] == color:
                    while self.is_inboard(ix, iy) and (ix, iy) != (x, y):
                        chessboard[ix][iy] = color
                        # cnt = cnt + 1
                        ix, iy = shift_i(ix, iy, self.rev_drc(i))
        return chessboard

    def position_value(self, chessboard, color):
        value = 0
        lim = self.chessboard_size
        value = value + \
                self.CORNER_WEIGHT * color * chessboard[0][0] + \
                self.CORNER_WEIGHT * color * chessboard[0][lim - 1] + \
                self.CORNER_WEIGHT * color * chessboard[lim - 1][0] + \
                self.CORNER_WEIGHT * color * chessboard[lim - 1][lim - 1] + \
                self.STAR_WEIGHT * color * chessboard[1][1] + \
                self.STAR_WEIGHT * color * chessboard[1][lim - 2] + \
                self.STAR_WEIGHT * color * chessboard[lim - 2][1] + \
                self.STAR_WEIGHT * color * chessboard[lim - 2][lim - 2]
        return value

    def stablize_bin_board(self, chessboard, bin_board, color, sx, sy):
        if chessboard[sx][sy] == color:
            bin_board[sx][sy] = True
            for dx, dy in self.drc:
                x, y = sx, sy
                while self.is_inboard(x, y) and chessboard[x][y] == color:
                    bin_board[x][y] = True
                    x = x + dx
                    y = y + dy
        return bin_board

    def count_stable(self, chessboard, color):
        bin_board = np.zeros((self.chessboard_size, self.chessboard_size), dtype=bool)
        lim = self.chessboard_size

        sx, sy = 0, 0
        self.stablize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = 0, lim - 1
        self.stablize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = lim - 1, 0
        self.stablize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = lim - 1, lim - 1
        self.stablize_bin_board(chessboard, bin_board, color, sx, sy)

        # print(bin_board)
        value = 0
        for i in bin_board:
            for j in i:
                if j:
                    value = value + 1
        return value

    def h(self, chessboard, color):
        valid_moves = self.get_valid_moves(chessboard, color)
        mobility_value = len(valid_moves)
        stable_value = self.count_stable(chessboard, color)
        position_value = self.position_value(chessboard, color)
        # print(mobility_value, stable_value, position_value)
        total_value = mobility_value + 0 * stable_value + 10 * position_value
        return total_value, valid_moves

    def minimax_search(self, chessboard, color, depth, beta):
        value, valid_moves = self.h(chessboard, color)

        if len(valid_moves) == 0 or depth == 0:
            return value

        best_move = None
        alpha = float('-inf')
        for x, y in valid_moves:
            temp_chessboard = self.move(chessboard, color, x, y)
            tv = -self.minimax_search(temp_chessboard, adv_color(color), depth - 1, -alpha)
            # if depth == SEARCH_DEPTH:
            #     print(tv, (x, y))
            if tv > alpha:
                alpha = tv
                best_move = (x, y)
                if alpha >= beta:
                    break

        if depth == SEARCH_DEPTH and best_move:
            self.candidate_list.append(best_move)
            # print(alpha, best_move)

        return alpha

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        self.candidate_list = self.get_valid_moves(chessboard, self.color)
        # if len(self.candidate_list) > 0:
        #     rd = random.choice(self.candidate_list)
        #     self.candidate_list.append(rd)
        self.minimax_search(chessboard, self.color, SEARCH_DEPTH, float('inf'))
        print(self.candidate_list)

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candidate_list,
        # we will choose the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return a empty list.
