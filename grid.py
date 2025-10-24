from typing import Generator, List, Tuple


class GridCell:
    def __init__(self, line: int, column: int, value: int = None) -> None:
        self.line = line
        self.column = column
        self.value = value


class Grid:
    def __init__(self, data: List[List[int]]) -> None:
        self._data = data

    def __repr__(self) -> str:
        """Affiche la grille avec un séparateur 3x3"""

        repr: List = []

        for index_line, cells in self.iter_lines():
            separator = ["-"] * len(cells)
            string = [cell.value or " " for cell in cells]

            for position in (6, 3):
                separator.insert(position, "|")
                string.insert(position, "|")

            if index_line in (3, 6):
                repr.append(" ".join(map(str, separator)))

            repr.append(" ".join(map(str, string)))

        return "\n".join(repr)

    def get_cell(self, position: GridCell) -> GridCell:
        """Retourne la valeur d'une cellule de la grille"""

        GridCell.value = self._data[position.line][position.column]

        return GridCell

    def update_cell(self, position: GridCell) -> None:
        """Modifie la valeur d'une cellule de la grille"""

        self._data[position.line][position.column] = position.value

    def iter_cells(self) -> Generator[GridCell, None, None]:
        """Retourne la liste complète des valeurs de la grille"""

        for _, cells in self.iter_lines():
            for cell in cells:
                yield cell

    def iter_lines(self) -> Generator[Tuple[int, List[GridCell]], None, None]:
        """Retourne la liste des lignes de la grille"""

        for index_line, line in enumerate(self._data):
            yield (
                index_line,
                [
                    GridCell(index_line, index_cell, cell)
                    for index_cell, cell in enumerate(line)
                ],
            )

    def count_values(self) -> int:
        """Retourne le nombre de valeurs remplies dans la grille"""

        return len([position.value for position in self.iter_cells() if position.value])

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
