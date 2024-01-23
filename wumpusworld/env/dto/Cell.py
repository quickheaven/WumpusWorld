from __future__ import annotations

from wumpusworld.enums.Percept import Percept
from wumpusworld.env.dto.Item import Item


class Cell:  # Room

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._items = []
        self._percepts = []

    def __str__(self):
        items = ""
        if len(self._items) > 0:
            items = " ".join(str(x) for x in self._items)

        sensors = ""
        if len(self._percepts) > 0:
            sensors = " ".join(Percept.get_by_id(x) for x in self._percepts)

        #label_x = self._x + 1
        #label_y = self._y + 1
        #return 'Cell [{}][{}]: [{},{}] {}\n{}'.format(self._x, self._y, label_x, label_y, items, sensors)

        return 'Cell [{}][{}]: {}\n{}'.format(self._x, self._y, items, sensors)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def items(self):
        return self._items

    # @item.setter
    # def item(self, item: Item) -> None:
    #    self._item = item

    def add_item(self, item: Item):
        self._items.append(item)

    @property
    def percepts(self):
        return self._percepts

    # @sensorStates.setter
    # def sensorState(self, sensorState: SensorState) -> None:
    #   self._sensorStates = sensorState

    def add_percept(self, percept: Percept) -> int:
        if percept in self._percepts:
            return 0
        else:
            self._percepts.append(percept)
            return 1

    def isEmpty(self) -> bool:
        return len(self._items) == 0