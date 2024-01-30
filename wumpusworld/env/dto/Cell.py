from __future__ import annotations

from wumpusworld.enums.CellState import CellState
from wumpusworld.env.dto.Item import Item
from wumpusworld.env.dto.Pit import Pit
from wumpusworld.env.dto.Wumpus import Wumpus


class Cell:  # Room

    def __init__(self, x, y, index_display_start_on_zero: bool = False):
        self._x = x
        self._y = y
        self._items = []
        self._cell_states = []
        self._index_display_start_on_zero = index_display_start_on_zero

    def __str__(self):
        items = ""
        if len(self._items) > 0:
            items = " ".join(str(x) for x in self._items)

        sensors = ""
        if len(self._cell_states) > 0:
            sensors = " ".join(CellState.get_by_id(x) for x in self._cell_states)

        label_x = self._x
        label_y = self._y
        if not self._index_display_start_on_zero:
            label_x = self._x + 1
            label_y = self._y + 1

        return 'Cell [{}][{}]: {}\n{}'.format(label_x, label_y, items, sensors)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def items(self):
        return self._items

    def add_item(self, item: Item):
        self._items.append(item)

    @property
    def cell_states(self):
        return self._cell_states

    def add_cell_state(self, cell_state: CellState) -> int:
        if cell_state in self._cell_states:
            return 0
        else:
            self._cell_states.append(cell_state)
            return 1

    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def has_pit(self) -> bool:
        for item in self.items:
            if isinstance(item, Pit):
                return True
        return False

    @property
    def has_wumpus(self) -> bool:
        for item in self.items:
            if isinstance(item, Wumpus):
                return True
        return False

    @property
    def has_stench(self) -> bool:
        for state in self._cell_states:
            if state == CellState.STENCH:
                return True
        return False

    @property
    def has_breeze(self) -> bool:
        for state in self._cell_states:
            if state == CellState.BREEZE:
                return True
        return False

    @property
    def has_glitter(self) -> bool:
        for state in self._cell_states:
            if state == CellState.GLITTER:
                return True
        return False

    @property
    def has_scream(self) -> bool:
        for state in self._cell_states:
            if state == CellState.SCREAM:
                return True
        return False
