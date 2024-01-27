class Coords:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __str__(self):
        return '({},{})'.format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
