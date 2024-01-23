from wumpusworld.env.dto.Item import Item


class Gold(Item):

    def __init__(self):
        super().__init__()
        self._name = "GOLD"

    def __str__(self):
        return '{}'.format(self._name)
