#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Board class for Gomoku
Generate GUI
detect click event of mouse and creat white or black chessman
record positions of chessman
determine win, loss or continue
"""

import numpy as np
import graphics as graph
import config as cfg

class Board(object):

    def __init__(self):
        self.n_row_ = cfg.N_ROW
        self.n_col_ = cfg.N_COL
        # position records the position of chessmen
        # 0 - empty, 1 - black, 2 - white
        self.position_ = np.zeros((self.n_row_, self.n_col_), dtype = int)
        # edge of board(xMin, xMax, yMin, yMax)
        self.board_edge_ = cfg.BOARD_EDGE
        # round
        self.round_ = 1


    # draw board 
    def drawBoard(self):
        # window object 
        self.win_ = graph.GraphWin("Board",\
            (self.board_edge_[1] - self.board_edge_[0]) * 1.25,\
            (self.board_edge_[3]- self.board_edge_[2]) * 1.25)
        # set color of background of window
        self.win_.setBackground(graph.color_rgb(240, 250, 15))
        # x,y-coordinates of grids
        self.x_pos_ = np.linspace(self.board_edge_[0], self.board_edge_[1], self.n_col_)
        self.y_pos_ = np.linspace(self.board_edge_[2], self.board_edge_[3], self.n_row_)
        # draw grid of chessboard
        for x in self.x_pos_:
            p1 = graph.Point(x, self.board_edge_[2])
            p2 = graph.Point(x, self.board_edge_[3])
            line = graph.Line(p1, p2)
            # set edge bold
            if x == self.board_edge_[0] or x == self.board_edge_[1]:
                line.setWidth(2.5)
            line.draw(self.win_)
        for y in self.y_pos_:
            p1 = graph.Point(self.board_edge_[0], y)
            p2 = graph.Point(self.board_edge_[1], y)
            line = graph.Line(p1, p2)
            # set edge bold
            if y == self.board_edge_[2] or y == self.board_edge_[3]:
                line.setWidth(2.5)
            line.draw(self.win_)


    # draw chessman responding to click
    def drawChessman(self, color = 1):
        dist_x = (self.board_edge_[1] - self.board_edge_[0]) / self.n_col_
        dist_y = (self.board_edge_[3] - self.board_edge_[2]) / self.n_row_
        # capture tolerance
        capture_tol = np.sqrt(dist_x ** 2 + dist_y ** 2) * 0.5
        # determine grid center of chessman 
        captured = False
        while(not captured):
            center_click = self.win_.getMouse()
            x_click = center_click.x
            y_click = center_click.y
            x_index = np.argmin(np.abs(self.x_pos_ - x_click))
            y_index = np.argmin(np.abs(self.y_pos_ - y_click))
            if np.sqrt((self.x_pos_[x_index] - x_click) ** 2 +\
                (self.y_pos_[y_index] - y_click) ** 2) <= capture_tol and\
                self.position_[y_index][x_index] == 0:
                p_center = graph.Point(self.x_pos_[x_index], self.y_pos_[y_index])
                captured = True
        # radius of chessman
        radius_chessman = capture_tol * 0.7
        circle = graph.Circle(p_center, radius_chessman)
        self.position_[y_index][x_index] = color
        if color == 2:
            circle.setFill('white')
            circle.setOutline('white')
        else:
            circle.setFill('black')
            circle.setOutline('black')
        circle.draw(self.win_)
        text = graph.Text(p_center, "%d" % self.round_)
        self.round_ += 1
        if color == 1:
            text.setTextColor('white')
        text.draw(self.win_)
        return y_index, x_index, color


    # draw chessman responding to AI computation
    def drawChessmanAI(self, row, col, color = 1):
        dist_x = (self.board_edge_[1] - self.board_edge_[0]) / self.n_col_
        dist_y = (self.board_edge_[3] - self.board_edge_[2]) / self.n_row_   
        radius_chessman = np.sqrt(dist_x ** 2 + dist_y ** 2) * 0.35
        p_center = graph.Point(self.x_pos_[col], self.y_pos_[row])
        circle = graph.Circle(p_center, radius_chessman)
        self.position_[row][col] = color
        if color == 1:
            circle.setFill('black')
            circle.setOutline('black')
        else: 
            circle.setFill('white')
            circle.setOutline('white')         
        circle.draw(self.win_)
        text = graph.Text(p_center, "%d" % self.round_)
        self.round_ += 1
        if color == 1:
            text.setTextColor('white')
        text.draw(self.win_)
        return row, col, color

    
    # draw interesting position inorder to debug
    def drawInterestingPos(self, row, col):
        dist_x = (self.board_edge_[1] - self.board_edge_[0]) / self.n_col_
        dist_y = (self.board_edge_[3] - self.board_edge_[2]) / self.n_row_   
        radius_chessman = np.sqrt(dist_x ** 2 + dist_y ** 2) * 0.1
        p_center = graph.Point(self.x_pos_[col], self.y_pos_[row])
        circle = graph.Circle(p_center, radius_chessman)
        circle.setFill('red')
        circle.setOutline('red')         
        circle.draw(self.win_)


    # determine win or not
    def judgeWin(self, judge_side = 1):
        # eight directions
        directions = np.asarray([[0, -1], [-1, -1], [-1, 0], [-1, 1],\
            [0, 1], [1, 1], [1, 0], [1, -1]], dtype = int)
        for i in range(self.n_row_):
            for j in range(self.n_col_):
                if self.position_[i][j] != judge_side:
                    continue
                for k in range(4):
                    side1 = 1
                    row = i + directions[k][0]
                    col = j + directions[k][1]
                    while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == self.position_[i][j]:
                        side1 += 1
                        row = i + directions[k][0] * side1
                        col = j + directions[k][1] * side1
                    side2 = 1
                    row = i + directions[k+4][0]
                    col = j + directions[k+4][1]
                    while row >= 0 and row < self.n_row_ and col >= 0 and col < self.n_col_ and\
                        self.position_[row][col] == self.position_[i][j]:
                        side2 += 1
                        row = i + directions[k+4][0] * side2
                        col = j + directions[k+4][1] * side2
                    length = side1 + side2 - 1
                    if length >= 5:
                        return True
        return False


    # print winer
    def printWiner(self, win_side = 1):
        center_point = graph.Point((self.board_edge_[0] + self.board_edge_[1]) / 2.0,\
            self.board_edge_[2] / 2.0)
        if win_side == 1:
            text = graph.Text(center_point, "The black wins the game. Congratulations!!!")
        else:
            text = graph.Text(center_point, "The white wins the game. Congratulations!!!")
        text.draw(self.win_)
        self.win_.getMouse()
        text.undraw()


    # close window and shutdow game
    def shutdownGame(self):
        self.win_.getMouse()
        self.win_.close()       

if __name__ == '__main__':
    board = Board()
    board.drawBoard()
    white_turn = False
    is_win = False
    while (not is_win):
        board.drawChessman(white_turn)
        is_win = board.judgeWin(white_turn)
        if (is_win):
            board.printWiner(white_turn)
        else:
            white_turn = not white_turn
    board.shutdownGame()