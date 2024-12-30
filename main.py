import pygame

from cell import Cell
from board import Board
from font import derive_font
from constants import Constants

pygame.init()
pygame.font.init()

pygame.display.set_caption('Minesweeper')
window = pygame.display.set_mode((Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT))

running = True
playing = False
clock = pygame.time.Clock()

selected_cells = []
prev_click_info = None

buttons = []
selected_button = None

time = 0
result = 0

board = None

# bottom row cells not being recognized
def get_selected_cell(mouse_x, mouse_y):
	if mouse_x < Constants.PADDING_SIDE or mouse_x > Constants.DISPLAY_WIDTH - Constants.PADDING_SIDE:
		return None

	if mouse_y < Constants.PADDING_TOP or mouse_y > Constants.DISPLAY_HEIGHT - Constants.PADDING_BOTTOM:
		return None

	mouse_x -= Constants.PADDING_SIDE
	mouse_y -= Constants.PADDING_TOP

	cell_x = int(mouse_x // Constants.CELL_SIZE)
	cell_y = int(mouse_y // Constants.CELL_SIZE)

	return board.get_grid()[cell_y][cell_x]


def get_selected_button(mouse_x, mouse_y):
	for button in buttons:
		if mouse_x >= button.get_x() and mouse_x <= button.get_x() + button.get_width():
			if mouse_y >= button.get_y() and mouse_y <= button.get_y() + button.get_height():
				return button

	return None

def reset():
	global board, time, result, playing

	board = Board(Constants.GRID_SIZE, Constants.GRID_SIZE, Constants.NUMBER_OF_MINES)

	time = 0
	result = 0
	playing = False


reset()

while running:
	window.fill(Constants.BLACK)
	clock.tick(Constants.FPS)

	if playing:
		time += 1 / Constants.FPS

	# show time
	text = derive_font(24).render(str(int(time // 1)), 1, Constants.WHITE)
	text_x = Constants.DISPLAY_WIDTH - Constants.PADDING_SIDE - text.get_width()
	text_y = Constants.PADDING_TOP - text.get_height() - Constants.PADDING_BETWEEN

	window.blit(text, (text_x, text_y))

	# show mines left
	text = derive_font(24).render(str(board.get_mines()), 1, Constants.WHITE)
	text_x = Constants.PADDING_SIDE
	text_y = Constants.PADDING_TOP - text.get_height() - Constants.PADDING_BETWEEN

	window.blit(text, (text_x, text_y))

	# handle pygame events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			playing = False
		
		if event.type == pygame.MOUSEMOTION:
			x, y = event.pos
			selected_button = get_selected_button(x, y)

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			mouse_button = event.button # 1 = left click; 3 = right click

			selected_cell = get_selected_cell(x, y)
			selected_button = get_selected_button(x, y)

			if selected_cell:
				row, column = selected_cell.get_location()

				if mouse_button != 1 and mouse_button != 3:
					continue

				# left mouse click feature
				# uncover cell
				if mouse_button == 1:
					selected_cell.select()
					selected_cells.append(selected_cell)

				# right mouse click feature
				# flag cell
				if mouse_button == 3 and playing:
					board.flag(row, column)

				# right + left mouse click feature
				# indicate or reveal adjacent cells
				if selected_cell.get_status() == Cell.UNCOVERED and playing:
					if not prev_click_info:
						prev_click_info = (time, mouse_button)
						continue
					
					prev_time, prev_button = prev_click_info

					if mouse_button != prev_button and time - prev_time < 5 / 60:
						adj_cells = board.get_adj_cells(row, column)
						adj_flags = board.get_adj_flags(adj_cells=adj_cells)

						for n in adj_cells:
							n_row, n_column = n.get_location()

							if n.get_status() != Cell.COVERED:
								continue

							if len(adj_flags) == selected_cell.get_hint():
								board.uncover(n_row, n_column)
							else:
								n.select()
								selected_cells.append(n)

					prev_click_info = None

		if event.type == pygame.MOUSEBUTTONUP:
			x, y = event.pos
			mouse_button = event.button # 1 = left click; 3 = right click

			selected_cell = get_selected_cell(x, y)

			if selected_cell and selected_cell in selected_cells and len(selected_cells) == 1 and mouse_button == 1:
				row, column = selected_cell.get_location()
				board.uncover(row, column)
				playing = True

			for cell in selected_cells:
				cell.select()

			selected_cells.clear()


	board.draw(window)
	pygame.display.update()

pygame.quit()