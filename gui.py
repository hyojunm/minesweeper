import pygame

from setting import Setting
from board import Board
from cell import Cell
from button import Button
from font import derive_font

pygame.init()
pygame.font.init()

FPS = 60

SCALE = 1

DISPLAY_WIDTH = SCALE * 800
DISPLAY_HEIGHT = SCALE * 900

PADDING_SIDE = SCALE * 50
PADDING_TOP = SCALE * 100
PADDING_BETWEEN = SCALE * 30

BUTTON_WIDTH = SCALE * 200
BUTTON_HEIGHT = SCALE * 40
BUTTON_BORDER_SIZE = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (180, 180, 180)
RED = (240, 16, 0)
BROWN = (82, 60, 0)

DIFFICULTY_SETTINGS = []
DIFFICULTY_SETTINGS.append(Setting('Easy', 10, 12, 5, derive_font(24)))
DIFFICULTY_SETTINGS.append(Setting('Medium', 20, 50, 3, derive_font(16)))
DIFFICULTY_SETTINGS.append(Setting('Hard', 28, 99, 2, derive_font(12)))

for setting in DIFFICULTY_SETTINGS:
	setting.set_cell_size(DISPLAY_WIDTH, PADDING_SIDE)

running = True
playing = False
clock = pygame.time.Clock()

game_settings_index = 1
game_settings = DIFFICULTY_SETTINGS[game_settings_index]

selected_cells = []
prev_click = None

buttons = []
selected_button = None

time = 0
result = 0

board = None


def draw_mine(x, y):
	mine_x = x + (game_settings.get_cell_size() / 2)
	mine_y = y + (game_settings.get_cell_size() / 2)
	mine_radius = (game_settings.get_cell_size() / 2) / 2

	pygame.draw.circle(window, BLACK, (mine_x, mine_y), mine_radius)

def draw_flag(x, y):
	flag_width = game_settings.get_cell_size() / 2
	flag_height = flag_width

	flag_x = x + game_settings.get_cell_size() / 2 - flag_width / 2
	flag_y = y + flag_x - x

	flag_rect = pygame.Rect(flag_x, flag_y, flag_width, flag_height / 2)
	pygame.draw.rect(window, RED, flag_rect)

	start_pos = (flag_x, flag_y)
	end_pos = (flag_x, flag_y + flag_height)

	pygame.draw.line(window, BLACK, start_pos, end_pos, game_settings.get_shadow_size())

	# show 'X' if game over and flag is not a mine

def draw_hint(x, y, hint):
	if hint == 0:
		return

	rendered_text = game_settings.get_font().render(str(hint), 1, BLACK)

	text_x = x + (game_settings.get_cell_size() / 2) - (rendered_text.get_width() / 2)
	text_y = y + (game_settings.get_cell_size() / 2) - (rendered_text.get_height() / 2)

	window.blit(rendered_text, (text_x, text_y))

def draw_board(board):
	for board_row in board.get_grid():
		for cell in board_row:
			row, column = cell.get_location()

			cell_size = game_settings.get_cell_size()
			shadow_size = game_settings.get_shadow_size()

			cell_x = (column * cell_size) + PADDING_SIDE
			cell_y = (row * cell_size) + PADDING_TOP
			cell_color = LIGHT_GRAY

			shadow_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
			pygame.draw.rect(window, BLACK, shadow_rect)

			if cell in selected_cells:
				cell_x += shadow_size
				cell_y += shadow_size

			if cell.get_status() == Cell.UNCOVERED:
				cell_x += shadow_size
				cell_y += shadow_size

				if cell.is_mine():
					cell_color = RED
				else:
					cell_color = GRAY

			cell_rect = pygame.Rect(cell_x, cell_y, cell_size - shadow_size, cell_size - shadow_size)
			pygame.draw.rect(window, cell_color, cell_rect)

			if cell.get_status() == Cell.UNCOVERED and cell.is_mine():
				draw_mine(cell_x, cell_y)

			if cell.get_status() == Cell.UNCOVERED and not cell.is_mine():
				draw_hint(cell_x, cell_y, cell.get_hint())

			if cell.get_status() == Cell.FLAGGED:
				draw_flag(cell_x, cell_y)

def get_selected_cell(mouse_x, mouse_y):
	if mouse_x < PADDING_SIDE or mouse_x > DISPLAY_WIDTH - PADDING_SIDE:
		return None

	if mouse_y < PADDING_TOP or mouse_y > DISPLAY_HEIGHT - PADDING_TOP:
		return None

	mouse_x -= PADDING_SIDE
	mouse_y -= PADDING_TOP

	cell_x = int(mouse_x // game_settings.get_cell_size())
	cell_y = int(mouse_y // game_settings.get_cell_size())

	return board.get_grid()[cell_y][cell_x]

def create_buttons():
	rect_x = PADDING_SIDE
	rect_y = PADDING_TOP + game_settings.get_cell_size() * game_settings.get_grid_size() + PADDING_BETWEEN

	easy_button = Button('Easy', rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT)
	buttons.append(easy_button)

	rect_x = DISPLAY_WIDTH / 2 - BUTTON_WIDTH / 2
	
	medium_button = Button('Medium', rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT)
	buttons.append(medium_button)

	rect_x = DISPLAY_WIDTH - PADDING_SIDE - BUTTON_WIDTH

	hard_button = Button('Hard', rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT)
	buttons.append(hard_button)

	rect_x = DISPLAY_WIDTH / 2 - BUTTON_WIDTH / 2
	rect_y = PADDING_TOP - BUTTON_HEIGHT - PADDING_BETWEEN

	restart_button = Button('Restart', rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT)
	buttons.append(restart_button)

# get the button clicked or hovered on
def get_selected_button(mouse_x, mouse_y):
	for button in buttons:
		if mouse_x >= button.get_x() and mouse_x <= button.get_x() + button.get_width():
			if mouse_y >= button.get_y() and mouse_y <= button.get_y() + button.get_height():
				return button

	return None

# End the current game and set the result accordingly
def game_over(final_result):
	global result, playing

	result = final_result
	playing = False

	draw_cells()
	pygame.display.update()
	pygame.time.delay(2000)

def set_up(settings):
	global board, time, result, playing

	size = settings.get_grid_size()
	mines = settings.get_mines()

	board = Board(size, size, mines)

	time = 0
	result = 0
	playing = False

pygame.display.set_caption('Minesweeper')
window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

create_buttons()
set_up(game_settings)


while running:
	clock.tick(FPS)
	window.fill(WHITE)

	if playing:
		time += 1 / FPS

	# show time
	text = derive_font(24).render(str(int(time // 1)), 1, BLACK)
	text_x = DISPLAY_WIDTH - PADDING_SIDE - text.get_width()
	text_y = PADDING_TOP - text.get_height() - PADDING_BETWEEN

	window.blit(text, (text_x, text_y))

	# show mines left
	text = derive_font(24).render(str(board.get_mines()), 1, BLACK)
	text_x = PADDING_SIDE
	text_y = PADDING_TOP - text.get_height() - PADDING_BETWEEN

	window.blit(text, (text_x, text_y))

	# show buttons
	for button in buttons:
		text = derive_font(16).render(button.get_label(), 1, BLACK)
		text_x = button.get_x() + button.get_width() / 2 - text.get_width() / 2
		text_y = button.get_y() + button.get_height() / 2 - text.get_height() / 2

		window.blit(text, (text_x, text_y))

	if selected_button:
		button_rect = pygame.Rect(selected_button.get_x(), selected_button.get_y(), selected_button.get_width(), selected_button.get_height())
		pygame.draw.rect(window, BLACK, button_rect, BUTTON_BORDER_SIZE)

	# add border around selected difficulty
	button = buttons[game_settings_index]
	button_rect = pygame.Rect(button.get_x(), button.get_y(), button.get_width(), button.get_height())

	pygame.draw.rect(window, BLACK, button_rect, BUTTON_BORDER_SIZE)

	# handle pygame events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.MOUSEMOTION:
			x, y = event.pos
			selected_button = get_selected_button(x, y)

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			mouse_button = event.button

			selected_cell = get_selected_cell(x, y)
			row, column = selected_cell.get_location()

			selected_button = get_selected_button(x, y)

			if selected_cell:
				if mouse_button != 1 and mouse_button != 3:
					continue

				# left mouse click feature
				# uncover cell
				if mouse_button == 1:
					selected_cells.append(selected_cell)

				# right mouse click feature
				# flag cell
				if mouse_button == 3 and playing:
					board.flag(row, column)

				# right + left mouse click feature
				# indicate or reveal adjacent cells
				if selected_cell.get_status() == Cell.UNCOVERED and playing:
					if not prev_click:
						prev_click = (time, mouse_button)
						continue
					
					prev_time, prev_button = prev_click

					if mouse_button != prev_button and time - prev_time < 5 / 60:
						adj_cells = board.get_adj_cells(row, column)
						adj_flags = board.get_adj_flags(adj_cells)

						for n in adj_cells:
							if n.get_status() != COVERED:
								continue

							if len(adj_flags) == selected_cell.get_hint():
								n.uncover()
							else:
								selected_cells.append(n)

					prev_click = None

		if event.type == pygame.MOUSEBUTTONUP:
			x, y = event.pos
			mouse_button = event.button

			selected_cell = get_selected_cell(x, y)
			row, column = selected_cell.get_location()
			
			if selected_cell in selected_cells and len(selected_cells) == 1 and mouse_button == 1:
				board.uncover(row, column)
				playing = True

			selected_cells.clear()


	# draw cells and update the window
	if result:
		board_rect = pygame.Rect(PADDING_SIDE, PADDING_TOP, cell_size * difficulty["cells"], cell_size * difficulty["cells"])
		pygame.draw.rect(window, LIGHT_GRAY, board_rect)

		if result == WIN:
			text = GAME_FONT_24_PT.render("Congratulations!", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 50))

			text = GAME_FONT_16_PT.render("You beat minesweeper!", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 100))

			text = GAME_FONT_16_PT.render(f"Difficulty: {difficulty['name']}", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 130))

			text = GAME_FONT_16_PT.render(f"Total time: {int(time // 1)} seconds", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 160))
		elif result == LOSE:
			text = GAME_FONT_24_PT.render("Oops...", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 50))

			text = GAME_FONT_16_PT.render("You uncovered a mine.", 1, WHITE)
			window.blit(text, (PADDING_SIDE + (cell_size * difficulty["cells"] / 2) - (text.get_width() / 2), PADDING_TOP + 100))
	else:
		draw_board(board)

	pygame.display.update()


pygame.quit()