class NonogramSolver:
    def __init__(self, row_clues, col_clues):
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.height = len(row_clues)
        self.width = len(col_clues)
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.row_possibilities = [self.get_possibilities(self.width, clue) for clue in self.row_clues]
        self.col_possibilities = [self.get_possibilities(self.height, clue) for clue in self.col_clues]

    def solve(self):
        self.fill_determined_cells()
        if not self.is_solved():
            self.backtrack(0, 0)
        return self.grid

    def is_solved(self):
        for row in self.grid:
            if ' ' in row:
                return False
        return True

    def fill_determined_cells(self):
        for row_idx, row_pos in enumerate(self.row_possibilities):
            self.grid[row_idx] = self.intersection(row_pos)
        for col_idx, col_pos in enumerate(self.col_possibilities):
            col_values = self.intersection(col_pos)
            for row_idx in range(self.height):
                if col_values[row_idx] != ' ':
                    self.grid[row_idx][col_idx] = col_values[row_idx]

    def intersection(self, possibilities):
        transposed = list(map(list, zip(*possibilities)))
        result = []
        for values in transposed:
            if all(val == values[0] for val in values):
                result.append(values[0])
            else:
                # 'X'로 마킹
                result.append('X' if 'X' in values else ' ')
        return result

    def backtrack(self, row_idx, col_idx):
        if row_idx == self.height:
            return True
        if col_idx == self.width:
            return self.backtrack(row_idx + 1, 0)
        if self.grid[row_idx][col_idx] != ' ':
            return self.backtrack(row_idx, col_idx + 1)

        for val in ['#', ' ']:
            self.grid[row_idx][col_idx] = val
            if self.is_valid():
                if self.backtrack(row_idx, col_idx + 1):
                    return True
        self.grid[row_idx][col_idx] = ' '
        return False

    def is_valid(self):
        for row_idx in range(self.height):
            row = self.grid[row_idx]
            if not self.matches_clue(row, self.row_clues[row_idx]):
                return False
        for col_idx in range(self.width):
            col = [self.grid[row_idx][col_idx] for row_idx in range(self.height)]
            if not self.matches_clue(col, self.col_clues[col_idx]):
                return False
        return True

    def matches_clue(self, line, clue):
        blocks = ''.join(line).replace('X', ' ').split()
        blocks = [len(block) for block in blocks if block == '#']
        return blocks == clue

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

    dimensions = list(map(int, lines[0].strip().split()))
    row_clues = []
    col_clues = []

    i = 1
    for _ in range(dimensions[0]):
        row_clues.append(list(map(int, lines[i].strip().split())))
        i += 1

    i += 1
    for _ in range(dimensions[1]):
        col_clues.append(list(map(int, lines[i].strip().split())))
        i += 1

    return row_clues, col_clues

# Example usage:
file_path = '1-4302.jpeg.txt'  # Input file path
row_clues, col_clues = parse_input(file_path)
solver = NonogramSolver(row_clues, col_clues)
solution = solver.solve()
print_grid(solution)
