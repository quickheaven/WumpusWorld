from __future__ import annotations

from wumpusworld.enums.CellState import CellState
from wumpusworld.env.dto.Item import Item


class Cell:  # Room

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._items = []
        self._cell_states = []

    def __str__(self):
        items = ""
        if len(self._items) > 0:
            items = " ".join(str(x) for x in self._items)

        sensors = ""
        if len(self._cell_states) > 0:
            sensors = " ".join(CellState.get_by_id(x) for x in self._cell_states)

        #label_x = self._x + 1
        #label_y = self._y + 1
        #return 'Cell [{}][{}]: [{},{}] {}\n{}'.format(self._x, self._y, label_x, label_y, items, sensors)

        return 'Cell [{}][{}]: {}\n{}'.format(self._x + 1, self._y + 1, items, sensors)

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
    def cell_states(self):
        return self._cell_states

    # @sensorStates.setter
    # def sensorState(self, sensorState: SensorState) -> None:
    #   self._sensorStates = sensorState

    def add_cell_state(self, cell_state: CellState) -> int:
        if cell_state in self._cell_states:
            return 0
        else:
            self._cell_states.append(cell_state)
            return 1

    def is_empty(self) -> bool:
        return len(self._items) == 0