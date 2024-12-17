class Setting:
    def __init__(self, name, grid_size, mines, shadow_size, font):
        self.name = name
        self.grid_size = grid_size
        self.mines = mines
        self.shadow_size = shadow_size
        self.font = font

    def get_name(self):
        return self.name

    def get_grid_size(self):
        return self.grid_size

    def get_cell_size(self):
        return self.cell_size

    def get_mines(self):
        return self.mines

    def get_shadow_size(self):
        return self.shadow_size

    def get_font(self):
        return self.font

    def set_cell_size(self, display_size, padding_size):
        self.cell_size = (display_size - 2 * padding_size) / self.grid_size