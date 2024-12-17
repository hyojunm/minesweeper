import random, copy
from cell import Cell

class Board:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.uncovered = 0
        self.grid = []
        set_grid()

    def __repr__(self):
        pass

    def get_mines(self):
        return self.mines

    def get_uncovered(self):
        return self.uncovered
        
    def set_grid(self):
        for row in range(self.rows):
            self.grid.append([])

            for column in range(self.columns):
                self.grid[row].append(Cell(row, column))

    def set_mines(self, start_row, start_column):
        available = copy.deepcopy(self.grid)

        # first uncovered cell cannot be a mine
        del available[start_row][start_column]

	    for i in range(self.mines):
		    mine = random.choice(random.choice(available))
            row, column = mine.get_location()

		    self.grid[row][column].set_mine()
    		del available[row][column]
	
	    del available

    def get_adj_cells(self, row, column):
        adj_cells = []

        for i in range(9):
            adj_row = (i // 3) + (row - 1)
            adj_col = (i % 3) + (column - 1)
            
            if adj_row < 0 or adj_col < 0:
                continue

            if adj_row >= self.rows or adj_col >= self.columns:
                continue

            if adj_row == row and adj_col == column:
                continue

            adj_cells.append(self.grid[adj_row][adj_col])

        # adj_cells.sort(reverse=True, key=(lambda item : item.column)) # ???
        return adj_cells

    def get_adj_mines(self, row=0, column=0, adj_cells=None):
        if not adj_cells:
            adj_cells = self.get_adj_cells(row, column)

        return list(filter(lambda item : item.is_mine(), adj_cells))

    def uncover(self, row, column):
        if self.uncovered == 0:
            set_mines(row, column)

        c = self.grid[row][column]

        if not c.uncover():
            return

        self.uncovered += 1

        if c.get_status() == Cell.UNCOVERED_MINE:
            pass

        if c.get_status() == Cell.UNCOVERED_LAND:
            adj_cells = self.get_adj_cells(row, column)
            adj_mines = self.get_adj_mines(adj_cells=adj_cells)

            c.set_hint(len(adj_mines))

            if not len(adj_mines):
                for n in adj_cells:
                    if n.uncover():
                        self.uncovered += 1