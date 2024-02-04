from random import choice

from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.Percept import Percept
from wumpusworld.enums.Action import Action


class MovePlanningAgent(Agent):

    def __init__(self):
        super().__init__()
        self._name = "MOVE_PLANNING_AGENT"

    def __str__(self):
        is_alive_str: str = 'A'  # Alive
        if not self.is_alive:
            is_alive_str = 'D'  # Dead
        return '{} ({})'.format(self._name, is_alive_str)

    def next_action(self, percept: Percept) -> Action:
        indexes = [i for i in range(6) if i not in [3, 4]]  # Exclude Grab (3) Climb (4).
        random_action_int: int = choice(indexes)
        return Action.get_by_id(random_action_int)

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
