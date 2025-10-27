from typing import Generator, List, Set, Tuple
from grid_cell import GridCell
from grid_iterable import GridIterable


class Grid:
    """Responsable de la grille du Sudoku"""

    def __init__(self, sudoku: List[List[int]]) -> None:
        self.__grid_cells = self.__initialize(sudoku)

    def __repr__(self) -> str:
        """Affiche la grille du Sudoku avec un séparateur 3x3"""

        repr: List = []

        for position in range(9):
            separator = ["-"] * 9
            string = [
                cell.solved_value if cell.solved_value else " "
                for cell in self.iter_element(GridIterable.LINE, position)
            ]

            for bloc_end_separator in (6, 3):
                separator.insert(bloc_end_separator, "|")
                string.insert(bloc_end_separator, "|")

            if position in (3, 6):
                repr.append(" ".join(map(str, separator)))

            repr.append(" ".join(map(str, string)))

        return "\n".join(repr)

    def __initialize(self, sudoku: List[List[int]]) -> Set[GridCell]:
        """
        Initialise une instance de GridCell pour chaque cellule du Sudoku.
        La grille passe d'une matérialisation en liste de listes à une matérialisation en liste.
        """

        return {
            GridCell(line, column, value)
            for line, line_items in enumerate(sudoku)
            for column, value in enumerate(line_items)
        }

    def count_values(self) -> int:
        """Retourne le nombre de valeurs remplies dans la grille du Sudoku"""

        return len({cell for cell in self.iter_grid() if cell.solved_value})

    def iter_grid(self) -> Generator[GridCell, None, None]:
        """Retourne la liste des cellules de la grille du Sudoku"""

        for cell in self.__grid_cells:
            yield cell

    def iter_element(
        self, iterable: GridIterable, position: int
    ) -> Generator[GridCell, None, None]:
        """Retourne la liste des cellules d'une ligne, d'une colonne ou d'un bloc de la grille du Sudoku"""

        count = 0
        for cell in self.__grid_cells:
            if count == 9:
                return

            if cell.get_attribute(iterable) == position:
                count += 1
                yield cell

    def iter_element_all(
        self,
    ) -> Generator[Tuple[int, int, GridIterable, List[GridCell]], None, None]:
        """Retourne le liste des cellules de chaque ligne, de chaque colonne, de chaque bloc pour chaque chiffre"""

        for position in range(9):
            for number in range(9):
                for iterable in GridIterable:
                    cells = {
                        cell
                        for cell in self.iter_element(iterable, position)
                        if (number + 1) in cell.get_possibilities()
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
                    frozenset(cell.get_possibilities())
                    for cell in self.iter_element(iterable, number)
                }

                if len(unique_values) != 9:
                    error = True

        if error:
            return "Sudoku non résolu ❌\n"
        else:
            return "Sudoku résolu ✅\n"
