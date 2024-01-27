import random

from wumpusworld.agent.Agent import Agent
from wumpusworld.enums.Action import Action
from wumpusworld.agent.Percept import Percept


class NaiveAgent(Agent):

    def __init__(self):
        super().__init__()
        self._name = "NAIVE_AGENT"

    def __str__(self):
        return self._name

    def next_action(self, percept: Percept) -> Action:
        random_action_int: int = random.randint(0, 5)
        return Action.get_by_id(random_action_int)

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} ({})'.format(self._name, parent_class_str)
