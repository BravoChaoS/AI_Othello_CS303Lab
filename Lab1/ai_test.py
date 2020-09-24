import ai
import numpy as np

chessboard = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, -1, 0, 0, 0, 0, 0, 0],
                       [0, 0, -1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, -1, 0, 0, 0],
                       [0, 0, 0, -1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

ai = ai.AI(8, 1, 100)

lst = ai.go(chessboard)
# for i in lst:
#     print(i)
