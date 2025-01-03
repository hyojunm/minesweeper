import pygame

from font import derive_font
from constants import Constants

class Cell:
    # status codes
    COVERED = 0
    UNCOVERED = 1
    SELECTED = 2
    FLAGGED = 3
    FLAGGED_INCORRECT = 4

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.mine = False
        self.status = self.COVERED
        self.hint = 0

    # used for command line output only
    def __repr__(self):
        status_code = ' '

        if self.status == self.UNCOVERED:
            status_code = str(self.hint)
        
        if self.status == self.FLAGGED:
            status_code = 'F'
        
        return f'({self.row}, {self.column})[{status_code}]'

    def is_mine(self):
        return self.mine

    def set_mine(self, mine=True):
        self.mine = mine

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_hint(self):
        return self.hint

    def set_hint(self, hint):
        self.hint = hint

    # get row and column as tuple
    def get_location(self):
        return (self.row, self.column)

    def uncover(self):
        if self.status != self.COVERED and self.status != self.SELECTED:
            return 0 # fail

        self.status = self.UNCOVERED
        return 1 # success

    # toggle flag
    def flag(self):
        if self.status == self.UNCOVERED:
            return 0 # fail - already uncovered

        if self.status == self.FLAGGED:
            self.status = self.COVERED
            return 1 # success - undo flag

        if self.status == self.COVERED:
            self.status = self.FLAGGED
            return 2 # success - place flag

    # toggle "select" as candidate to be uncovered
    def select(self):
        if self.status == self.COVERED:
            self.status = self.SELECTED
            return 0 # success - selected

        if self.status == self.SELECTED:
            self.status = self.COVERED
            return 1 # success - unselected

    def draw(self, window):
        # assign constant values to variables for easier access
        cell_size = Constants.CELL_SIZE
        shadow_size = Constants.SHADOW_SIZE

        cell_x = (self.column * cell_size) + Constants.PADDING_SIDE
        cell_y = (self.row * cell_size) + Constants.PADDING_TOP
        cell_color = Constants.LIGHT_GRAY

        shadow_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
        pygame.draw.rect(window, Constants.BLACK, shadow_rect)

        # offset cell if uncovered or selected
        if self.status == self.UNCOVERED or self.status == self.SELECTED:
            cell_x += shadow_size
            cell_y += shadow_size

        if self.status == self.UNCOVERED and self.mine:
            cell_color = Constants.RED

        if self.status == self.UNCOVERED and not self.mine:
            cell_color = Constants.GRAY

        cell_width = cell_size - shadow_size
        cell_height = cell_size - shadow_size

        cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
        pygame.draw.rect(window, cell_color, cell_rect)

        if self.status == self.UNCOVERED and self.mine:
            self.draw_mine(window, cell_x, cell_y)

        if self.status == self.UNCOVERED and not self.mine:
            self.draw_hint(window, cell_x, cell_y)

        if self.status == self.FLAGGED:
            self.draw_flag(window, cell_x, cell_y)

        if self.status == self.FLAGGED_INCORRECT:
            self.draw_x(window, cell_x, cell_y)

    def draw_mine(self, window, x, y):
        mine_x = x + (Constants.CELL_SIZE / 2)
        mine_y = y + (Constants.CELL_SIZE / 2)
        mine_radius = (Constants.CELL_SIZE / 2) / 2

        pygame.draw.circle(window, Constants.BLACK, (mine_x, mine_y), mine_radius)

    def draw_hint(self, window, x, y):
        # don't display anything if there are no adjacent mines
        if self.hint == 0:
            return

        game_font = derive_font(Constants.BOARD_FONT_SIZE)
        rendered_text = game_font.render(str(self.hint), 1, Constants.BLACK)

        text_x = x + (Constants.CELL_SIZE / 2) - (rendered_text.get_width() / 2)
        text_y = y + (Constants.CELL_SIZE / 2) - (rendered_text.get_height() / 2)

        window.blit(rendered_text, (text_x, text_y))

    def draw_flag(self, window, x, y):
        flag_width = Constants.CELL_SIZE / 2
        flag_height = flag_width

        flag_x = x + Constants.CELL_SIZE / 2 - flag_width / 2
        flag_y = y + flag_x - x

        flag_rect = pygame.Rect(flag_x, flag_y, flag_width, flag_height / 2)
        pygame.draw.rect(window, Constants.RED, flag_rect)

        start_pos = (flag_x, flag_y)
        end_pos = (flag_x, flag_y + flag_height)

        pygame.draw.line(window, Constants.BLACK, start_pos, end_pos, Constants.SHADOW_SIZE)

    def draw_x(self, window, x, y):
        start_x = x
        end_x = start_x + Constants.CELL_SIZE - Constants.SHADOW_SIZE

        start_y = y
        end_y = start_y + Constants.CELL_SIZE - Constants.SHADOW_SIZE

        pygame.draw.line(window, Constants.RED, (start_x, start_y), (end_x, end_y), 4)
        pygame.draw.line(window, Constants.RED, (end_x, start_y), (start_x, end_y), 4)