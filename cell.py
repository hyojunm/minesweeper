class Cell:
    COVERED = 0
    UNCOVERED_LAND = 1
    UNCOVERED_MINE = 2
    FLAGGED = 3

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.mine = False
        self.status = Cell.COVERED
        self.hint = 0

    def __repr__(self):
        return f'({self.row}, {self.column})'

    def is_mine(self):
        return self.mine

    def set_mine(self, mine=True):
        self.mine = mine

    def get_status(self):
        return self.value

    def set_status(self, value):
        self.value = value

    def get_hint(self):
        return self.hint

    def set_hint(self, hint):
        self.hint = hint

    def get_location(self):
        return (self.row, self.column)

    def uncover(self):
        if self.status != Cell.COVERED:
            return False

        if self.mine:
            self.status = Cell.UNCOVERED_MINE

        if not self.mine:
            self.status = Cell.UNCOVERED_LAND

        return True

    # toggle flag
    def flag(self):
        if self.status == Cell.FLAGGED:
            self.status = Cell.COVERED
        
        if self.status == Cell.COVERED:
            self.status = Cell.FLAGGED