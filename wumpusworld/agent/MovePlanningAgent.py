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
        self._agent_state = AgentState()
        self._safe_locations = set()
        self._action_list = []

    def __str__(self):
        is_alive_str: str = 'A'  # Alive
        if not self.is_alive:
            is_alive_str = 'D'  # Dead
        return '{} ({})'.format(self._name, is_alive_str)

    def next_action(self, percept: Percept) -> Action:
        action_int = -1
        # Update the state of the Move Planning agent before running the next_action on the environment level.
        # Inspiration comes from Scala project branch beeline-agent

        if self._agent_state.has_gold:
            print('The agent have the gold. Performing an escape plan.')
            if self._agent_state.location == Coords(0, 0):
                action_int = 4  # Climb

            else:
                # add action to the list.
                indexes = [i for i in range(2)]  # Exclude Grab (3) Climb (4).
                action_int = choice(indexes)
                """
                TODO move back to original location based on shortest path
                Study further networkx.
                Plan the graph and edges.
                Find the shortest path based on the Coords.
                Translate the shortest path into list of actions.
                Used that list of actions to go back to starting cell.
                """
                if len(self._action_list) == 0:
                    # call a function that will use networkx to build the shortest path.
                    pass
                else:
                    # execute an action plan based on action_list.
                    pass

                # grid_width: int = self._grid_width
                # grid_height: int = self._grid_height

                # self._agent_state = self._agent_state.apply_move_action(beeline_action, grid_width, grid_height)
                # self._action_list = self._action_list.append(action_int)

        elif percept.glitter():
            self._agent_state.has_gold = True
            action_int = 3  # Grab

        else:
            indexes = [i for i in range(6) if i not in [3, 4]]  # Exclude Grab (3) Climb (4).
            action_int = choice(indexes)

            match action_int:
                case 0:
                    new_safe_location = self._agent_state.forward(self._grid_width, self._grid_height)
                    self._safe_locations.add(new_safe_location)
                case 1:
                    self._agent_state.turn_left()
                case 2:
                    self._agent_state.turn_right()
                case 2:
                    self._agent_state.use_arrow = True

        safe_locations = [str(coords) for coords in self._safe_locations]
        action_list = [str(i) for i in self._action_list]
        print('MovePlanningAgent.next_action grid_width: {}, grid_height: {}, \nagent_state: {}, \nsafe_locations: {}, '
              '\naction_list: {}'
              .format(self._grid_width, self._grid_height, self._agent_state, safe_locations, action_list))
        return Action.get_by_id(action_int)

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
