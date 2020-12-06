# Import required modules
import pygame
from game import Cell, create_cells, start_game, board


# Initialize pygame
pygame.init()
pygame.font.init()


# Set window properties
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 1000

pygame.display.set_caption("Minesweeper Game")
window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


# Set fonts
GAME_FONT = "PressStart2P-Regular.ttf"

GAME_FONT_32_PT = pygame.font.Font(GAME_FONT, 32)
GAME_FONT_24_PT = pygame.font.Font(GAME_FONT, 24)
GAME_FONT_16_PT = pygame.font.Font(GAME_FONT, 16)
GAME_FONT_12_PT = pygame.font.Font(GAME_FONT, 12)


# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (180, 180, 180)
RED = (240, 16, 0)
BROWN = (82, 60, 0)


# Set game properties
FPS = 60

PADDING_SIDE = 100
PADDING_TOP = 150

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_BORDER_SIZE = 3

WIN = 1
LOSE = 2

DIFFICULTIES = [{ "cells": 10, "mines": 12, "shadow": 5, "font": GAME_FONT_24_PT, "name": "Easy" },
				{ "cells": 20, "mines": 50, "shadow": 3, "font": GAME_FONT_16_PT, "name": "Medium" },
				{ "cells": 28, "mines": 99, "shadow": 2, "font": GAME_FONT_12_PT, "name": "Hard" }]


# Set game variables
running = True
playing = False
clock = pygame.time.Clock()

difficulty = DIFFICULTIES[1]
cell_size = 0

selected_cells = []
selected_button = None
click = None

mines_left = 0
time = 0
result = 0

# Other UI elements
buttons = []


# Create empty cells and set cell size
def set_up(difficulty):
	global cell_size, mines_left, time, result, playing

	create_cells(difficulty)
	cell_size = (DISPLAY_WIDTH - (2 * PADDING_SIDE)) / difficulty["cells"]

	create_buttons()

	mines_left = difficulty["mines"]
	time = 0
	result = 0
	playing = False


# Draw the board and the cells
def draw_cells():
	global mines_left, result, playing

	uncovered_cells = 0

	for row in board:
		for cell in row:
			shadow_rect = pygame.Rect(cell.column * cell_size + PADDING_SIDE, cell.row * cell_size + PADDING_TOP,
								 cell_size, cell_size)
			pygame.draw.rect(window, BLACK, shadow_rect)

			cell_x = (cell.column * cell_size) + PADDING_SIDE
			cell_y = (cell.row * cell_size) + PADDING_TOP
			cell_color = LIGHT_GRAY

			if cell.is_mine and result == LOSE and not cell.uncovered:
				cell.uncover()

			if cell.uncovered:
				if cell not in selected_cells:
					uncovered_cells += 1

				cell_x += difficulty["shadow"]
				cell_y += difficulty["shadow"]
				
				if cell.is_mine and cell not in selected_cells:
					cell_color = RED
				else:
					cell_color = GRAY

			cell_rect = pygame.Rect(cell_x, cell_y, cell_size - difficulty["shadow"], cell_size - difficulty["shadow"])
			pygame.draw.rect(window, cell_color, cell_rect)

			if cell.is_mine and cell.uncovered and cell not in selected_cells:
				mine_x = cell_x + (cell_size / 2)
				mine_y = cell_y + (cell_size / 2)
				mine_radius = (cell_size / 2) / 2

				pygame.draw.circle(window, BLACK, (mine_x, mine_y), mine_radius)

				if playing:
					game_over(LOSE)
			elif cell.flagged:
				flag_width = cell_size / 2
				flag_height = flag_width
				flag_x = cell_x + (cell_size / 2 - flag_width / 2)
				flag_y = cell_y + (flag_x - cell_x)

				flag = pygame.Rect(flag_x, flag_y, flag_width, flag_height / 2)
				pygame.draw.rect(window, RED, flag)

				pygame.draw.line(window, BLACK, (flag_x, flag_y), (flag_x, flag_y + flag_height), difficulty["shadow"])

				if result == LOSE and not cell.is_mine:
					pygame.draw.line(window, BLACK, (cell_x, cell_y), (cell_x + (cell_size - difficulty["shadow"]), cell_y + (cell_size - difficulty["shadow"])), difficulty["shadow"])
					pygame.draw.line(window, BLACK, (cell_x + (cell_size - difficulty["shadow"]), cell_y), (cell_x, cell_y + (cell_size - difficulty["shadow"])), difficulty["shadow"])
			else:
				value = difficulty["font"].render(cell.value, 1, BLACK)
				window.blit(value, (cell_x + (cell_size / 2) - (value.get_width() / 2),
									cell_y + (cell_size / 2) - (value.get_height() / 2)))

	if uncovered_cells == (difficulty["cells"] ** 2) - difficulty["mines"] and playing:
		mines_left = 0
		game_over(WIN)


# Get the row and column values for the cell that the user clicked or hovered on
def get_selected_cell(mouse_x, mouse_y):
	mouse_x -= PADDING_SIDE
	mouse_y -= PADDING_TOP

	if mouse_x < 0 or mouse_x > DISPLAY_WIDTH - (2 * PADDING_SIDE) or mouse_y < 0 or mouse_y > DISPLAY_HEIGHT - (2 * PADDING_TOP):
		return False
	else:
		cell_x = int(mouse_x // cell_size)
		cell_y = int(mouse_y // cell_size)

		return board[cell_y][cell_x]


# Create buttons and set up button location
def create_buttons():
	rect_x = PADDING_SIDE
	rect_y = PADDING_TOP + (cell_size * difficulty["cells"]) + 30

	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))

	rect_x = (DISPLAY_WIDTH / 2) - (BUTTON_WIDTH / 2)
	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))

	rect_x = (DISPLAY_WIDTH - PADDING_SIDE) - BUTTON_WIDTH
	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))

	rect_x = (DISPLAY_WIDTH / 2) - (BUTTON_WIDTH / 2)
	rect_y = PADDING_TOP - (BUTTON_HEIGHT + 30)
	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))


# Get the button that the user clicked or hovered on
def get_selected_button(mouse_x, mouse_y):
	for button in buttons:
		if mouse_x >= button.x and mouse_x <= button.x + button.w and mouse_y >= button.y and mouse_y <= button.y + button.h:
			return button

	return False


# End the current game and set the result accordingly
def game_over(final_result):
	global result, playing

	result = final_result
	playing = False

	draw_cells()
	pygame.display.update()
	pygame.time.delay(2000)


# Set up the game
set_up(difficulty)


# Keep the program running
while running:

	# Set clock and fill window
	clock.tick(FPS)
	window.fill(WHITE)

	
	# Update and draw stopwatch
	if playing:
		time += 1 / FPS

	text = GAME_FONT_24_PT.render(str(int(time // 1)), 1, BLACK)
	window.blit(text, (DISPLAY_WIDTH - PADDING_SIDE - text.get_width(), PADDING_TOP - text.get_height() - 30))


	# Show the number of mines left
	text = GAME_FONT_24_PT.render(str(mines_left), 1, BLACK)
	window.blit(text, (PADDING_SIDE, PADDING_TOP - text.get_height() - 30))


	# Draw restart button on top
	text = GAME_FONT_16_PT.render("Restart", 1, BLACK)
	window.blit(text, (buttons[3].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[3].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))


	# Draw difficulty buttons on the bottom
	text = GAME_FONT_16_PT.render("Easy", 1, BLACK)
	window.blit(text, (buttons[0].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[0].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))

	text = GAME_FONT_16_PT.render("Medium", 1, BLACK)
	window.blit(text, (buttons[1].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[1].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))

	text = GAME_FONT_16_PT.render("Hard", 1, BLACK)
	window.blit(text, (buttons[2].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[2].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))


	# Add rectangle border around selected button
	if selected_button:
		pygame.draw.rect(window, BLACK, selected_button, 3)

	pygame.draw.rect(window, BLACK, buttons[DIFFICULTIES.index(difficulty)], 3)


	# Handle pygame events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEMOTION:
			x, y = event.pos
			button = get_selected_button(x, y)

			if button:
				selected_button = button
			else:
				selected_button = None
		elif event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			mouse_button = event.button
			cell = get_selected_cell(x, y)

			if cell:
				if cell.uncovered and (mouse_button == 1 or mouse_button == 3):
					if click and mouse_button != click[1] and time - click[0] < 5 / 60 and playing:
						adj_cells = cell.get_adj_cells()
						adj_flags = len(list(filter(lambda item : item.flagged, adj_cells)))

						for adj_cell in adj_cells:
							if not adj_cell.uncovered and not adj_cell.flagged:
								if adj_flags == int(cell.value):
									adj_cell.uncover()
								else:
									adj_cell.uncovered = True
									selected_cells.append(adj_cell)

						click = None
					else:
						click = [time, mouse_button]
				elif mouse_button == 1 and not cell.flagged:
					cell.uncovered = True
					selected_cells.append(cell)
				elif mouse_button == 3 and playing:
					if cell.flagged:
						cell.flagged = False
						mines_left += 1
					else:
						cell.flagged = True
						mines_left -= 1

			else:
				button = get_selected_button(x, y)

				if button:
					if buttons.index(button) != DIFFICULTIES.index(difficulty) and buttons.index(button) < len(DIFFICULTIES):
						difficulty = DIFFICULTIES[buttons.index(button)]
					
					set_up(difficulty)

		elif event.type == pygame.MOUSEBUTTONUP:
			x, y = event.pos
			mouse_button = event.button
			cell = get_selected_cell(x, y)

			if len(selected_cells) == 1:
				if mouse_button == 1:
					selected_cells[0].uncovered = False

					if cell in selected_cells:
						if playing:
							cell.uncover()
						else:
							start_game(cell.row, cell.column, difficulty)
							playing = True
			else:
				for selected_cell in selected_cells:
					selected_cell.uncovered = False

			selected_cells.clear()


	# Draw cells and update the window
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
		draw_cells()

	pygame.display.update()


pygame.quit()