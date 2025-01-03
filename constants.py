class Constants:
    FPS = 60
    SCALE = 1

    # display information
    DISPLAY_WIDTH = SCALE * 600
    DISPLAY_HEIGHT = SCALE * 650

    PADDING_TOP = SCALE * 75
    PADDING_BOTTOM = SCALE * 25
    PADDING_SIDE = SCALE * 25
    PADDING_BETWEEN = SCALE * 25

    # game board information
    GRID_SIZE = 16
    CELL_SIZE = (DISPLAY_WIDTH - 2 * PADDING_SIDE) / GRID_SIZE
    SHADOW_SIZE = 2
    NUMBER_OF_MINES = 40
    BOARD_FONT_SIZE = 16

    # color information
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (180, 180, 180)
    RED = (240, 16, 0)
    BROWN = (82, 60, 0)