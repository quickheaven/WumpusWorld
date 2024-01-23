from wumpusworld.env.dto.Item import Item


class Wumpus(Item):

    def __init__(self):
        super().__init__()
        self._name = "WUMPUS"

    def __str__(self):
        return '{}'.format(self._name)
