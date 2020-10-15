import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
SEARCH_DEPTH = 4
SEP1 = 15
SEP2 = 40
random.seed(time.time())


# don't change the class name
def shift_i(x, y, drc, step=1):
    return x + drc[0], y + drc[1]


def adv_color(color):
    return -color


class AI(object):
    drc = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    WEIGHT_CORNER = 0
    WEIGHT_DIFFERENCE = 0
    WEIGHT_STABILITY = 0
    WEIGHT_MOBILITY = 0
    WEIGHT_POSITION = 0
    WEIGHTED_BOARD = [[100, -10, 8, 6, 6, 8, -10, 100],
                      [-10, -25, -4, -4, -4, -4, -25, -10],
                      [8, -4, 6, 4, 4, 6, -4, 8],
                      [6, -4, 4, 0, 0, 4, -4, 6],
                      [6, -4, 4, 0, 0, 4, -4, 6],
                      [8, -4, 6, 4, 4, 6, -4, 8],
                      [-10, -25, -4, -4, -4, -4, -25, -10],
                      [100, -10, 8, 6, 6, 8, -10, 100]]

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
        depth = self.chessboard_size * self.chessboard_size - len(idx)
        return depth, valid_moves

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
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                value = value + self.WEIGHTED_BOARD[i][j] * chessboard[i][j] * color

        if chessboard[0][0] != COLOR_NONE:
            value = value - 2 * self.WEIGHTED_BOARD[1][0] * chessboard[1][0] * color
            value = value - 2 * self.WEIGHTED_BOARD[0][1] * chessboard[0][1] * color
        if chessboard[0][7] != COLOR_NONE:
            value = value - 2 * self.WEIGHTED_BOARD[1][7] * chessboard[1][7] * color
            value = value - 2 * self.WEIGHTED_BOARD[0][6] * chessboard[0][6] * color
        if chessboard[7][0] != COLOR_NONE:
            value = value - 2 * self.WEIGHTED_BOARD[6][0] * chessboard[6][0] * color
            value = value - 2 * self.WEIGHTED_BOARD[7][1] * chessboard[7][1] * color
        if chessboard[7][7] != COLOR_NONE:
            value = value - 2 * self.WEIGHTED_BOARD[7][6] * chessboard[7][6] * color
            value = value - 2 * self.WEIGHTED_BOARD[6][7] * chessboard[6][7] * color

        return value

    @staticmethod
    def difference(chessboard, color):
        ply_cnt = len(np.where(chessboard == color)[0])
        adv_cnt = len(np.where(chessboard == adv_color(color))[0])

        if ply_cnt == 0:
            return -10000
        if adv_cnt == 0:
            return 10000
        return 100 * (ply_cnt - adv_cnt) / (ply_cnt + adv_cnt + 1)

    def stabilize_bin_board(self, chessboard, bin_board, color, sx, sy):
        # todo: bfs
        if chessboard[sx][sy] == color:
            bin_board[sx][sy] = True
            for dx, dy in self.drc:
                x, y = sx, sy
                while self.is_inboard(x, y) and chessboard[x][y] == color:
                    bin_board[x][y] = True
                    x = x + dx
                    y = y + dy
        return bin_board

    def stability(self, chessboard, color):
        bin_board = np.zeros((self.chessboard_size, self.chessboard_size), dtype=bool)
        lim = self.chessboard_size

        sx, sy = 0, 0
        self.stabilize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = 0, lim - 1
        self.stabilize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = lim - 1, 0
        self.stabilize_bin_board(chessboard, bin_board, color, sx, sy)
        sx, sy = lim - 1, lim - 1
        self.stabilize_bin_board(chessboard, bin_board, color, sx, sy)

        # print(bin_board)
        ply_value = 0
        for i in bin_board:
            for j in i:
                if j:
                    ply_value = ply_value + 1

        bin_board = np.zeros((self.chessboard_size, self.chessboard_size), dtype=bool)
        lim = self.chessboard_size

        sx, sy = 0, 0
        self.stabilize_bin_board(chessboard, bin_board, adv_color(color), sx, sy)
        sx, sy = 0, lim - 1
        self.stabilize_bin_board(chessboard, bin_board, adv_color(color), sx, sy)
        sx, sy = lim - 1, 0
        self.stabilize_bin_board(chessboard, bin_board, adv_color(color), sx, sy)
        sx, sy = lim - 1, lim - 1
        self.stabilize_bin_board(chessboard, bin_board, adv_color(color), sx, sy)

        # print(bin_board)
        adv_value = 0
        for i in bin_board:
            for j in i:
                if j:
                    adv_value = adv_value + 1
        return 100 * (ply_value - adv_value) / (ply_value + adv_value + 1)

    def update_weight(self, rnd):
        # dynamic
        self.WEIGHT_DIFFERENCE = max(rnd - 40, 1) * 30
        self.WEIGHT_MOBILITY = min(61 - rnd, 25) * 30
        # static
        self.WEIGHT_CORNER = 0
        self.WEIGHT_STABILITY = 10
        self.WEIGHT_POSITION = 50

    def h(self, chessboard, color):
        # get status information
        depth, valid_moves = self.get_valid_moves(chessboard, color)
        self.update_weight(depth - 4)
        # calculate value
        mobility_value = len(valid_moves)
        difference_value = self.difference(chessboard, color)
        stable_value = 0
        # stable_value = self.stability(chessboard, color)
        position_value = self.position_value(chessboard, color)
        # print(mobility_value, stable_value, position_value)
        total_value = self.WEIGHT_MOBILITY * mobility_value + \
                      self.WEIGHT_STABILITY * stable_value + \
                      self.WEIGHT_POSITION * position_value + \
                      self.WEIGHT_DIFFERENCE * difference_value
        return total_value, valid_moves

    def minimax_search(self, chessboard, color, depth, beta):
        value, valid_moves = self.h(chessboard, color)

        if len(valid_moves) == 0 or depth == 0:
            return value

        best_move = None
        alpha = float('-inf')
        for x, y in valid_moves:
            # print(len(valid_moves))
            temp_chessboard = chessboard.copy()
            temp_chessboard = self.move(temp_chessboard, color, x, y)
            tv = -self.minimax_search(temp_chessboard, adv_color(color), depth - 1, -alpha)
            if depth == SEARCH_DEPTH:
                print(tv, (x, y))
            if tv > alpha:
                alpha = tv
                best_move = (x, y)
                if depth == SEARCH_DEPTH:
                    self.candidate_list.append(best_move)
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
        depth, self.candidate_list = self.get_valid_moves(chessboard, self.color)
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
