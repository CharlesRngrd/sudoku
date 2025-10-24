from typing import List
from grid import Grid, GridCell


class Game:
    STOP_PROCESS = False
    STOP_ITERATION = False

    def __init__(self, sudoku):
        self.sudoku: Grid = Grid(sudoku)
        self.available: List[Grid] = [
            Grid([[number + 1 for _ in range(9)] for _ in range(9)])
            for number in range(9)
        ]

    def process(self) -> None:
        """Processus principal"""

        print(f"\nNombre de valeurs initiales : {self.sudoku.count_values()}\n")

        while not self.STOP_PROCESS:
            self.STOP_PROCESS = True

            for number in range(9):
                self.STOP_ITERATION = False

                while not self.STOP_ITERATION:
                    self.disable_values(number)

                    self.STOP_ITERATION = not any(
                        [
                            self.check_lines(number),
                            self.check_columns(number),
                            self.check_blocs(number),
                        ]
                    )

                    if not self.STOP_ITERATION:
                        self.STOP_PROCESS = False

            # self.disable_values(number)
            # if self.check_unique_possibility():
            #     self.STOP_ITERATION = False

        self.assert_finish()

    def disable_values(self, number: int) -> None:
        """Actualise les place indisponibles pour une valeur observée"""

        for cell in self.sudoku.iter_cells():
            # S'il y a une valeur dans le sudoku, alors la place n'est plus disponible :
            if cell.value:
                self.available[number].update_cell(cell.drop_value())

            # Si cette valeur n'est pas celle observée, alors on arrête là :
            if cell.value != number + 1:
                continue

            # Si cette valeur est celle observée,
            # alors la valeur n'est plus disponible dans la ligne, la colonne et le bloc :
            for cell_bis in self.available[number].iter_cells():
                if any(
                    [
                        cell_bis.line == cell.line,
                        cell_bis.column == cell.column,
                        (
                            cell_bis.get_bloc_line() == cell.get_bloc_line()
                            and cell_bis.get_bloc_col() == cell.get_bloc_col()
                        ),
                    ]
                ):
                    self.available[number].update_cell(cell_bis.drop_value())

    def matching_cells(self, cells, number: int) -> List[GridCell]:
        """Retourne la liste des cellules qui ont une valeur donnée"""

        return [cell for cell in cells if cell.value == number + 1]

    def check_lines(self, number: int) -> bool:
        """
        Vérifie dans chaque ligne :
        - Si la valeur observée n'a qu'une place disponible, alors on actualise le sudoku.
        """

        for cells in self.available[number].iter_lines():
            cells_valid = self.matching_cells(cells, number)

            if len(cells_valid) == 1:
                self.sudoku.update_cell(cells_valid[0])

                return True

    def check_columns(self, number: int) -> bool:
        """
        Vérifie dans chaque colonne :
        - Si la valeur observée n'a qu'une place disponible, alors on actualise le sudoku.
        """

        for cells in self.available[number].iter_columns():
            cells_valid = self.matching_cells(cells, number)

            if len(cells_valid) == 1:
                self.sudoku.update_cell(cells_valid[0])

                return True

    def check_blocs(self, number: int) -> bool:
        """
        Vérifie dans chaque bloc :
        - Si la valeur observée n'a qu'une place disponible, alors on actualise le sudoku.
        - Si la valeur obserée a plusieurs places disponibles mais uniquement que ces places sont alignées,
          alors on désactive cette valeur dans le reste du bloc.
        """

        for cells in self.available[number].iter_blocs():
            cells_valid = self.matching_cells(cells, number)

            # Si la valeur observée n'a qu'une place disponible, alors on actualise le sudoku :
            if len(cells) == 1:
                cells[0].value = number + 1
                self.sudoku.update_cell(cells[0])

                return True

            # S'il y a plusieurs fois la valeur observée dans le bloc et qu'elles sont sur une seule ligne,
            # alors on désactive cette valeur dans le reste du bloc :
            if len(set([cell.line for cell in cells_valid])) == 1:
                for cells_bis in self.available[number].iter_cells():
                    if (
                        cells_bis.value
                        and cells_bis.line == cells_valid[0].line
                        and cells_bis.get_bloc_col() != cells_valid[0].get_bloc_col()
                    ):
                        self.available[number].update_cell(cells_bis.drop_value())

                        return True

            # S'il y a plusieurs fois la valeur observée dans le bloc et qu'elles sont sur une seule colonne,
            # alors on désactive cette valeur dans le reste du bloc :
            if len(set([cell.column for cell in cells])) == 1:
                for cells_bis in self.available[number].iter_cells():
                    if (
                        cells_bis.value
                        and cells_bis.column == cells_valid[0].column
                        and cells_bis.get_bloc_line() != cells_valid[0].get_bloc_line()
                    ):
                        self.available[number].update_cell(cells_bis.drop_value())

                        return True

    def check_unique_possibility(self):
        def get_cells(element):
            for i_line, line in enumerate(element):
                for i_cell, cell in enumerate(line):
                    yield i_line, i_cell, line, cell

        possibility = [[[] for _ in range(9)] for _ in range(9)]

        for number in range(9):
            for cell in self.available[number].iter_cells():
                if not cell.value:
                    continue

                possibility[cell.line][cell.column].append(cell.value)

        for i_line, i_cell, _, cell in get_cells(possibility):
            if len(set(cell)) == 1:
                if not self.sudoku.get_cell(GridCell(i_line, i_cell)):
                    self.sudoku.update_cell(i_line, i_cell, cell[0])
                    return True

    def assert_finish(self):
        if not (
            self.sudoku.check_columns_completed()
            and self.sudoku.check_columns_completed()
        ):
            print("Sodoku resolution failed !")

        print(self.sudoku)
