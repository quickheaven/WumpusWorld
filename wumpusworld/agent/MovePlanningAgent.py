from random import choice
import matplotlib.pyplot as plt
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
            print('The agent have the gold. Performing the escape plan.')
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
                    # --------------------------------------------------------------------------------------------------
                    #  Agent keeps track of safe locations (5pts)
                    # --------------------------------------------------------------------------------------------------

                    agent_old_location = self._agent_state.location
                    agent_old_orientation = self._agent_state.orientation

                    #  move may not actually be safe, but if not agent will be dead so doesn't matter
                    agent_new_safe_location = self._agent_state.forward(self._grid_width, self._grid_height)
                    agent_new_orientation = self._agent_state.orientation

                    is_loc_changed: bool = (agent_old_location.x != agent_new_safe_location.x
                                            or agent_old_location.y != agent_new_safe_location.y)
                    if is_loc_changed:
                        self._safe_locations.add(
                            (agent_new_safe_location, agent_old_location, agent_new_orientation, agent_old_orientation))

                case 1:
                    self._agent_state.turn_left()
                case 2:
                    self._agent_state.turn_right()
                case 2:
                    self._agent_state.use_arrow = True

        safe_locations = ['From Coords: ({},{}) To Coords: ({},{}) :: New Orientation: {}, Old Orientation: {}'
                          .format(old_coords.x, old_coords.y, new_coords.x, new_coords.y, str(new_orientation),
                                  str(old_orientation)) for
                          new_coords, old_coords, new_orientation, old_orientation in self._safe_locations]

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

        for new_loc, old_loc, new_orient, old_orient in self._safe_locations:
            # Build the nodes
            node = ((new_loc.x, new_loc.y), {'orientation': new_orient})
            nodes.append(node)

            # Build the edges : (from location, to location)
            edge = ((old_loc.x, old_loc.y), (new_loc.x, new_loc.y))
            edges.append(edge)

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
        """
        Example: 
        edges: [((2, 0), (2, 1)), ((0, 0), (1, 0)), ((2, 1), (3, 1)), ((1, 0), (2, 0))]
        Source Node: (3, 1), Target Node: (0, 0)
        The shortest path: [(3, 1), (2, 1), (2, 0), (1, 0), (0, 0)]
        
        safe_locations: ['From Coords: (2,0) To Coords: (2,1) :: New Orientation: East, Old Orientation: East', 
        'From Coords: (0,0) To Coords: (1,0) :: New Orientation: North, Old Orientation: North', 
        'From Coords: (2,1) To Coords: (3,1) :: New Orientation: North, Old Orientation: North', 
        'From Coords: (1,0) To Coords: (2,0) :: New Orientation: North, Old Orientation: North'],
        """
        # TODO
        # Loop the shortest_path
        #   Find the relation between the nodes of shortest path.
        #   Based on a given orientation, adjust how to turn-around. Include this on the plan.
        #

        escape_plan = []  # TODO build the escape plan

        return escape_plan

    def to_string(self) -> str:
        parent_class_str = super().__str__()
        return '{} {}'.format(self._name, parent_class_str)
