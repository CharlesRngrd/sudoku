from sudoku import Game

grid_demo = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9],
]

grid_level1 = [
    [None, None, None, None, None, None, 7, None, 6],
    [None, 7, None, 9, None, 6, 3, None, None],
    [None, 5, None, 4, 7, 3, 8, 9, None],
    [1, 3, 2, None, None, 5, None, 7, 9],
    [None, None, 4, 2, 1, None, 5, 3, 8],
    [None, 9, None, None, None, 4, None, None, None],
    [None, 2, 7, None, 6, 8, None, 1, 3],
    [None, None, None, None, 4, None, None, 8, None],
    [6, None, None, None, 9, 7, None, None, 4],
]

grid_level2 = [
    [8, 9, None, None, 7, 2, 5, None, 1],
    [5, None, 7, None, 3, None, 6, None, None],
    [None, 6, 3, 5, None, 9, None, 2, 7],
    [3, None, None, None, None, 7, None, None, None],
    [9, None, None, None, 8, None, 7, None, None],
    [None, None, 5, None, None, None, 2, None, None],
    [None, None, None, 4, 1, 5, None, 6, None],
    [None, 4, None, None, 6, None, None, None, None],
    [None, None, None, None, None, None, 3, None, None],
]

grid_level3 = [
    [7, 4, 5, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, 9, None],
    [None, 9, 6, None, 8, 4, 7, None, None],
    [None, 6, 1, None, None, 8, None, None, 4],
    [None, None, 9, 7, None, 3, 1, 8, None],
    [3, None, None, None, 1, None, None, None, 2],
    [None, 8, None, None, None, None, None, None, None],
    [None, None, None, None, 3, 1, None, None, 9],
    [None, None, None, None, None, None, 8, 2, 7],
]


for grid in [grid_demo, grid_level1, grid_level2, grid_level3]:
    game = Game(grid)
    game.process()
