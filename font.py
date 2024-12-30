import pygame

GAME_FONT = './fonts/PressStart2P-Regular.ttf'

# save font objects for later
fonts = {}

def derive_font(size, style=GAME_FONT):
	if not style in fonts:
		fonts[style] = {}

	if not size in fonts[style]:
		fonts[style][size] = pygame.font.Font(style, size)
		
	return fonts[style][size]