from abc import abstractmethod

from wumpusworld.enums.Action import Action
from wumpusworld.env.dto.Item import Item
from wumpusworld.env.dto.Percept import Percept

"""
Wumpus World HAS-A Agent:
The Agent HAS-A next action that can be Forward, Turn Left, Turn Right, Shoot, Grab and Climb.
"""


class Agent(Item):

    @abstractmethod
    def next_action(self, percept: Percept) -> Action:
        pass
