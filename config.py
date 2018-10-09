## board
N_ROW = 15
N_COL = 15
BOARD_EDGE = [50, 450, 50, 450]


## side 1 : black, 2 : white
AI_SIDE = 1

## AI search paremeters
# search depth of decision tree
SEARCH_DEPTH = 8
# interesting range, the position which distance between occupied position 
# within interesting range will be considered in next move
INTERESTING_RANGE = 2


## weights of whole postion
# weights for score in different mode
# [alive one, alive two, alive three, alive four, alive five,
# dead two, dead three, dead four]
# alive means both side is clear, dead means one side is blocked and the
# other side is clear. Ignore both side is blocked
WEIGHTS = [10, 100, 1000, 10000, 100000, 10, 100, 100] 

## weights of vacant position
FIVE = 100000
BLOCK_FOUR = 50000
FOUR = 10000
BLOCK_THREE = 4000
THREE = 1000
BLOCK_TWO = 500
TWO = 200
OTHERS = 10

