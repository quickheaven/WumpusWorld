from random import choice

from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.AgentState import AgentState
from wumpusworld.agent.Percept import Percept
from wumpusworld.agent.orientation.Coords import Coords
from wumpusworld.enums.Action import Action


class MovePlanningAgent(Agent):

    def __init__(self, grid_width: int, grid_height: int):
        super().__init__()
        self._name = "MOVE_PLANNING_AGENT"
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._agent_state = AgentState
        self._safe_locations = set()
        self._action_list = []

    def __str__(self):
        is_alive_str: str = 'A'  # Alive
        if not self.is_alive:
            is_alive_str = 'D'  # Dead
        return '{} ({})'.format(self._name, is_alive_str)

    def next_action(self, percept: Percept) -> Action:

        if self._agent_state.has_gold:
            if self._agent_state.location == Coords(0, 0):
                random_action_int = 4  # Climb
                return Action.get_by_id(random_action_int)
            else:
                # add action to the list.
                indexes = [i for i in range(2)]  # Exclude Grab (3) Climb (4).
                beeline_action_int: int = choice(indexes)
                beeline_action: Action = Action.get_by_id(beeline_action_int)
                # TODO move back to original location based on shortest path
                #
                # grid_width: int = self._grid_width
                # grid_height: int = self._grid_height
                #
                # self._agent_state = self._agent_state.apply_move_action(beeline_action, grid_width, grid_height)
                # self._action_list = self._action_list.append(beeline_action_int)

                return beeline_action

        elif percept.glitter:
            self.has_gold = True
            random_action_int = 3  # Grab
            return Action.get_by_id(random_action_int)
        else:
            indexes = [i for i in range(6) if i not in [3, 4]]  # Exclude Grab (3) Climb (4).
            random_action_int: int = choice(indexes)
            return Action.get_by_id(random_action_int)

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
