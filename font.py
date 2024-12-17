import pygame

GAME_FONT = './fonts/PressStart2P-Regular.ttf'

def derive_font(size, style=GAME_FONT):
	return pygame.font.Font(style, size)