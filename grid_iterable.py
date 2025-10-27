from enum import Enum


class GridIterable(Enum):
    """Liste les éléments de la grille du Sudoku sur lesquels on peut itérer"""

    LINE = "line"
    COLUMN = "column"
    BLOC = "bloc"
