import random
import pygame
import multiprocessing

from cell import Cell
from constants import Constants

class Board:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.total_land = rows * columns - mines
        self.uncovered = 0
        self.uncovered_mines = 0
        self.grid = []
        self.set_grid()

    def __repr__(self):
        pass

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def get_mines(self):
        return self.mines

    def get_uncovered(self):
        return self.uncovered

    def get_grid(self):
        return self.grid

    def is_win(self):
        return self.uncovered == self.total_land

    def is_lose(self):
        return self.uncovered_mines > 0
        
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

        return adj_cells

    def get_adj_mines(self, row=0, column=0, adj_cells=None):
        if not adj_cells:
            adj_cells = self.get_adj_cells(row, column)

        return list(filter(lambda item : item.is_mine(), adj_cells))

    def get_adj_flags(self, row=0, column=0, adj_cells=None):
        if not adj_cells:
            adj_cells = self.get_adj_cells(row, column)

        return list(filter(lambda item : item.status == Cell.FLAGGED, adj_cells))

    def uncover(self, row, column):
        if self.uncovered == 0:
            self.set_mines(row, column)

        c = self.grid[row][column]
        
        if not c.uncover():
            return

        self.uncovered += 1

        if c.is_mine():
            self.uncovered_mines += 1
            return

        adj_cells = self.get_adj_cells(row, column)
        adj_mines = self.get_adj_mines(adj_cells=adj_cells)

        c.set_hint(len(adj_mines))

        if not len(adj_mines):
            for n in adj_cells:
                next_row, next_col = n.get_location()
                self.uncover(next_row, next_col)

    def flag(self, row, column):
        c = self.grid[row][column]
        status = c.flag()

        if status == 1:
            self.mines += 1

        if status == 2:
            self.mines -= 1

    def draw(self, window):
        board_x = Constants.PADDING_SIDE - 5
        board_y = Constants.PADDING_TOP - 5
        board_size = Constants.GRID_SIZE * Constants.CELL_SIZE + 10

        # repaint board rectangle
        fill_rect = pygame.Rect(board_x, board_y, board_size, board_size)
        pygame.draw.rect(window, Constants.WHITE, fill_rect)

        fill_rect = pygame.Rect(board_x + 5, board_y + 5, board_size - 10, board_size - 10)
        pygame.draw.rect(window, Constants.BLACK, fill_rect)

        # processes = []

        for row in self.grid:
            for cell in row:
                cell.draw(window)
                # process = multiprocessing.Process(target=cell.draw, args=[window])
                # process.start()

                # processes.append(process)
                # maybe add threading here

        # for process in processes:
        #     process.join()