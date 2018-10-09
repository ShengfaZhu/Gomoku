#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Play gomoku against human player with AI
Using max-min search algorithm of zero-sum game
"""
import numpy as np 
from collections import deque
import sys
import config as cfg

class AIPlayer(object):

    def __init__(self, side = 1):
        self.side_ = cfg.AI_SIDE # 1 : black, first; 2 : white, next
        self.n_row_ = cfg.N_ROW
        self.n_col_ = cfg.N_COL
        # position records the position of chessmen
        # 0 - empty, 1 - black, 2 - white
        self.position_ = np.zeros((self.n_row_, self.n_col_), dtype = int)
        self.search_depth_ = cfg.SEARCH_DEPTH
        self.weights_ = cfg.WEIGHTS
        self.interesting_range_ = cfg.INTERESTING_RANGE
        # interesting position list, ingonre the positin outside interesting range
        self.interesting_pos_ = []
    

    # count the number of continuous chessman 
    # in eight directions of each location
    def calContinuousChessman(self):
        # count same chessman in eight directions
        count = np.zeros((self.n_row_, self.n_col_, 8), dtype = int)
        # eight directions
        directions = [[0, -1], [-1, -1], [-1, 0], [-1, 1],\
            [0, 1], [1, 1], [1, 0], [1, -1]]
        # index of row and col increasing step 
        row_col_step = [[0, self.n_row_, 1, 0, self.n_col_, 1],\
            [0, self.n_row_, 1, self.n_col_ - 1, -1, -1],\
            [self.n_row_ - 1, -1, -1, self.n_col_ - 1, -1, -1],\
            [self.n_row_ - 1, -1, -1, 0, self.n_col_, 1]]
        # update count from eight directions
        for k in range(4):
            for i in range(row_col_step[k][0], row_col_step[k][1], row_col_step[k][2]):
                for j in range(row_col_step[k][3], row_col_step[k][4], row_col_step[k][5]):
                    judge_side = self.position_[i][j]
                    if judge_side == 0:
                        continue
                    for m in range(2):
                        count[i][j][2*k + m] = 1
                        i_prev = i + directions[2*k + m][0]
                        j_prev = j + directions[2*k + m][1]
                        if (i_prev >= 0 and i_prev < self.n_row_ and j_prev >= 0 and\
                            j_prev < self.n_col_ and self.position_[i_prev][j_prev] == judge_side):
                            count[i][j][2*k + m] = count[i_prev][j_prev][2*k + m] + 1
        return count


    # score for give count
    def score(self, count):
        score_black = 0 # score of the black side
        score_white = 0 # score of the white side
        score_matrix = np.zeros((self.n_row_, self.n_col_))
        # eight directions
        directions = np.asarray([[0, -1], [-1, -1], [-1, 0], [-1, 1],\
            [0, 1], [1, 1], [1, 0], [1, -1]], dtype = int)
        for i in range(self.n_row_):
            for j in range(self.n_col_):
                if count[i][j][0] == 0:
                    continue
                temp_score = 0
                # check eight directions
                for k in range(4):
                    length = count[i][j][k] + count[i][j][k+4] - 1
                    # length should be between 1 and 5
                    length = min(length, 5)
                    length = max(length, 1)
                    # determine alive or dead
                    alive_side = 0
                    for m in [0, 4]:
                        side = np.asarray([i, j], dtype = int) + directions[k+m] * count[i][j][k+m]
                        if (side[0] >= 0 and side[0] < self.n_row_ and side[1] >= 0 and\
                            side[1] < self.n_col_ and self.position_[side[0]][side[1]] == 0):
                            alive_side = alive_side + 1
                    if alive_side == 2 or length == 5:# alive
                        temp_score += self.weights_[length - 1]
                    elif alive_side == 1 and length >= 2:# dead
                        temp_score += self.weights_[length + 3]
                score_matrix[i][j] = temp_score
                if self.position_[i][j] == 1:# black
                    score_black += temp_score
                else:# white
                    score_white += temp_score
        # for item in self.position_:
        #     print(item)
        # for item in score_matrix:
        #     print(item)
        # print(score_black - score_white)
        return score_black - score_white
        


    # elatuate the score of given position
    def evaluate(self):
        score_black = 0 # score of the black side
        score_white = 0 # score of the white side
        # eight directions
        directions = np.asarray([[0, -1], [-1, -1], [-1, 0], [-1, 1],\
            [0, 1], [1, 1], [1, 0], [1, -1]], dtype = int)
        # score_matrix = np.zeros((self.n_row_, self.n_col_), dtype = int)
        for i in range(self.n_row_):
            for j in range(self.n_col_):
                if self.position_[i][j] == 0:
                    continue
                temp_score = 0
                for k in range(4):
                    side1 = 1
                    row = i + directions[k][0]
                    col = j + directions[k][1]
                    while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == self.position_[i][j]:
                        side1 += 1
                        row = i + directions[k][0] * side1
                        col = j + directions[k][1] * side1
                    side1_alive = False
                    if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == 0:
                        side1_alive = True
                    side2 = 1
                    row = i + directions[k+4][0]
                    col = j + directions[k+4][1]
                    while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == self.position_[i][j]:
                        side2 += 1
                        row = i + directions[k+4][0] * side2
                        col = j + directions[k+4][1] * side2
                    side2_alive = False
                    if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == 0:
                        side2_alive = True
                    length = side1 + side2 - 1
                    length = max(length, 1)
                    length = min(length, 5)
                    if length == 5 or (side1_alive and side2_alive):
                        temp_score += self.weights_[length - 1]
                    elif length >= 2 and (side1_alive or side2_alive):
                        temp_score += self.weights_[length + 3]
                # score_matrix[i][j] = temp_score
                if self.position_[i][j] == 1:
                    score_black += temp_score
                else: 
                    score_white += temp_score
        # for item in score_matrix:
        #     print(item)
        return score_black - score_white

    
    # update current postion and
    # update set of interesting position according to previous move
    def update(self, move):
        self.updatePos(move)
        offensive_side = (move[2] % 2) + 1
        self.updateInterestingPos(offensive_side)


    # undo previous move
    def undo(self, prev_move):
        self.position_[prev_move[0]][prev_move[1]] = 0
        self.interesting_pos_.clear()

    # update current postion
    def updatePos(self, move):
        # move = (row, col, color)
        # update self position
        row = move[0]
        col = move[1]
        self.position_[row][col] = move[2]
        
    
    # print position
    def printPosition(self):
        for items in self.position_:
            print(items)


    # update interesting position with BFS
    # def updateInterestingPos(self, prev_row, prev_col):
    #     # remove (prev_row, prev_col) from interesting pos set
    #     if self.interesting_pos_.__contains__((prev_row, prev_col)):
    #         self.interesting_pos_.remove((prev_row, prev_col))
    #     q = deque() # assisted queue for BFS
    #     # eight directions
    #     directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1),\
    #         (0, 1), (1, 1), (1, 0), (1, -1)]
    #     q.appendleft((prev_row, prev_col))
    #     depth = 0
    #     while (len(q) > 0) and (depth < self.interesting_range_):
    #         sz = len(q)
    #         depth = depth + 1
    #         for _ in range(sz):
    #             # delete and reture the front of queue
    #             curr = q.pop()
    #             for j in range(len(directions)):
    #                 temp = (curr[0] + directions[j][0], curr[1] + directions[j][1])
    #                 if temp[0] >= 0 and temp[0] < self.n_row_ and temp[1] >= 0 and\
    #                     temp[1] < self.n_col_ and self.position_[temp[0]][temp[1]] == 0:   
    #                     q.appendleft(temp)
    #                     if self.interesting_pos_.__contains__(temp) == False:
    #                         self.interesting_pos_.add(temp)
    #     q.clear()


    # evaluate each vacant position, and sort them into list
    def updateInterestingPos(self, side):
        self.interesting_pos_.clear()
        block_threes = []
        threes = []
        block_twos = []
        twos = []
        others = []
        for row in range(self.n_row_):
            for col in range(self.n_col_):
                if self.position_[row][col] != 0:
                    continue
                # determine if (row, col) in interesting range
                if not self.withinRange(row, col):
                    continue
                score = self.evaluateVacant(row, col, side)
                if score >= cfg.FIVE:
                    self.interesting_pos_.append((row, col))
                    return
                elif score >= cfg.BLOCK_FOUR:
                    self.interesting_pos_.append((row, col))
                    return
                elif score >= cfg.FOUR:
                    self.interesting_pos_.append((row, col))
                    return
                elif score >= 2 * cfg.BLOCK_THREE:
                    self.interesting_pos_.append((row, col))
                    return
                elif score >= cfg.BLOCK_THREE:
                    block_threes.append((row, col))
                elif score >= 2 * cfg.THREE:
                    self.interesting_pos_.append((row, col))
                    return
                elif score >= cfg.THREE:
                    threes.append((row, col))
                elif score >= cfg.BLOCK_TWO:
                    block_twos.append((row, col))
                elif score >= cfg.TWO:
                    twos.append((row, col))
                else:
                    others.append((row, col))    
        self.interesting_pos_ = block_threes + threes + block_twos + twos + others



    # determine if (row, col) in interesting range
    def withinRange(self, row, col):
        directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1),\
            (0, 1), (1, 1), (1, 0), (1, -1)]
        for step in range(1, self.interesting_range_ + 1):
            for j in range(len(directions)):
                temp = (row + directions[j][0] * step, col + directions[j][1] * step)
                if temp[0] >= 0 and temp[0] < self.n_row_ and temp[1] >= 0 and\
                    temp[1] < self.n_col_ and self.position_[temp[0]][temp[1]] != 0:
                    return True
        return False


    # evaluate each vacant 
    def evaluateVacant(self, curr_row, curr_col, side):
        offensive_side = side
        defensive_side = (side % 2) + 1
        directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1),\
            (0, 1), (1, 1), (1, 0), (1, -1)]
        temp_score = 0
        # offensive
        for k in range(4):
            side1 = 1
            row = curr_row + directions[k][0]
            col = curr_col + directions[k][1]
            while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == offensive_side:
                side1 += 1
                row = curr_row + directions[k][0] * side1
                col = curr_col + directions[k][1] * side1
            side1_alive = False
            if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == 0:
                side1_alive = True
            side2 = 1
            row = curr_row + directions[k+4][0]
            col = curr_col + directions[k+4][1]
            while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == offensive_side:
                side2 += 1
                row = curr_row + directions[k+4][0] * side2
                col = curr_col + directions[k+4][1] * side2
            side2_alive = False
            if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == 0:
                side2_alive = True
            length = side1 + side2 - 1
            length = max(length, 1)
            length = min(length, 5)
            if length >= 5:
                return cfg.FIVE
            elif length == 4 and side1_alive and side2_alive:
                temp_score += cfg.FOUR
            elif length == 4 and (side1_alive or side2_alive):
                temp_score += cfg.THREE
            elif length == 3 and side1_alive and side2_alive:
                temp_score += cfg.THREE
            elif length == 2 and side1_alive and side2_alive:
                temp_score += cfg.TWO
            else:
                temp_score += cfg.OTHERS
        # defensive
        for k in range(4):
            side1 = 1
            row = curr_row + directions[k][0]
            col = curr_col + directions[k][1]
            while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == defensive_side:
                side1 += 1
                row = curr_row + directions[k][0] * side1
                col = curr_col + directions[k][1] * side1
            side1_alive = False
            if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == 0:
                side1_alive = True
            side2 = 1
            row = curr_row + directions[k+4][0]
            col = curr_col + directions[k+4][1]
            while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == defensive_side:
                side2 += 1
                row = curr_row + directions[k+4][0] * side2
                col = curr_col + directions[k+4][1] * side2
            side2_alive = False
            if row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                self.position_[row][col] == 0:
                side2_alive = True
            length = side1 + side2 - 1
            length = max(length, 1)
            length = min(length, 5)
            if length >= 5:
                return cfg.BLOCK_FOUR
            elif length == 4 and (side1_alive or side2_alive):
                temp_score += cfg.BLOCK_THREE
            elif length == 3 and side1_alive and side2_alive:
                temp_score += cfg.TWO
            else:
                temp_score += cfg.OTHERS
        return temp_score
            

    # print interesting position
    def printInterestingPos(self):
        print(self.interesting_pos_)



    # search for best decision under current situation 
    def search(self):
        best_score = -1 * sys.maxsize
        # print(self.interesting_pos_)
        for row, col in self.interesting_pos_:
            self.position_[row][col] = self.side_
            # score = self.searchCore(1)
            score = self.searchAlphaBeta(1, best_score, sys.maxsize)
            if score > best_score:
                best_score = score
                best_row, best_col = row, col
            self.position_[row][col] = 0
        return best_row, best_col, best_score


    # implement max-min search
    def searchCore(self, depth):
        if depth == self.search_depth_:
            count = self.calContinuousChessman()
            return self.score(count)
        best_score = -1 * sys.maxsize
        sign = 1
        if (depth % 2) == 1:
            sign = -1
        for i, j in self.interesting_pos_:
            if self.position_[i][j] == 0:
                self.position_[i][j] = (depth % 2) + 1
                s = self.searchCore(depth + 1)
                s = sign * s
                if (s > best_score):
                    best_score = s
                self.position_[i][j] = 0
        return sign * best_score


    # implement max-min search
    # using alpha-beta prunning:
    # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    # alpha: maximum number so far, beta: minimum number so far
    def searchAlphaBeta(self, depth, alpha, beta):
        if depth == self.search_depth_:
            # count = self.calContinuousChessman()
            return self.evaluate()
        best_score = -1 * sys.maxsize
        new_alpha = -1 * sys.maxsize
        new_beta = sys.maxsize
        sign = 1
        if (depth % 2) == 1:
            sign = -1
            self.updateInterestingPos((self.side_ % 2) + 1)
        else:
            self.updateInterestingPos(self.side_)
        for i, j in self.interesting_pos_:
            if self.position_[i][j] == 0:
                self.position_[i][j] = (depth % 2) + 1
                s = self.searchAlphaBeta(depth + 1, new_alpha, new_beta)
                # update alpha and beta
                new_alpha = max(new_alpha, s)
                new_beta = min(new_beta, s)
                s = sign * s
                if (s > best_score):
                    best_score = s
                self.position_[i][j] = 0
                # determine whether pruning
                if ((sign > 0) and (s > beta)) or ((sign < 0) and (sign * s < alpha)):
                    return sign * best_score
        return sign * best_score
