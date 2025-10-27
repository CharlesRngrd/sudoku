from typing import Generator, List
from grid_cell import GridCell
from grid_element import GridElement


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
                cell.get_possibilities()[0] if cell.is_solved else " "
                for cell in self.iter_element(GridElement.LINE, position)
            ]

            for bloc_end_separator in (6, 3):
                separator.insert(bloc_end_separator, "|")
                string.insert(bloc_end_separator, "|")

            if position in (3, 6):
                repr.append(" ".join(map(str, separator)))

            repr.append(" ".join(map(str, string)))

        return "\n".join(repr)

    def __initialize(self, sudoku: List[List[int]]) -> List[GridCell]:
        """
        Initialise une instance de GridCell pour chaque cellule du Sudoku.
        La grille passe d'une matérialisation en liste de listes à une matérialisation en liste.
        """

        return [
            GridCell(line, column, value)
            for line, line_items in enumerate(sudoku)
            for column, value in enumerate(line_items)
        ]

    def count_values(self) -> int:
        """Retourne le nombre de valeurs remplies dans la grille du Sudoku"""

        return len([cell for cell in self.iter_grid() if cell.is_solved])

    def iter_grid(self) -> Generator[GridCell, None, None]:
        """Retourne la liste des cellules de la grille du Sudoku"""

        for cell in self.__grid_cells:
            yield cell

    def iter_element(
        self, element: GridElement, position: int
    ) -> Generator[GridCell, None, None]:
        """Retourne la liste des cellules d'une ligne, d'une colonne ou d'un bloc de la grille du Sudoku"""

        for cell in self.__grid_cells:
            if cell.__getattribute__(element.value) == position:
                yield cell

    def check_solved(self) -> None:
        """Vérifie que chaque ligne, colonne et bloc contient 9 chiffres distincts"""

        error = False

        for number in range(9):
            for element in GridElement:
                unique_values = {
                    frozenset(cell.get_possibilities())
                    for cell in self.iter_element(element, number)
                }

                if len(unique_values) != 9:
                    error = True
                    break

        if error:
            print("Sudoku non résolu ❌")
        else:
            print("Sudoku résolu ✅")
