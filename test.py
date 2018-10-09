#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time 
import board as chess
import aiPlayer as ai


board = chess.Board()
board.drawBoard()
player = ai.AIPlayer()
player.update(board.drawChessmanAI(7, 7, color = 1))

is_win = False
while (not is_win):
    player.update(board.drawChessman(color = 2))
    is_win = board.judgeWin(judge_side= 2)
    if is_win:
        board.printWiner(win_side= 2)
        break
    start = time.clock()
    best_row, best_col, best_score = player.search()
    end = time.clock()
    print("Thinking time is %.2f seconds" % (end - start))
    print(best_row, best_col, best_score)
    player.update(board.drawChessmanAI(best_row, best_col, color = 1))
    is_win = board.judgeWin(judge_side= 1)
    if is_win:
        board.printWiner(win_side= 1)
        break
board.shutdownGame()