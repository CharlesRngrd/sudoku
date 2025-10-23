class Game:
    def __init__(self, grid):
        self.grid = grid
        self.available = [
            [[number + 1 for _ in range(9)] for _ in range(9)] for number in range(9)
        ]

    def get_cells(self, element):
        for i_line, line in enumerate(element):
            for i_cell, cell in enumerate(line):
                yield i_line, i_cell, line, cell

    def print(self, element):
        for index, line in enumerate(element):
            if index in (0, 3, 6):
                print(*["- " * (len(line) + 2)])

            _display = [cell or " " for cell in line]
            for position in (6, 3):
                _display.insert(position, "|")

            print(*_display)

            if index == len(line) - 1:
                print(*["- " * (len(line) + 2)])

    def process(self):
        global_next = True
        while global_next:
            global_next = False

            for number in range(9):
                next = True
                while next:
                    self.disable(number)
                    next = any(
                        [
                            self.check_lines(number),
                            self.check_columns(number),
                        ]
                    )

                    if next:
                        global_next = True

    def disable(self, number):
        for _i_line, _i_cell, _, cell in self.get_cells(self.grid):
            if cell:
                self.available[number][_i_line][_i_cell] = None

            if cell != number + 1:
                continue

            for i_line, i_cell, _, _ in self.get_cells(self.grid):
                same_line = i_line == _i_line
                same_col = i_cell == _i_cell
                same_block = i_line // 3 == _i_line // 3 and i_cell // 3 == _i_cell // 3

                if any([same_line, same_col, same_block]):
                    self.available[number][i_line][i_cell] = None

    def check_lines(self, number):
        for i_line, line in enumerate(self.available[number]):
            line_values = []
            position = []

            for i_cell, _ in enumerate(line):
                if line[i_cell] == number + 1:
                    position = [i_line, i_cell]
                    line_values.append(number + 1)

            if len(line_values) == 1:
                self.grid[position[0]][position[1]] = number + 1
                return True

    def check_columns(self, number):
        for column in range(9):
            column_values = []
            position = []

            for i_line, line in enumerate(self.available[number]):
                if line[column] == number + 1:
                    position = [i_line, column]
                    column_values.append(1)

            if len(column_values) == 1:
                self.grid[position[0]][position[1]] = number + 1
                return True

    def assert_finish(self):
        for line in self.grid:
            assert len(set(line)) == 9

        for column in range(9):
            column_values = []
            for line in self.grid:
                column_values.append(line[column])

            assert len(set(column_values)) == 9
