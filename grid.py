class Grid:
    def __init__(self, data) -> None:
        self._data = data

    def print(self) -> None:
        """Affiche la grille avec un séparateur 3X3"""

        for index, line in enumerate(self._data):
            separator = ["-"] * len(line)
            to_print = [cell or " " for cell in line]

            for position in (6, 3):
                separator.insert(position, "|")
                to_print.insert(position, "|")

            if index in (3, 6):
                print(*separator)

            print(*to_print)

    def get_cell(self, index_line, index_column):
        """Retourne la valeur d'une cellule de la grille"""

        return self._data[index_line][index_column]

    def update_cell(self, index_line, index_column, value):
        """Modifie la valeur d'une cellule de la grille"""

        self._data[index_line][index_column] = value

    def iter_cells(self):
        """Retourne la liste complète des valeurs de la grille"""

        for i_line, line in enumerate(self._data):
            for i_cell, cell in enumerate(line):
                yield i_line, i_cell, line, cell

    def count_values(self):
        """Retourne le nombre de valeurs remplies dans la grille"""

        return len([cell for _, _, _, cell in self.iter_cells() if cell])

    def check_lines_completed(self):
        """Vérifie si toutes les lignes contiennent tous les chiffres de 1 à 9"""

        return all([len(set(line)) == 9 for line in self._data])

    def check_columns_completed(self):
        """Vérifie si toutes les colonnes contiennent tous les chiffres de 1 à 9"""

        return all(
            [
                len(set([line[column] for line in self._data])) == 9
                for column in range(9)
            ]
        )
