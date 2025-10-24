from grid import Grid, GridCell


class Game:
    STOP_PROCESS = False
    STOP_ITERATION = False

    def __init__(self, sudoku):
        self.sudoku = Grid(sudoku)
        self.available = [
            [[number + 1 for _ in range(9)] for _ in range(9)] for number in range(9)
        ]

    def get_cells(self, element):
        for i_line, line in enumerate(element):
            for i_cell, cell in enumerate(line):
                yield i_line, i_cell, line, cell

    def process(self):
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

            self.disable_values(number)
            if self.check_unique_possibility():
                self.STOP_ITERATION = False

        self.assert_finish()

    def disable_values(self, number):
        for position in self.sudoku.iter_cells():
            if position.value:
                self.available[number][position.line][position.column] = None

            if position.value != number + 1:
                continue

            for position_bis in self.sudoku.iter_cells():
                same_line = position_bis.line == position.line
                same_col = position_bis.column == position.column
                same_block = (
                    position_bis.line // 3 == position.line // 3
                    and position_bis.column // 3 == position.column // 3
                )

                if any([same_line, same_col, same_block]):
                    self.available[number][position_bis.line][position_bis.column] = (
                        None
                    )

    def check_lines(self, number):
        for i_line, line in enumerate(self.available[number]):
            line_values = [
                [i_line, i_cell]
                for i_cell, _ in enumerate(line)
                if line[i_cell] == number + 1
            ]

            if len(line_values) == 1:
                self.sudoku.update_cell(
                    GridCell(line_values[0][0], line_values[0][1], number + 1)
                )

                return True

    def check_columns(self, number):
        for column in range(9):
            column_values = [
                [i_line, column]
                for i_line, line in enumerate(self.available[number])
                if line[column] == number + 1
            ]

            if len(column_values) == 1:
                self.sudoku.update_cell(
                    GridCell(column_values[0][0], column_values[0][1], number + 1)
                )

                return True

    def check_blocs(self, number):
        for line_bloc in range(3):
            for column_bloc in range(3):
                block_values = []

                for i_line, i_cell, _, cell in self.get_cells(self.available[number]):
                    if (
                        cell == number + 1
                        and i_line // 3 == line_bloc
                        and i_cell // 3 == column_bloc
                    ):
                        block_values.append([i_line, i_cell])

                if len(block_values) > 1:
                    if len(set([value[0] for value in block_values])) == 1:
                        for i_line, i_cell, _, _ in self.get_cells(
                            self.available[number]
                        ):
                            if i_line == block_values[0][0]:
                                if (
                                    self.available[number][i_line][i_cell] is not None
                                    and i_cell // 3 != column_bloc
                                ):
                                    self.available[number][i_line][i_cell] = None

                                    return True

                    if len(set([value[1] for value in block_values])) == 1:
                        for i_line, i_cell, _, _ in self.get_cells(
                            self.available[number]
                        ):
                            if i_cell == block_values[0][1]:
                                if (
                                    self.available[number][i_line][i_cell] is not None
                                    and i_line // 3 != line_bloc
                                ):
                                    self.available[number][i_line][i_cell] = None

                                    return True

                if len(block_values) == 1:
                    self.sudoku.update_cell(
                        GridCell(block_values[0][0], block_values[0][1], number + 1)
                    )

                    return True

    def check_unique_possibility(self):
        possibility = [[[] for _ in range(9)] for _ in range(9)]

        for number in range(9):
            for i_line, i_cell, _, cell in self.get_cells(self.available[number]):
                if cell is None:
                    continue

                possibility[i_line][i_cell].append(cell)

        for i_line, i_cell, _, cell in self.get_cells(possibility):
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
