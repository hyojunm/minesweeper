class Cell:
    COVERED = 0
    UNCOVERED = 1
    FLAGGED = 2

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.mine = False
        self.status = self.COVERED
        self.hint = 0

    def __repr__(self):
        return f'({self.row}, {self.column})[{'M' if self.mine else ' '}]'

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

    def get_location(self):
        return (self.row, self.column)

    def uncover(self):
        if self.status != self.COVERED:
            return False

        self.status = self.UNCOVERED
        return True

    # toggle flag
    def flag(self):
        if self.status == self.COVERED:
            self.status = self.FLAGGED
            return True

        if self.status == self.FLAGGED:
            self.status = self.COVERED
            return False