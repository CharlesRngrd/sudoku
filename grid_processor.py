from __future__ import annotations
from typing import List, TYPE_CHECKING
from grid_iterable import GridIterable

if TYPE_CHECKING:
    from grid import Grid
    from grid_cell import GridCell


class GridProcessor:
    """Responsable de la résolution du Sudoku"""

    QUEUE: List[GridCell] = []

    @classmethod
    def add_solved_cell(cls, grid_cell: GridCell) -> None:
        """Ajoute une cellule résolue"""

        cls.QUEUE.append(grid_cell)

    @classmethod
    def remove_solved_cell(cls) -> GridCell:
        """Supprime une cellule résolue"""

        if len(cls.QUEUE):
            return cls.QUEUE.pop()

    @classmethod
    def execute(cls, grid: Grid) -> None:
        """
        Execute les stratégies associées aux cellules résolues.
        En appliquant une stratégie sur une cellule résolue, les possibilités vont se réduire sur d'autres cellules.
        Cela peut déclancher d'autres résolutions en chaine.
        """

        print(f"Nombre de valeurs initiales : {grid.count_values()}")

        while cell_queue := GridProcessor.remove_solved_cell():
            cls.strategy_post_solved(grid, cell_queue)

            for position in range(9):
                for number in range(9):
                    for iterable in GridIterable:
                        cls.strategy_single_possibility(
                            grid, position, number, iterable
                        )

        print(f"Nombre de valeurs finales : {grid.count_values()}")
        print(grid)
        print(grid.check_solved())

    @staticmethod
    def strategy_post_solved(grid: Grid, cell_queue: GridCell) -> None:
        """
        Stratégie qui consiste à :
        Supprimer une possibilité sur la ligne, la colonne et le bloc d'une cellule dès lors qu'elle a été résolue.
        Cette possibilité à supprimer correspond à la valeur de la cellule résolue.
        """

        for grid_cell in grid.iter_grid():
            drop_conditions = [
                cell_queue.line == grid_cell.line,
                cell_queue.column == grid_cell.column,
                cell_queue.bloc == grid_cell.bloc,
            ]

            if any(drop_conditions):
                grid_cell.drop_possibility(cell_queue.get_possibilities()[0])

    @staticmethod
    def strategy_single_possibility(
        grid: Grid, position: int, number: int, iterable: GridIterable
    ) -> None:
        """
        Stratégie qui consiste à :
        Vérifier dans chaque ligne, colonne et bloc si une possibilité est présente une seule fois.
        Dans ce cas, la cellule est résolue.
        """

        cells = [
            cell
            for cell in grid.iter_element(iterable, position)
            if (number + 1) in cell.get_possibilities()
        ]

        if any([cell for cell in cells if cell.is_solved]):
            return

        if len(cells) == 1:
            cells[0].solve_possibility(number + 1)
