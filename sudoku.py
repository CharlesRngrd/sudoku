class Game:
    STOP_PROCESS = False
    STOP_ITERATION = False

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.available = [
            [[number + 1 for _ in range(9)] for _ in range(9)] for number in range(9)
        ]

    def get_cells(self, element):
        for i_line, line in enumerate(element):
            for i_cell, cell in enumerate(line):
                yield i_line, i_cell, line, cell

    def print_grid(self, element):
        for index, line in enumerate(element):
            separator = ["-"] * len(line)
            to_print = [cell or " " for cell in line]

            for position in (6, 3):
                separator.insert(position, "|")
                to_print.insert(position, "|")

            if index in (3, 6):
                print(*separator)

            print(*to_print)

    def process(self):
        self.count_initial_values()

        while not self.STOP_PROCESS:
            self.STOP_PROCESS = True

            for number in range(9):
                self.STOP_ITERATION = False

                while not self.STOP_ITERATION:
                    self.disable_values(number)
                    self.check_lines(number)
                    self.check_columns(number)

                    if not self.STOP_ITERATION:
                        self.STOP_PROCESS = False

        self.assert_finish()

    def count_initial_values(self):
        count = len([cell for _, _, _, cell in self.get_cells(self.sudoku) if cell])
        print(f"\nNombre de valeurs initiales : {count}\n")

    def disable_values(self, number):
        for _i_line, _i_cell, _, cell in self.get_cells(self.sudoku):
            if cell:
                self.available[number][_i_line][_i_cell] = None

            if cell != number + 1:
                continue

            for i_line, i_cell, _, _ in self.get_cells(self.sudoku):
                same_line = i_line == _i_line
                same_col = i_cell == _i_cell
                same_block = i_line // 3 == _i_line // 3 and i_cell // 3 == _i_cell // 3

                if any([same_line, same_col, same_block]):
                    self.available[number][i_line][i_cell] = None

    def disable_block(self, number, line_values):
        if len(line_values) == 2 and line_values[0][1] // 3 == line_values[1][1] // 3:
            for i_line, i_cell, _, cell in self.get_cells(self.available[number]):
                if (
                    cell == number + 1
                    and i_line // 3 == line_values[0][0] // 3
                    and i_cell // 3 == line_values[0][1] // 3
                ):
                    self.available[number][i_line][i_cell] = None

            self.available[number][line_values[0][0]][line_values[0][1]] = number + 1
            self.available[number][line_values[1][0]][line_values[1][1]] = number + 1

    def check_lines(self, number):
        self.STOP_ITERATION = True

        for i_line, line in enumerate(self.available[number]):
            line_values = [
                [i_line, i_cell]
                for i_cell, _ in enumerate(line)
                if line[i_cell] == number + 1
            ]

            if len(line_values) == 1:
                self.sudoku[line_values[0][0]][line_values[0][1]] = number + 1

                self.STOP_ITERATION = False

            self.disable_block(number, line_values)

    def check_columns(self, number):
        self.STOP_ITERATION = True

        for column in range(9):
            column_values = [
                [i_line, column]
                for i_line, line in enumerate(self.available[number])
                if line[column] == number + 1
            ]

            if len(column_values) == 1:
                self.sudoku[column_values[0][0]][column_values[0][1]] = number + 1

                self.STOP_ITERATION = False

    def assert_finish(self):
        has_wrong_line = any([len(set(line)) != 9 for line in self.sudoku])

        has_wrong_column = any(
            [
                len(set([line[column] for line in self.sudoku])) != 9
                for column in range(9)
            ]
        )

        if has_wrong_line or has_wrong_column:
            self.print_grid(self.sudoku)
            raise AssertionError("Sodoku resolution failed !")

        self.print_grid(self.sudoku)
