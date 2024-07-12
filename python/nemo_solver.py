class NonogramSolver:
    def __init__(self, row_clues, col_clues):
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.height = len(row_clues)
        self.width = len(col_clues)
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def is_valid_row(self, row, clue, row_idx):
        filled_blocks = ''.join(self.grid[row_idx]).split()
        filled_blocks = [len(block) for block in filled_blocks if block]
        return filled_blocks == clue

    def is_valid_col(self, col, clue, col_idx):
        filled_blocks = ''.join([self.grid[row_idx][col_idx] for row_idx in range(self.height)]).split()
        filled_blocks = [len(block) for block in filled_blocks if block]
        return filled_blocks == clue

    def solve(self):
        changed = True
        while changed:
            changed = False
            for row_idx, clue in enumerate(self.row_clues):
                if self.update_row(row_idx, clue):
                    changed = True
            for col_idx, clue in enumerate(self.col_clues):
                if self.update_col(col_idx, clue):
                    changed = True
        return self.grid

    def update_row(self, row_idx, clue):
        original_row = self.grid[row_idx][:]
        possible_row = self.fill_line(self.width, clue, self.grid[row_idx])
        self.grid[row_idx] = possible_row
        return original_row != possible_row

    def update_col(self, col_idx, clue):
        original_col = [self.grid[row_idx][col_idx] for row_idx in range(self.height)]
        col = [self.grid[row_idx][col_idx] for row_idx in range(self.height)]
        possible_col = self.fill_line(self.height, clue, col)
        for row_idx in range(self.height):
            self.grid[row_idx][col_idx] = possible_col[row_idx]
        return original_col != possible_col

    def fill_line(self, length, clue, line):
        possibilities = self.get_possibilities(length, clue)
        result = [' '] * length
        for pos in possibilities:
            for idx in range(length):
                if line[idx] == ' ' or line[idx] == pos[idx]:
                    result[idx] = pos[idx]
        return result

    def get_possibilities(self, length, clue):
        if not clue:
            return [[' '] * length]
        if sum(clue) + len(clue) - 1 > length:
            return []

        first, *rest = clue
        possibilities = []
        for start in range(length - sum(clue) - len(clue) + 2):
            prefix = [' '] * start + ['#'] * first
            for suffix in self.get_possibilities(length - len(prefix) - 1, rest):
                possibilities.append(prefix + [' '] + suffix)
        return possibilities

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    dimensions = list(map(int, lines[0].split()))
    row_clues = []
    col_clues = []

    i = 1
    for _ in range(dimensions[0]):
        row_clues.append(list(map(int, lines[i].split())))
        i += 1

    for _ in range(dimensions[1]):
        col_clues.append(list(map(int, lines[i].split())))
        i += 1

    return row_clues, col_clues

# Example usage:
file_path = 'input.txt'  # Input file path
row_clues, col_clues = parse_input(file_path)
solver = NonogramSolver(row_clues, col_clues)
solution = solver.solve()
print_grid(solution)
