from random import choice

import networkx as nx
from networkx import Graph
from scipy.spatial import distance

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
        action_int: int = -1
        # Inspiration comes from Scala project branch beeline-agent

        if self._agent_state.has_gold:
            print('The agent have the gold. Performing an escape plan.')
            if self._agent_state.location == Coords(0, 0):  # we have a winner
                action_int = 4  # Climb

            else:
                # add action to the list.
                indexes = [i for i in range(2)]  # Exclude Grab (3) Climb (4).
                action_int = choice(indexes)

                if len(self._action_list) == 0:

                    # --------------------------------------------------------------------------------------------------
                    # Agent creates and updates the escape plan  (5pts)
                    # --------------------------------------------------------------------------------------------------
                    print('Building the escape plan.')
                    self._action_list = self.__create_shortest_path_escape_plan()

                else:

                    # --------------------------------------------------------------------------------------------------
                    # Agent follows the shortest path back to start after gold grab(5pts)
                    # --------------------------------------------------------------------------------------------------
                    print('Execute the action plan based on action_list.')

                    grid_width: int = self._grid_width
                    grid_height: int = self._grid_height

                    #  Get the action from the action list (the first on the list)
                    action_int = self._action_list[0]

                    #  Apply the move action
                    self._agent_state = self._agent_state.apply_move_action(Action.get_by_id(action_int), grid_width,
                                                                            grid_height)
                    #  Remove the action from the action list (the first on the list)
                    self._action_list.pop(0)

        elif percept.glitter():
            self._agent_state.has_gold = True
            action_int = 3  # Grab

        else:
            indexes = [i for i in range(6) if i not in [3, 4]]  # Exclude Grab (3) Climb (4).
            action_int = choice(indexes)

            match action_int:
                case 0:
                    new_safe_location = self._agent_state.forward(self._grid_width, self._grid_height)

                    # --------------------------------------------------------------------------------------------------
                    #  Agent keeps track of safe locations (5pts)
                    # --------------------------------------------------------------------------------------------------
                    #  move may not actually be safe, but if not agent will be dead so doesn't matter
                    self._safe_locations.add((new_safe_location, self._orientation))

                case 1:
                    self._agent_state.turn_left()
                case 2:
                    self._agent_state.turn_right()
                case 2:
                    self._agent_state.use_arrow = True

        safe_locations = ['Coords: ({},{}) Orientation: {}'.format(coords.x, coords.y, orientation) for
                          coords, orientation in self._safe_locations]

        print('MovePlanningAgent.next_action grid_width: {}, grid_height: {}, \nagent_state: {}, \nsafe_locations: {}, '
              .format(self._grid_width, self._grid_height, self._agent_state, safe_locations))
        return Action.get_by_id(action_int)

    def __get_manhattan_distance(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return dist

    def __create_shortest_path_escape_plan(self):
        graph: Graph = nx.Graph()
        graph.graph["Graph_Name"] = "Escape Plan"

        nodes = []
        edges = []

        old_x = 0
        old_y = 0

        for loc, orient in self._safe_locations:
            # Build the nodes
            node = ((loc.x, loc.y), {'orientation': orient})
            nodes.append(node)

            # Build the edges : (from location, to location)
            edge = ((old_x, old_y), (loc.x, loc.y))
            edges.append(edge)
            old_x = loc.x
            old_y = loc.y

        print('nodes: {}'.format(nodes))
        print('edges: {}'.format(edges))

        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        # --------------------------------------------------------------------------------------------------
        # Shortest path is created from the graph (5pts)
        # --------------------------------------------------------------------------------------------------
        source_node = self._agent_state.location.get()
        target_node = Coords(0, 0).get()
        print('Source Node: {}, Target Node: {}'.format(source_node, target_node))

        # https://datascienceparichay.com/article/manhattan-distance-python/
        #  Option 1:
        shortest_path = nx.astar_path(graph, source_node, target_node, heuristic=distance.cityblock)
        #  Option 2:
        #  shortest_path = nx.astar_path(graph, source_node, target_node, heuristic=self.__get_manhattan_distance)
        print("The shortest path: {}".format(shortest_path))

        escape_plan = [1, 2, 3, 1]  # TODO build the escape plan

        return escape_plan

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
