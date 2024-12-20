import random

from cell import Cell

class Board:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.uncovered = 0
        self.grid = []
        self.set_grid()

    def __repr__(self):
        pass

    def get_mines(self):
        return self.mines

    def get_uncovered(self):
        return self.uncovered

    def get_grid(self):
        return self.grid
        
    def set_grid(self):
        for row in range(self.rows):
            self.grid.append([])

            for column in range(self.columns):
                self.grid[row].append(Cell(row, column))

    def set_mines(self, start_row, start_column):
        available = []

        for row in range(self.rows):
            available.append([])

            for column in range(self.columns):
                available[row].append(True)
               
        # first uncovered cell cannot be a mine
        available[start_row][start_column] = False

        # don't put mine adjacent to first uncovered cell
        for n in self.get_adj_cells(start_row, start_column):
            row, column = n.get_location()
            available[row][column] = False

        row = start_row
        column = start_column

        for i in range(self.mines):
            while not available[row][column]:
                row = random.randint(0, self.rows - 1)
                column = random.randint(0, self.columns - 1)

            self.grid[row][column].set_mine()
            available[row][column] = False

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

    def get_adj_flags(self, row=0, column=0, adj_cells=None):
        if not adj_cells:
            adj_cells = self.get_adj_cells(row, column)

        return list(filter(lambda item : item.status == FLAGGED, adj_cells))

    def uncover(self, row, column):
        if self.uncovered == 0:
            self.set_mines(row, column)

        c = self.grid[row][column]

        if not c.uncover():
            return

        self.uncovered += 1
        
        if c.is_mine():
            pass

        adj_cells = self.get_adj_cells(row, column)
        adj_mines = self.get_adj_mines(adj_cells=adj_cells)

        c.set_hint(len(adj_mines))

        if not len(adj_mines):
            for n in adj_cells:
                next_row, next_col = n.get_location()
                self.uncover(next_row, next_col)

    def flag(self, row, column):
        c = self.grid[row][column]

        if c.get_status() == Cell.UNCOVERED:
            return

        if c.flag():
            self.mines -= 1
        else:
            self.mines += 1