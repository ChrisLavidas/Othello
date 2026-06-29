class Move:
    def __init__(self, row=-1, col=-1, value=0):
        self._row = row
        self._col = col
        self._value = value


    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
