class Game:
    GRID = [
        [5, 3, None, None, 7, None, None, None, None],
        [6, None, None, 1, 9, 5, None, None, None],
        [None, 9, 8, None, None, None, None, 6, None],
        # ---
        [8, None, None, None, 6, None, None, None, 3],
        [4, None, None, 8, None, 3, None, None, 1],
        [7, None, None, None, 2, None, None, None, 6],
        # ---
        [None, 6, None, None, None, None, 2, 8, None],
        [None, None, None, 4, 1, 9, None, None, 5],
        [None, None, None, None, 8, None, None, 7, 9],
    ]

    def __init__(self):
        self.available1 = [[1 for _ in range(9)] for _ in range(9)]

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

    def process1(self):
        next = True
        while next:
            self.disable1()
            next = self.check1()

    def check1(self):
        for i_line, line in enumerate(self.available1):
            line_values = []
            position = []

            for i_cell, _ in enumerate(line):
                if line[i_cell] == 1:
                    position = [i_line, i_cell]
                    line_values.append(1)

            if len(line_values) == 1:
                self.GRID[position[0]][position[1]] = 1
                print(f"Valeur 1 trouvée en position {position}")
                return True

        for column in range(9):
            column_values = []
            position = []

            for i_line, line in enumerate(self.available1):
                if line[column] == 1:
                    position = [i_line, column]
                    column_values.append(1)

            if len(column_values) == 1:
                self.GRID[position[0]][position[1]] = 1
                print(f"Valeur 1 trouvée en position {position}")
                return True

    def disable1(self):
        for _i_line, _i_cell, _, cell in self.get_cells(self.GRID):
            if cell:
                self.available1[_i_line][_i_cell] = None

            if cell != 1:
                continue

            for i_line, i_cell, _, _ in self.get_cells(self.GRID):
                same_line = i_line == _i_line
                same_col = i_cell == _i_cell
                same_block = i_line // 3 == _i_line // 3 and i_cell // 3 == _i_cell // 3

                if any([same_line, same_col, same_block]):
                    self.available1[i_line][i_cell] = None


game = Game()
game.process1()
game.print(game.GRID)
game.print(game.available1)
