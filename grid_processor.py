from __future__ import annotations
from typing import List, Set, TYPE_CHECKING
from grid_iterable import GridIterable

if TYPE_CHECKING:
    from grid import Grid
    from grid_cell import GridCell


class GridProcessor:
    """Responsable de la résolution du Sudoku"""

    QUEUE: Set[GridCell] = set()

    @classmethod
    def add_solved_cell(cls, grid_cell: GridCell) -> None:
        """Ajoute une cellule résolue"""

        cls.QUEUE.add(grid_cell)

    @classmethod
    def remove_solved_cell(cls) -> GridCell:
        """Supprime une cellule résolue"""

        if len(cls.QUEUE):
            return cls.QUEUE.pop()

    @classmethod
    def execute(cls, grid: Grid) -> None:
        """
        Execute pour chaque ligne, chaque colonne et chaque bloc les stratégies.
        Ces stratégies sont jouées pour chaque nombre.

        En appliquant une stratégie sur une cellule résolue,
        les possibilités vont se réduire sur d'autres cellules.
        Cela peut déclancher d'autres résolutions en chaine.
        """

        print(f"Nombre de valeurs initiales : {grid.count_values()}")

        while cell_queue := GridProcessor.remove_solved_cell():
            cls.strategy_post_solved(grid, cell_queue)

            # Les stratégies suivantes sont très lentes,
            # donc elles sont jouées le plus tard possible.
            if len(cls.QUEUE):
                continue

            for position in range(9):
                for number in range(9):
                    for iterable in GridIterable:
                        cells = {
                            cell
                            for cell in grid.iter_element(iterable, position)
                            if (number + 1) in cell.get_possibilities()
                        }

                        if any({cell for cell in cells if cell.solved_value}):
                            continue

                        cls.strategy_single_possibility(cells, number)
                        cls.strategy_aligned_possibility(grid, iterable, cells, number)

        print(f"Nombre de valeurs finales : {grid.count_values()}")
        print(grid)
        print(grid.check_solved())

    @staticmethod
    def strategy_post_solved(grid: Grid, cell_queue: GridCell) -> None:
        """
        Stratégie qui consiste à :

        Supprimer une possibilité sur la ligne, la colonne et le bloc d'une cellule
        dès lors qu'elle a été résolue.
        Cette possibilité à supprimer correspond à la valeur de la cellule résolue.
        """

        for grid_cell in grid.iter_grid():
            drop_conditions = {
                cell_queue.line == grid_cell.line,
                cell_queue.column == grid_cell.column,
                cell_queue.bloc == grid_cell.bloc,
            }

            if any(drop_conditions):
                grid_cell.drop_possibility(cell_queue.solved_value)

    @staticmethod
    def strategy_single_possibility(cells: List[GridCell], number: int) -> None:
        """
        Stratégie qui consiste à :

        Vérifier dans chaque ligne, colonne et bloc si une possibilité est présente
        une seule fois.
        Dans ce cas, la cellule est résolue.
        """

        if len(cells) == 1:
            next(iter(cells)).solve_possibility(number + 1)

    @staticmethod
    def strategy_aligned_possibility(
        grid: Grid, iterable: GridIterable, cells: List[GridCell], number: int
    ) -> None:
        """
        Stratégie qui consiste à :

        Vérifier dans chaque ligne et chaque colonne si les possibilités sont alignées
        et présentes dans un seul bloc.
        Dans ce cas, aucune autre cellule de ce bloc ne peut contenir cette possibilité.
        """

        if len(cells) > 1:
            if iterable not in (GridIterable.LINE, GridIterable.COLUMN):
                return

            if len({cell.bloc for cell in cells}) != 1:
                return

            cleanable_cells = {
                cell
                for cell in grid.iter_element(GridIterable.BLOC, next(iter(cells)).bloc)
                if (number + 1) in cell.get_possibilities()
                and cell.get_attribute(iterable)
                != next(iter(cells)).get_attribute(iterable)
            }

            for cell in cleanable_cells:
                cell.drop_possibility(number + 1)
