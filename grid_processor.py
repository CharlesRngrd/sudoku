from __future__ import annotations
from typing import Dict, List, Set, TYPE_CHECKING

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

        while cell_queue := GridProcessor.remove_solved_cell():
            grid.move_solved_cell(cell_queue)

            cls.strategy_post_solved(grid, cell_queue)

            # Les stratégies suivantes sont très lentes,
            # donc elles sont jouées le plus tard possible.
            if len(cls.QUEUE):
                continue

            for _, number, iterable, cells in grid.iter_possibilities_wrapper():
                cls.strategy_single_possibility(cells, number)

                if len(cells) < 2:
                    continue

                cls.strategy_duplicate_pairs(cells)
                cls.strategy_aligned_possibility(grid, iterable, cells, number)

    @staticmethod
    def strategy_post_solved(grid: Grid, cell_queue: GridCell) -> None:
        """
        Stratégie qui consiste à :

        Supprimer une possibilité sur la ligne, la colonne et le bloc d'une cellule
        dès lors qu'elle a été résolue.
        Cette possibilité à supprimer correspond à la valeur de la cellule résolue.
        """

        for iterable in GridIterable:
            grid_cells = grid.possibilities[iterable][
                cell_queue.get_attribute(iterable)
            ]

            for grid_cell in grid_cells:
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

        Vérifier dans chaque ligne et chaque colonne si les possibilités sont présentes dans un seul bloc.
        Dans ce cas, aucune autre cellule de ce bloc ne peut contenir cette possibilité.
        """

        if iterable == GridIterable.BLOC:
            return

        if len({cell.bloc for cell in cells}) != 1:
            return

        cleanable_cells = {
            cell
            for cell in grid.iter_possibilities(
                GridIterable.BLOC, next(iter(cells)).bloc, number + 1
            )
            if cell not in cells
        }

        for cell in cleanable_cells:
            cell.drop_possibility(number + 1)

    @staticmethod
    def strategy_duplicate_pairs(cells: List[GridCell]) -> None:
        """
        Stratégie qui consiste à :

        Identifier 2 cellules dans une ligne, dans une colonne ou dans un bloc
        qui ont uniqument 2 valeurs possibles.
        Dans ce cas, ces valeurs peuvent être supprimée des autres cellules cet élément.
        """

        possibility_map: Dict[str, List[GridCell]] = {}

        for cell in cells:
            if len(cell.get_possibilities()) != 2:
                continue

            key = str(cell.get_possibilities())

            possibility_map.setdefault(key, [])
            possibility_map[key].append(cell)

        duplicates = [
            duplicate_cells
            for _, duplicate_cells in possibility_map.items()
            if len(duplicate_cells) == 2
        ]

        if not duplicates:
            return

        for duplicate_cells in duplicates:
            for cell in cells:
                if cell in duplicate_cells:
                    continue

                for possibility in duplicate_cells[0].get_possibilities():
                    cell.drop_possibility(possibility)
