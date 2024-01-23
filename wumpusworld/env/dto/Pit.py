from wumpusworld.env.dto.Item import Item


class Pit(Item):

    def __init__(self):
        super().__init__()
        self._name = "PIT"

    def __str__(self):
        return '{}'.format(self._name)
