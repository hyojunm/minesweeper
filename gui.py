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
TITLE_FONT = pygame.font.SysFont("arial", 100)
GAME_FONT = pygame.font.SysFont("monospace", 50)
SETTINGS_FONT = pygame.font.SysFont("monospace", 30)


# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (180, 180, 180)
GRAY_BG = (128, 128, 128, 0.5)
RED = (240, 16, 0)


# Set game properties
FPS = 60

SHADOW = 3

PADDING_SIDE = 100
PADDING_TOP = 150

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

DIFFICULTIES = [{ "cells": 8, "mines": 8 },
				{ "cells": 16, "mines": 32 },
				{ "cells": 24, "mines": 72 }]


# Set game variables
running = True
playing = False
clock = pygame.time.Clock()

difficulty = DIFFICULTIES[1]
cell_size = 0

selected_cell = None
selected_button = None

time = 0

# Other UI elements (buttons, stopwatch, etc.)
buttons = []


# Draw the board and the cells
def draw_cells():
	uncovered_cells = 0

	for row in board:
		for cell in row:
			shadow = pygame.Rect(cell.column * cell_size + PADDING_SIDE, cell.row * cell_size + PADDING_TOP,
								 cell_size, cell_size)
			pygame.draw.rect(window, BLACK, shadow)

			cell_x = (cell.column * cell_size) + PADDING_SIDE
			cell_y = (cell.row * cell_size) + PADDING_TOP
			cell_color = LIGHT_GRAY

			if cell.uncovered:
				uncovered_cells += 1
				cell_x += SHADOW
				cell_y += SHADOW
				cell_color = GRAY

				if cell.is_mine and cell != selected_cell:
					print("You lose...")
					pygame.quit()

			elif cell.flagged:
				cell_color = RED

			cell_rect = pygame.Rect(cell_x, cell_y, cell_size - SHADOW, cell_size - SHADOW)
			pygame.draw.rect(window, cell_color, cell_rect)

			value = GAME_FONT.render(cell.value, 1, BLACK)
			window.blit(value, (cell_x + (cell_size / 2) - (value.get_width() / 2),
								cell_y + (cell_size / 2) - (value.get_height() / 2)))

	if uncovered_cells == (difficulty["cells"] ** 2) - difficulty["mines"]:
		print("You win")
		pygame.quit()


# Get the row and column values for the cell that the user clicked or hovered on
def get_selected_cell(mouse_x, mouse_y):
	mouse_x -= PADDING_SIDE
	mouse_y -= PADDING_TOP

	if mouse_x < 0 or mouse_x > DISPLAY_WIDTH - (2 * PADDING_SIDE) or mouse_y < 0 or mouse_y > DISPLAY_HEIGHT - (2 * PADDING_TOP):
		return False
	else:
		cell_x = int(mouse_x // cell_size)
		cell_y = int(mouse_y // cell_size)

		return [cell_x, cell_y]


# Create buttons and set up button location
def create_buttons():
	rect_x = PADDING_SIDE
	rect_y = PADDING_TOP + (cell_size * difficulty["cells"]) + 30

	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))

	rect_x = (DISPLAY_WIDTH / 2) - (BUTTON_WIDTH / 2)
	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))

	rect_x = (DISPLAY_WIDTH - PADDING_SIDE) - BUTTON_WIDTH
	buttons.append(pygame.Rect(rect_x, rect_y, BUTTON_WIDTH, BUTTON_HEIGHT))


# Get the button that the user clicked or hovered on
def get_selected_button(mouse_x, mouse_y):
	for button in buttons:
		if mouse_x >= button.x and mouse_x <= button.x + button.w and mouse_y >= button.y and mouse_y <= button.y + button.h:
			return button

	return False


# Create empty cells and set cell size
create_cells(difficulty)
cell_size = (DISPLAY_WIDTH - (2 * PADDING_SIDE)) / difficulty["cells"]
create_buttons()


# Keep the program running
while running:

	# Set clock and fill window
	clock.tick(FPS)
	window.fill(WHITE)


	# Draw difficulty buttons on the bottom
	text = SETTINGS_FONT.render("Easy", 1, BLACK)
	window.blit(text, (buttons[0].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[0].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))

	text = SETTINGS_FONT.render("Medium", 1, BLACK)
	window.blit(text, (buttons[1].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[1].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))

	text = SETTINGS_FONT.render("Hard", 1, BLACK)
	window.blit(text, (buttons[2].x + (BUTTON_WIDTH / 2) - (text.get_width() / 2),
					   buttons[2].y + (BUTTON_HEIGHT / 2) - (text.get_height() / 2)))

	if selected_button:
		pygame.draw.rect(window, BLACK, button, SHADOW)

	pygame.draw.rect(window, BLACK, buttons[DIFFICULTIES.index(difficulty)], SHADOW)


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
			selected_cell = get_selected_cell(x, y)

			if selected_cell and mouse_button == 1:
				board[selected_cell[1]][selected_cell[0]].uncovered = True
			else:
				button = get_selected_button(x, y)

				if button:
					playing = False
					difficulty = DIFFICULTIES[buttons.index(button)]
					create_cells(difficulty)
					pygame.time.delay(1000)
					cell_size = (DISPLAY_WIDTH - (2 * PADDING_SIDE)) / difficulty["cells"]
		elif event.type == pygame.MOUSEBUTTONUP:
			x, y = event.pos
			mouse_button = event.button
			cell = get_selected_cell(x, y)

			if selected_cell:
				if mouse_button == 1:				
					board[selected_cell[1]][selected_cell[0]].uncovered = False

					if cell and cell == selected_cell:
						if playing:
							board[cell[1]][cell[0]].uncover()
						else:
							start_game(cell[1], cell[0], difficulty)
							playing = True
				elif mouse_button == 3 and playing:
					if board[selected_cell[1]][selected_cell[0]].flagged:
						board[selected_cell[1]][selected_cell[0]].flagged = False
					else:
						board[selected_cell[1]][selected_cell[0]].flagged = True

			selected_cell = None


	# Draw cells and update the window
	draw_cells()
	pygame.display.update()


pygame.quit()