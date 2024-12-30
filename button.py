from font import derive_font

class Button:
    def __init__(self, label, x, y, width, height):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        pass

    def get_label(self):
        return self.label

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    # def draw(self, window, color):
    #     text = derive_font(16).render(self.label, 1, color)

    #     # center text horizontally
    #     x = self.x + self.width / 2 - text.get_width() / 2

    #     # center text vertically
	# 	y = self.y + self.height / 2 - text.get_height() / 2

	# 	window.blit(text, (x, y))