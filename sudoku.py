from typing import List
from grid import Grid, GridAvailableList, GridAvailableSingle, GridCell


class Game:
    STOP_PROCESS: bool = False
    STOP_ITERATION: bool = False

    def __init__(self, sudoku):
        self.sudoku: Grid = Grid(sudoku)
        self.available: List[GridAvailableSingle] = [
            GridAvailableSingle([[number + 1 for _ in range(9)] for _ in range(9)])
            for number in range(9)
        ]

        self.available_liste = GridAvailableList()
        self.available_liste.define_possibilities()

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

            for number in range(9):
                self.disable_values(number)

            if self.check_unique_possibility():
                self.STOP_PROCESS = False

        self.assert_finish()

    def disable_values(self, number: int) -> None:
        """Actualise les place indisponibles pour une valeur observée"""

        for cell in self.sudoku.iter_cells():
            # S'il y a une valeur dans le sudoku, alors la place n'est plus disponible :
            if cell.value:
                self.available[number].reset_cell(cell)

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
                    self.available[number].reset_cell(cell_bis)

    def matching_cells(self, cells: List[GridCell], number: int) -> List[GridCell]:
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
            if len(cells_valid) == 1:
                cells_valid[0].value = number + 1
                self.sudoku.update_cell(cells_valid[0])

                for cell in cells:
                    self.available[number].reset_cell(cell)

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
                        self.available[number].reset_cell(cells_bis)

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
                        self.available[number].reset_cell(cells_bis)

                        return True

    def check_unique_possibility(self) -> bool:
        """Vérifie s'il y a des cellules avec une seule valeur possible"""

        update = False

        for cell in self.available_liste.iter_cells():
            if len(cell.value) == 1:
                cell.value = cell.value[0]
                if not self.sudoku.get_cell(cell).value:
                    self.sudoku.update_cell(cell)
                    update = True

        return update

    def assert_finish(self):
        if not (
            self.sudoku.check_columns_completed()
            and self.sudoku.check_columns_completed()
        ):
            print(
                f"Nombre de valeurs finales : {self.sudoku.count_values()} | Failure :(\n"
            )

            print(self.available_liste)

        print(self.sudoku)
