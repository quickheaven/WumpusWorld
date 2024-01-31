from wumpusworld.env.dto.Item import Item


class Wumpus(Item):

    def __init__(self):
        super().__init__()
        self._name = "WUMPUS"
        self._is_alive = True

    def __str__(self):
        is_alive_str: str = 'A'  # Alive
        if not self.is_alive:
            is_alive_str = 'D'  # Dead
        return '{} ({})'.format(self._name, is_alive_str)

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self._is_alive = is_alive
