from abc import abstractmethod

from wumpusworld.env.dto.Item import Item

"""
Wumpus World HAS-A Agent:
The Agent have 6 actions (Forward, Turn Left, Turn Right, Shoot, Grab and Climb)
"""
class Agent(Item):

    @abstractmethod
    def next_action(self):
        pass

