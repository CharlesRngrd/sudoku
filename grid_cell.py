from typing import Set

from grid_iterable import GridIterable
from grid_processor import GridProcessor


class GridCell:
    """Responsable de la position et des possibilités d'une cellule du Sudoku"""

    def __init__(self, line: int, column: int, value: int) -> None:
        self.line = line
        self.column = column

        self.bloc = self.compute_bloc(line, column)

        self.__possibilities: Set[int] = set()

        self.__initialize(value)

    @property
    def solved_value(self) -> int:
        """Retourne la valeur d'une cellule du Sudoku si elle a été trouvée"""

        if len(self.__possibilities) == 1:
            return next(iter(self.__possibilities))

    def __repr__(self):
        return f"Cellule({self.line}, {self.column}, {self.__possibilities})"

    def __initialize(self, value: int) -> None:
        """
        Initialise les possibilités d'une cellule du Sudoko :
        - Si la valeur de départ est nulle, alors tous les chiffres sont possibles
        - Si la valeur de départ est un chiffre, alors cette cellule est résolue
        """

        if value:
            self.solve_possibility(value)

        else:
            self.__possibilities = {number + 1 for number in range(9)}

    @staticmethod
    def compute_bloc(line: int, column: int):
        """Retourne le bloc 3x3 associé à la ligne et à la colonne"""

        return (line // 3) * 3 + column // 3

    def get_attribute(self, iterable: GridIterable) -> int:
        """Retourne de façon dynamique un attribut d'une cellule du Sudoku"""

        match iterable:
            case GridIterable.LINE:
                return self.line
            case GridIterable.COLUMN:
                return self.column
            case GridIterable.BLOC:
                return self.bloc

    def get_possibilities(self) -> Set[int]:
        """Retourne les possibilités d'une cellule du Sudoku"""

        return self.__possibilities

    def solve_possibility(self, value: int) -> None:
        """Assigne la valeur à la cellule et notifie le gestionnaire d'évènements"""

        self.__possibilities = {value}
        GridProcessor.add_solved_cell(self)

    def drop_possibility(self, value: int) -> None:
        """
        Supprime une possibilité d'une cellule du Sudoku.
        S'il ne reste qu'une possibilité, le gestionnaire d'évènements est notifié.
        """

        if value in self.__possibilities:
            self.__possibilities.remove(value)

            if self.solved_value:
                GridProcessor.add_solved_cell(self)
