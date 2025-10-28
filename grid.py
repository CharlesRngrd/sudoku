from typing import Dict, Generator, List, Tuple

from grid_cell import GridCell
from grid_iterable import GridIterable


class Grid:
    """Responsable de la grille du Sudoku"""

    def __init__(self, sudoku: List[List[int]]) -> None:
        self.grid = sudoku

        self.possibilities: Dict[str, Dict[int, List[GridCell]]] = {
            iterable: {key: [] for key in range(9)} for iterable in GridIterable
        }

        self.__initialize()

    def __repr__(self) -> str:
        """Affiche la grille du Sudoku avec un séparateur 3x3"""

        repr: List = []

        for position in range(9):
            separator = ["-"] * 9
            string = [cell if cell else " " for cell in self.grid[position]]

            for bloc_end_separator in (6, 3):
                separator.insert(bloc_end_separator, "|")
                string.insert(bloc_end_separator, "|")

            if position in (3, 6):
                repr.append(" ".join(map(str, separator)))

            repr.append(" ".join(map(str, string)))

        return "\n".join(repr)

    def __initialize(self) -> None:
        """
        Initialise la liste des possibilités à partir de la grille de Sudoku de départ
        """

        for line, column, value in self.iter_grid():
            cell = GridCell(line, column, value)

            for iterable in GridIterable:
                self.possibilities[iterable][cell.get_attribute(iterable)].append(cell)

    def move_solved_cell(self, cell: GridCell) -> None:
        """Ajout une valeur à la grille du Sudoku"""

        self.grid[cell.line][cell.column] = cell.solved_value

        for iterable in GridIterable:
            self.possibilities[iterable][cell.get_attribute(iterable)].remove(cell)

    def count_values(self) -> int:
        """Retourne le nombre de valeurs remplies dans la grille du Sudoku"""

        return len([value for _, _, value in self.iter_grid() if value])

    def iter_grid(
        self, iterable: GridIterable = None, position: int = None, number: int = None
    ) -> Generator[int, None, None]:
        """Retourne la liste des cellules de la grille du Sudoku"""

        for line, line_items in enumerate(self.grid):
            for column, value in enumerate(line_items):
                match iterable:
                    case GridIterable.LINE:
                        if line != position:
                            continue

                    case GridIterable.COLUMN:
                        if column != position:
                            continue

                    case GridIterable.BLOC:
                        if GridCell.compute_bloc(line, column) != position:
                            continue

                if number and value != number:
                    continue

                yield line, column, value

    def iter_possibilities(
        self, iterable: GridIterable, position: int, number: int = None
    ) -> Generator[GridCell, None, None]:
        """Retourne la liste des cellules d'une ligne, d'une colonne ou d'un bloc de la grille du Sudoku"""

        for cell in self.possibilities[iterable][position]:
            if number and number not in cell.get_possibilities():
                continue

            yield cell

    def iter_possibilities_wrapper(
        self,
    ) -> Generator[Tuple[int, int, GridIterable, List[GridCell]], None, None]:
        """Retourne le liste des cellules de chaque ligne, de chaque colonne, de chaque bloc pour chaque chiffre"""

        for position in range(9):
            for number in range(9):
                for iterable in GridIterable:
                    cells = {
                        cell
                        for cell in self.iter_possibilities(
                            iterable, position, number + 1
                        )
                    }

                    yield position, number, iterable, cells

    def check_solved(self) -> None:
        """Vérifie que chaque ligne, colonne et bloc contient 9 chiffres distincts"""

        error = False

        for number in range(9):
            if error:
                break

            for iterable in GridIterable:
                if error:
                    break

                unique_values = {
                    value for _, _, value in self.iter_grid(iterable, number)
                }

                if len(unique_values) != 9:
                    error = True

        if error:
            return "Sudoku non résolu ❌\n"

        return "Sudoku résolu ✅\n"
