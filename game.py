# Import required modules
import random, copy

# Board list containing all of the cells
board = []

# Cell class for each "block" in the game
class Cell:
	# Set cell properties
	def __init__(self, row, column):
		self.row = row
		self.column = column
		self.value = " "
		self.uncovered = False
		self.flagged = False
		self.is_mine = False


	# String representation of the class
	def __repr__(self):
		return f"{self.column}, {self.row}"


	# Uncover this cell (if no mines around it, uncover adjacent cells)
	def uncover(self):
		if self.uncovered or self.flagged:
			return

		self.uncovered = True

		if self.is_mine:
			self.value = "M"
		else:
			adj_cells = self.get_adj_cells()
			adj_mines = self.get_adj_mines(adj_cells=adj_cells)
			
			if len(adj_mines):
				self.value = str(len(adj_mines))
			else:
				for cell in adj_cells:
					if not cell.uncovered:
						cell.uncover()


	# Get adjacent (surrounding) cells
	def get_adj_cells(self):
		adj_cells = []

		for i in range(9):
			try:
				row = (i // 3) + (self.row - 1)
				column = (i % 3) + (self.column - 1)

				if row < 0 or column < 0:
					raise IndexError()

				cell = board[row][column]
				adj_cells.append(cell)
			except IndexError as e:
				continue

		adj_cells.sort(reverse=True, key=(lambda item : item.column))
		return adj_cells


	# Get adjacent (surrounding) mines
	def get_adj_mines(self, adj_cells=None):
		if not adj_cells:
			adj_cells = self.get_adj_cells()

		return list(filter(lambda item : item.is_mine, adj_cells))


# Fill in the board list with empty cells based on selected difficulty
def create_cells(difficulty):
	board.clear()
	
	for row in range(difficulty["cells"]):
		board.append([])

		for column in range(difficulty["cells"]):
			board[row].append(Cell(row, column))


# Create the cells and determine mines based on selected difficulty
def start_game(start_row, start_column, difficulty):
	available = copy.deepcopy(board)

	for cell in available[start_row][start_column].get_adj_cells():
		del available[cell.row][cell.column]

	for i in range(difficulty["mines"]):
		row = random.choice(available)
		mine = random.choice(row)
		board[mine.row][mine.column].is_mine = True
		del available[available.index(row)][row.index(mine)]
	
	del available

	board[start_row][start_column].uncover()
