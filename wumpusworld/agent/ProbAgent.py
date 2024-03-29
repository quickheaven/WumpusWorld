from random import choice
from typing import Type

import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph
from scipy.spatial import distance

from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.AgentState import AgentState
from wumpusworld.agent.Orientation import Orientation
from wumpusworld.agent.Percept import Percept
from wumpusworld.agent.orientation.Coords import Coords
from wumpusworld.agent.orientation.East import East
from wumpusworld.agent.orientation.North import North
from wumpusworld.agent.orientation.South import South
from wumpusworld.agent.orientation.West import West
from wumpusworld.enums.Action import Action


class ProbAgent(Agent):

    def __init__(self, grid_width: int, grid_height: int):
        super().__init__()
        self._name = "PROB_AGENT"
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._agent_state = AgentState()
        self._safe_locations = set()
        self._action_list = []
        # -------------------------------------------------------------
        self._visited_locations = set()
        self._breeze_locations = set()
        self._stench_locations = set()
        # -------------------------------------------------------------

    def __str__(self):
        is_alive_str: str = 'A'  # Alive
        if not self.is_alive:
            is_alive_str = 'D'  # Dead

        agent_state_orientation: str = ""
        if isinstance(self._agent_state.orientation, North):
            agent_state_orientation = "↑"

        elif isinstance(self._agent_state.orientation, South):
            agent_state_orientation = "↓"

        elif isinstance(self._agent_state.orientation, West):
            agent_state_orientation = "←"

        elif isinstance(self._agent_state.orientation, East):
            agent_state_orientation = "→"

        return '{} ({}) ({})'.format(self._name, is_alive_str, agent_state_orientation)

    def next_action(self, percept: Percept) -> Action:
        action_int: int = -1

        # -------------------------------------------------------------
        # visiting_new_location
        is_visiting_new_location: bool = True
        for loc in self._visited_locations:
            if self._agent_state.location == loc:
                is_visiting_new_location = False
                break

        if not is_visiting_new_location:
            self._visited_locations.add(self._agent_state.location)

        # new_breeze_locations
        if percept.breeze():
            self._breeze_locations.add(self._agent_state.location)

        # new_stench_locations
        if percept.stench():
            self._stench_locations.add(self._agent_state.location)
        # -------------------------------------------------------------

        if self._agent_state.has_gold:
            print('The agent have the gold. Performing the escape plan.')

            if self._agent_state.location.x == 0 and self._agent_state.location.y == 0:  # we have a winner
                action_int = 4  # Climb
                print('**** The agent wins the game. ****')
            else:

                if len(self._action_list) == 0:  # Only create the escape action plan if it's not yet available.

                    # --------------------------------------------------------------------------------------------------
                    # Agent creates and updates the escape plan
                    # --------------------------------------------------------------------------------------------------
                    print('Building the escape plan using networkx.')
                    self._action_list = self.__create_escape_plan()
                    print('The action list of the escape plan {}.'.format(self._action_list))

                    # Set the action based on the first action list from the escape plan.
                    action_int = self._action_list[0]
                    self._action_list.pop(0)

                    # Update the agent state.
                    self._agent_state = self._agent_state.apply_move_action(action_int,
                                                                            self._grid_width,
                                                                            self._grid_height)

                else:

                    # --------------------------------------------------------------------------------------------------
                    # Agent follows the shortest path back to start after gold grab
                    # --------------------------------------------------------------------------------------------------
                    print('Execute the escape plan based on action_list {}.'.format(self._action_list))

                    #  Get the action from the action list (the first on the list)
                    action_int = self._action_list[0]

                    #  Apply the move action
                    self._agent_state = self._agent_state.apply_move_action(action_int,
                                                                            self._grid_width,
                                                                            self._grid_height)
                    # print('The agent location after apply the state: {} {}'.format(self._agent_state.location,
                    #                                                               self._agent_state.orientation))

                    #  Remove the action from the action list (the first on the list)
                    self._action_list.pop(0)

        elif percept.glitter():
            self._agent_state.has_gold = True
            self.has_gold = True  # Needed because Environment is looking on Agent and not the agent state.
            action_int = 3  # Grab

        else:
            # def safeLocations(tolerance: Double): Set[Coords] = {
            #       allLocations.flatMap(row => row.filter(location => newInferredPitProbs(location.x)(location.y) < tolerance && newInferredWumpusProbs(location.x)(location.y) < tolerance)).toSet ++ visitedLocations
            # }
            # action_int = self.__search_for_gold(percept,safeLocations(0.40))

            action_int = self.__search_for_gold(percept, 0.40)

        return Action.get_by_id(action_int)

    def __search_for_gold(self, percept: Percept, tolerance: float):
        indexes = [i for i in range(6) if i not in [3, 4]]  # Exclude Grab (3) Climb (4).
        action_int = choice(indexes)

        match action_int:
            case 0:
                # --------------------------------------------------------------------------------------------------
                # Agent keeps track of safe locations
                # --------------------------------------------------------------------------------------------------

                agent_old_safe_location = self._agent_state.location

                #  move may not actually be safe, but if not agent will be dead so doesn't matter
                agent_new_safe_location = self._agent_state.forward(self._grid_width, self._grid_height)

                self._safe_locations.add(
                    (agent_new_safe_location, agent_old_safe_location, self._agent_state.orientation))

            case 1:
                self._agent_state.turn_left()
            case 2:
                self._agent_state.turn_right()
            case 5:
                if percept.stench():
                    self._agent_state.use_arrow = True
                else:
                    self._agent_state.use_arrow = False

        # Get the unique safe locations without the old location and previous orientation. This is only for logging.
        safe_locations = set()
        for new_safe_loc, old_safe_loc, orientation in self._safe_locations:
            safe_locations.add(new_safe_loc.get())

        print('ProbAgent.next_action: \nagent_state: {}, \nsafe_locations: {}, '
              .format(self._agent_state, safe_locations))
        return action_int

    def __get_manhattan_distance(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return dist

    def __find_shortest_path(self):
        graph: Graph = nx.Graph()
        graph.graph["Graph_Name"] = "Escape Plan"

        nodes = []
        edges = []

        # for new_loc, old_loc, new_orient in self._safe_locations:
        for new_loc, old_loc, new_orient in self._safe_locations:
            # Build the nodes
            node = ((new_loc.x, new_loc.y), {'orientation': new_orient})
            nodes.append(node)

            # Build the edges : (from location, to location)
            edge = ((old_loc.x, old_loc.y), (new_loc.x, new_loc.y))
            edges.append(edge)

        # print('nodes: {}'.format(nodes))
        # print('edges: {}'.format(edges))

        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        # --------------------------------------------------------------------------------------------------
        # Shortest path is created from the graph
        # --------------------------------------------------------------------------------------------------
        source_node = self._agent_state.location.get()
        target_node = Coords(0, 0).get()
        print('Source Node: {}, Target Node: {}'.format(source_node, target_node))

        # https://datascienceparichay.com/article/manhattan-distance-python/
        #  Option 1: Use a custom function for manhattan distance.
        #  shortest_path = nx.astar_path(graph, source_node, target_node, heuristic=self.__get_manhattan_distance)

        #  Option 2: Use scipy library.
        shortest_path = nx.astar_path(graph, source_node, target_node, heuristic=distance.cityblock)
        print("The shortest path: {}".format(shortest_path))

        """
        nx.draw_networkx(graph,  # pos=pos,
                         node_color="red", node_size=3000, with_labels=True,
                         font_color="white", font_size="20", font_family="Times New Roman",
                         font_weight="bold",
                         width=5
                         )
        plt.margins(0.2)
        plt.show()
        """
        list_shortest_path = []
        for i, shortest_path in enumerate(shortest_path):
            list_shortest_path.append(Coords(shortest_path[0], shortest_path[1]))

        return list_shortest_path

    def __create_escape_plan(self):

        shortest_path = self.__find_shortest_path()

        return self.__create_action_list_from_shortest_path(shortest_path)

    def __create_action_list_from_shortest_path(self, nodes_remaining):
        forward = Action.get_by_value("FORWARD")
        action_list_escape_plan = []
        agent_state_orientation = self._agent_state.orientation
        agent_state_location = self._agent_state.location
        # print('*** agent_state_orientation: {}'.format(agent_state_orientation))

        while nodes_remaining:
            # print('*** len(nodes_remaining) : {}'.format(len(nodes_remaining)))
            # print('*** action_list_escape_plan: {}, {}'.format(action_list_escape_plan, nodes_remaining))
            if len(nodes_remaining) == 1:
                return action_list_escape_plan
            else:

                direction_to_go = self.__direction(agent_state_location, nodes_remaining[1])
                # print('*** direction_to_go: {}: agent_state_orientation: {}'.format(str(direction_to_go),
                #                                                                    str(agent_state_orientation)))

                if str(direction_to_go) == str(agent_state_orientation):  # is there a better way to do this in Python?
                    # print('*** Equal Orientation ****')
                    action_list_escape_plan.append(forward)
                    agent_state_location = nodes_remaining[1]
                    nodes_remaining.pop(0)
                else:
                    action, new_orientation = self.__rotate(direction_to_go, agent_state_orientation)
                    action_list_escape_plan.append(action)
                    agent_state_orientation = new_orientation

        return action_list_escape_plan

    def __direction(self, fr_location: Coords, to_location: Coords) -> Orientation:
        # Based on scala project with my added adjustments.
        print('__direction fr_location: {}, to_location: {}'.format(fr_location, to_location))
        if fr_location.x == to_location.x:
            if fr_location.y < to_location.y:
                return East()
            else:
                return West()
        else:
            if fr_location.x < to_location.x:
                return North()
            else:
                return South()

    def __rotate(self, node_orientation: Orientation,
                 agent_orientation: Orientation) -> (int, Orientation):
        # Based on scala project with my added adjustments.
        print('__rotate: node_orientation: {}, agent_orientation: {}'.format(node_orientation, agent_orientation))
        turn_left = Action.get_by_value("TURN_LEFT")
        turn_right = Action.get_by_value("TURN_RIGHT")
        if isinstance(node_orientation, North) and isinstance(agent_orientation, East):
            return turn_left, North()
        elif isinstance(node_orientation, South) and isinstance(agent_orientation, East):
            return turn_right, South()
        elif isinstance(node_orientation, West) and isinstance(agent_orientation, East):
            return turn_right, South()
        elif isinstance(node_orientation, North) and isinstance(agent_orientation, West):
            return turn_right, North()
        elif isinstance(node_orientation, South) and isinstance(agent_orientation, West):
            return turn_left, South()
        elif isinstance(node_orientation, East) and isinstance(agent_orientation, West):
            return turn_right, North()
        elif isinstance(node_orientation, South) and isinstance(agent_orientation, North):
            return turn_right, East()
        elif isinstance(node_orientation, East) and isinstance(agent_orientation, North):
            return turn_right, East()
        elif isinstance(node_orientation, West) and isinstance(agent_orientation, North):
            return turn_left, West()
        elif isinstance(node_orientation, North) and isinstance(agent_orientation, South):
            return turn_right, West()
        elif isinstance(node_orientation, East) and isinstance(agent_orientation, South):
            return turn_left, East()
        elif isinstance(node_orientation, West) and isinstance(agent_orientation, South):
            return turn_right, West()
        else:
            raise ValueError("The agent cannot determine how to rotate.")

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
