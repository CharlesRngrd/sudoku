from time import time
from grid import Grid
from grid_processor import GridProcessor

sudokus = [
    [
        [7, 4, 5, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, 9, None],
        [None, 9, 6, None, 8, 4, 7, None, None],
        [None, 6, 1, None, None, 8, None, None, 4],
        [None, None, 9, 7, None, 3, 1, 8, None],
        [3, None, None, None, 1, None, None, None, 2],
        [None, 8, None, None, None, None, None, None, None],
        [None, None, None, None, 3, 1, None, None, 9],
        [None, None, None, None, None, None, 8, 2, 7],
    ],
    [
        [None, None, None, None, 3, 2, None, 6, 8],
        [None, None, None, 5, None, 8, None, None, 3],
        [None, None, None, 7, None, 4, None, None, 1],
        [4, 3, 5, None, 7, None, None, None, 2],
        [None, None, 6, None, None, 9, None, 8, None],
        [None, None, None, None, None, None, 3, None, None],
        [1, 9, None, None, None, None, None, 5, None],
        [None, None, None, 9, None, None, None, None, None],
        [5, None, 4, None, 8, None, 7, None, 9],
    ],
    [
        [None, None, None, 9, None, 2, None, 8, 7],
        [7, 6, None, None, 8, None, None, None, None],
        [None, 2, None, 3, None, None, 5, None, None],
        [None, None, None, None, None, None, 8, None, 3],
        [2, None, None, 7, 5, None, 1, None, None],
        [None, None, None, 2, None, None, None, None, 4],
        [None, None, None, 5, None, None, 9, 4, None],
        [5, None, None, None, None, None, None, 3, None],
        [8, None, 1, 6, 4, 9, None, None, None],
    ],
    [
        [2, None, None, None, 9, None, 7, None, None],
        [4, 9, None, None, 5, 7, 8, None, None],
        [None, None, 3, 2, None, None, 1, None, 6],
        [None, 4, None, None, None, None, 2, 5, None],
        [5, None, None, None, None, 2, 9, 8, None],
        [None, 2, 7, None, None, None, None, None, 3],
        [None, None, None, None, None, None, None, 6, None],
        [None, None, None, None, None, 5, None, None, None],
        [1, 8, 5, None, 6, None, None, None, None],
    ],
    [
        [None, 8, 4, 6, None, None, None, None, 1],
        [2, 5, 7, None, None, 1, 6, None, None],
        [None, None, 3, 5, 4, None, None, None, None],
        [1, None, None, None, None, 4, None, 5, None],
        [7, None, None, 3, None, None, None, None, None],
        [None, None, None, None, None, 7, 4, 9, None],
        [None, None, None, None, 1, None, None, None, 2],
        [5, None, None, None, 2, 8, None, 7, None],
        [None, 2, None, None, None, None, 1, None, None],
    ],
    [
        [None, None, 5, None, None, None, None, 6, 2],
        [None, 6, 3, None, None, 9, None, None, None],
        [None, None, None, None, None, None, None, None, 4],
        [None, None, None, None, None, 6, 7, None, 3],
        [None, None, 6, 7, None, 5, None, None, None],
        [1, None, None, 8, None, None, None, None, None],
        [8, None, 1, 2, None, None, 6, None, None],
        [None, None, None, None, None, None, 5, 3, None],
        [None, 4, None, None, None, None, 8, None, None],
    ],
    [
        [None, None, 5, 6, None, 2, None, None, None],
        [7, None, None, 8, 1, None, 4, None, None],
        [None, None, None, None, None, None, 5, 6, None],
        [None, 4, 9, None, None, None, None, None, None],
        [8, None, None, None, None, None, None, None, 7],
        [None, None, None, None, 5, 1, None, None, None],
        [None, None, None, 9, 4, None, 8, None, 2],
        [3, None, 6, 1, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ],
    [
        [None, None, 5, None, 7, 2, None, None, None],
        [4, 3, 8, None, None, None, None, None, None],
        [None, None, 7, None, 1, None, None, None, None],
        [None, None, None, None, None, 4, None, None, None],
        [None, 5, None, None, None, 8, None, 3, None],
        [None, None, None, 7, None, None, 4, 8, None],
        [3, None, None, None, None, None, None, None, 5],
        [None, 6, None, None, None, None, 7, None, None],
        [None, None, None, 6, 9, None, None, None, 2],
    ],
    [
        [None, 1, None, None, None, 8, None, None, 6],
        [3, 6, None, None, None, None, None, None, None],
        [None, None, None, 5, None, None, None, None, 7],
        [None, None, None, None, 8, 4, 5, 1, None],
        [None, None, None, None, None, None, None, None, None],
        [9, None, 5, None, 1, 3, 8, None, None],
        [None, None, 2, None, 9, None, None, None, None],
        [None, None, 3, 7, None, None, None, None, None],
        [7, None, None, None, None, None, 4, None, None],
    ],
    [
        [None, None, None, 2, 4, 8, None, None, None],
        [None, None, None, 9, None, None, None, 6, None],
        [None, None, None, 5, None, None, 1, 9, None],
        [None, None, None, None, None, None, 4, None, None],
        [None, 8, None, None, None, 5, 2, None, None],
        [None, 2, 4, None, None, None, None, None, 9],
        [5, None, None, None, 8, None, None, None, None],
        [None, None, 9, None, None, 7, None, None, None],
        [1, None, None, None, None, None, None, 3, 7],
    ],
]

time_start = time()

for sudoku in sudokus:
    grid = Grid(sudoku)

    print(f"Nombre de valeurs initiales : {grid.count_values()}")

    GridProcessor.execute(grid)

    print(f"Nombre de valeurs finales : {grid.count_values()}")
    print(grid)
    print(grid.check_solved())

time_end = time()

print(f"{len(sudokus)} résolus en {round(time_end - time_start, 2)} secondes")
