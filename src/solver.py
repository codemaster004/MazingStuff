import numpy as np

MAZE_SIZE = [6, 8]  # X, Y

START_POINT = (0, 0)
END_POINT = (1, 2)

maze = np.load("assets/maze.npy")
"""
Wall Encoding:
[
 0: (W, W, W, W), (W, W, W, S), (W, W, S, W), (W, W, S, S),
 4: (W, S, W, W), (W, S, W, S), (W, S, S, W), (W, S, S, S),
 8: (S, W, W, W), (S, W, W, S), (S, W, S, W), (S, W, S, S),
12: (S, S, W, W), (S, S, W, S), (S, S, S, W), (S, S, S, S)
]
      1
     ---
  3 |   | 2
     ---
      0
"""
maze_list = [[10, 11, 9], [14, 15, 13], [6, 7, 5]]


def find_shortest_route():
	pass
