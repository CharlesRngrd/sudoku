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
    [None, 8, 3, None, None, 7, None, 6, None],
    [9, 1, None, None, None, 2, 7, 4, None],
    [2, None, 7, 1, None, None, None, None, None],
    [1, 9, None, None, None, None, None, 3, None],
    [6, 5, 2, 8, None, None, None, 7, None],
    [None, None, 4, None, None, None, 5, None, None],
    [5, None, 1, None, 4, 6, None, None, 7],
    [8, 4, None, 7, None, 9, 3, None, None],
    [7, 2, 9, None, None, None, None, None, 6],
]


for grid in [grid_demo, grid_level1]:
    game = Game(grid)
    game.print(game.grid)
    game.process()
    game.print(game.grid)
    game.assert_finish()
