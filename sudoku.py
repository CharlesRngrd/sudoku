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
        self.count_values()

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

        self.check_unique_possibility()

        self.assert_finish()

    def count_values(self):
        count = len([cell for _, _, _, cell in self.get_cells(self.grid) if cell])
        print(f"Nombre de valeurs initiales : {count}")

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
        for i_line, line in enumerate(self.available[number]):
            line_values = []

            for i_cell, _ in enumerate(line):
                if line[i_cell] == number + 1:
                    line_values.append([i_line, i_cell])

            if len(line_values) == 1:
                self.grid[line_values[0][0]][line_values[0][1]] = number + 1
                return True

            self.disable_block(number, line_values)

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

    def check_unique_possibility(self):
        possibility = [[[] for _ in range(9)] for _ in range(9)]

        for number in range(9):
            for i_line, i_cell, _, cell in self.get_cells(self.available[number]):
                possibility[i_line][i_cell].append(cell)

        for i_line, i_cell, _, cell in self.get_cells(possibility):
            possible_values = [value for value in cell if value]

            if len(set(possible_values)) == 1:
                if self.grid[i_line][i_cell] == possible_values[0]:
                    return

                self.grid[i_line][i_cell] = possible_values[0]
                return True

    def assert_finish(self):
        error = False

        for line in self.grid:
            if len(set(line)) != 9:
                error = True

        for column in range(9):
            column_values = []
            for line in self.grid:
                column_values.append(line[column])

            if len(set(column_values)) != 9:
                error = True

        if error:
            self.print(self.grid)
            raise AssertionError("Sodoku resolution failed !")

        self.print(self.grid)
