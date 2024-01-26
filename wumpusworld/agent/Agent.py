from abc import abstractmethod

from wumpusworld.enums.Action import Action
from wumpusworld.env.dto.Item import Item
from wumpusworld.env.dto.Percept import Percept

"""
Wumpus World HAS-A Agent:
The Agent HAS-A next action that can be Forward, Turn Left, Turn Right, Shoot, Grab and Climb.
"""


class Agent(Item):

    def __init__(self):
        self._has_gold = False
        self._has_arrow = True
        self._is_alive = True

    def __str__(self):
        return "Gold: {}, Arrow: {}, Alive: {}".format(self._has_gold, self._has_arrow, self._is_alive)

    @abstractmethod
    def next_action(self, percept: Percept) -> Action:
        pass

    @property
    def has_gold(self) -> bool:
        return self._has_gold

    @has_gold.setter
    def has_gold(self, has_gold: bool) -> None:
        self._has_gold = has_gold

    @property
    def has_arrow(self) -> bool:
        return self._has_arrow

    @has_arrow.setter
    def has_arrow(self, has_arrow: bool) -> None:
        self._has_arrow = has_arrow

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self._is_alive = is_alive
