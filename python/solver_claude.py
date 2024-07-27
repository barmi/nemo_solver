def read_puzzle(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()

	width, height = map(int, lines[0].split())
	row_clues = [tuple(map(int, line.split())) for line in lines[1:height + 1]]
	col_clues = [tuple(map(int, line.split())) for line in lines[height + 2:]]

	return width, height, row_clues, col_clues


def solve_line(line, blocks):
	n = len(line)
	m = len(blocks)

	if m == 0:
		return '0' * n
	if sum(blocks) + m - 1 > n:
		return None

	dp = [[False] * (n + 1) for _ in range(m + 1)]
	dp[0][0] = True

	for j in range(1, n + 1):
		dp[0][j] = dp[0][j - 1] and (line[j - 1] in '0?')

	for i in range(1, m + 1):
		for j in range(blocks[i - 1], n + 1):
			if j >= blocks[i - 1] and all(line[k] in '1?' for k in range(j - blocks[i - 1], j)):
				if j == blocks[i - 1] or line[j - blocks[i - 1] - 1] in '0?':
					dp[i][j] = dp[i - 1][j - blocks[i - 1] - 1] if j > blocks[i - 1] else dp[i - 1][0]

	if not dp[m][n]:
		return None

	result = ['?'] * n
	i, j = m, n
	while i > 0:
		while j > 0 and not dp[i][j]:
			j -= 1
		for k in range(j - blocks[i - 1], j):
			result[k] = '1'
		if j > blocks[i - 1]:
			result[j - blocks[i - 1] - 1] = '0'
		j -= blocks[i - 1] + 1
		i -= 1

	while j > 0:
		result[j - 1] = '0'
		j -= 1

	return ''.join(result)


def solve_nonogram(width, height, row_clues, col_clues):
	grid = [['?' for _ in range(width)] for _ in range(height)]

	changed = True
	while changed:
		changed = False
		for i in range(height):
			new_row = solve_line(''.join(grid[i]), row_clues[i])
			if new_row and ''.join(grid[i]) != new_row:
				grid[i] = list(new_row)
				changed = True

		for j in range(width):
			col = ''.join(grid[r][j] for r in range(height))
			new_col = solve_line(col, col_clues[j])
			if new_col and col != new_col:
				for r in range(height):
					grid[r][j] = new_col[r]
				changed = True

	return grid


def print_solution(grid):
	for row in grid:
		print(''.join('#' if cell == '1' else '.' if cell == '0' else '?' for cell in row))


def main():
	filename = '1-4302.jpeg.txt'
	width, height, row_clues, col_clues = read_puzzle(filename)
	solution = solve_nonogram(width, height, row_clues, col_clues)
	print_solution(solution)


if __name__ == "__main__":
	main()