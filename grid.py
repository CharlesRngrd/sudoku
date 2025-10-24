from typing import Generator, List


class GridCell:
    def __init__(self, line: int, column: int, value: int = None) -> None:
        self.line = line
        self.column = column
        self.value = value

    def get_bloc_line(self) -> int:
        return self.line // 3

    def get_bloc_col(self) -> int:
        return self.column // 3


class GridAvailableList:
    POSSIBILITIES = None

    @classmethod
    def define_possibilities(cls) -> None:
        cls.POSSIBILITIES = [
            [[number + 1 for number in range(9)] for _ in range(9)] for _ in range(9)
        ]

    @classmethod
    def remove_possibility(cls, cell: GridCell, old_value: int) -> None:
        """Actualise la liste des valeurs possibles pour une cellule du sudoku"""

        if old_value:
            cls.POSSIBILITIES[cell.line][cell.column].remove(old_value)


class Grid:
    def __init__(self, data: List[List[int]]) -> None:
        self._data = data

    def __repr__(self) -> str:
        """Affiche la grille avec un séparateur 3x3"""

        repr: List = []

        for cells in self.iter_lines():
            separator = ["-"] * len(cells)
            string = [cell.value or " " for cell in cells]

            for position in (6, 3):
                separator.insert(position, "|")
                string.insert(position, "|")

            if cells[0].line in (3, 6):
                repr.append(" ".join(map(str, separator)))

            repr.append(" ".join(map(str, string)))

        return "\n".join(repr)

    def iter_lines(self) -> Generator[List[GridCell], None, None]:
        """Retourne la liste des lignes de la grille"""

        for index_line, line in enumerate(self._data):
            yield [
                GridCell(index_line, index_cell, cell)
                for index_cell, cell in enumerate(line)
            ]

    def iter_columns(self) -> Generator[List[GridCell], None, None]:
        """Retourne la liste des colonnes de la grille"""

        for column in range(9):
            to_yield = []
            for cells in self.iter_lines():
                to_yield.append(*[cell for cell in cells if cell.column == column])

            yield to_yield

    def iter_blocs(self) -> Generator[List[GridCell], None, None]:
        """Retourne la liste des blocs de la grille"""

        for line_bloc in range(3):
            for column_bloc in range(3):
                to_yield = []

                for cell in self.iter_cells():
                    if (
                        cell.get_bloc_line() == line_bloc
                        and cell.get_bloc_col() == column_bloc
                    ):
                        to_yield.append(cell)

                yield to_yield

    def iter_cells(self) -> Generator[GridCell, None, None]:
        """Retourne la liste complète des valeurs de la grille"""

        for cells in self.iter_lines():
            for cell in cells:
                yield cell

    def get_cell(self, cell: GridCell) -> GridCell:
        """Retourne la valeur d'une cellule de la grille"""

        GridCell.value = self._data[cell.line][cell.column]

        return GridCell

    def update_cell(self, cell: GridCell) -> None:
        """Modifie la valeur d'une cellule de la grille"""

        self._data[cell.line][cell.column] = cell.value

    def count_values(self) -> int:
        """Retourne le nombre de valeurs remplies dans la grille"""

        return len([cell.value for cell in self.iter_cells() if cell.value])

    def check_lines_completed(self) -> bool:
        """Vérifie si toutes les lignes contiennent tous les chiffres de 1 à 9"""

        return all([len(set(line)) == 9 for line in self._data])

    def check_columns_completed(self) -> bool:
        """Vérifie si toutes les colonnes contiennent tous les chiffres de 1 à 9"""

        return all(
            [
                len(set([line[column] for line in self._data])) == 9
                for column in range(9)
            ]
        )


class GridAvailableSingle(Grid):
    def update_cell(self, cell: GridCell) -> None:
        """Modifie la valeur d'une cellule de la grille"""

        raise NotImplementedError("Please use GridAvailableSingle.reset_cell instead !")

    def reset_cell(self, cell: GridCell) -> None:
        """Modifie la valeur d'une cellule de la grille"""

        GridAvailableList.remove_possibility(cell, self._data[cell.line][cell.column])
        self._data[cell.line][cell.column] = None
