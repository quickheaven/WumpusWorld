from random import choice

import networkx as nx
import torch
from networkx import Graph
from pomegranate.bayesian_network import BayesianNetwork
from pomegranate.distributions import ConditionalCategorical
from scipy.spatial import distance

from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.AgentState import AgentState
from wumpusworld.agent.Orientation import Orientation
from wumpusworld.agent.Percept import Percept
from wumpusworld.agent.Predicate import Predicate
from wumpusworld.agent.orientation.Coords import Coords
from wumpusworld.agent.orientation.East import East
from wumpusworld.agent.orientation.North import North
from wumpusworld.agent.orientation.South import South
from wumpusworld.agent.orientation.West import West
from wumpusworld.enums.Action import Action
from wumpusworld.env.dto.Cell import Cell


class ProbAgent(Agent):

    def __init__(self, grid_width: int, grid_height: int):
        super().__init__()
        self._name = "PROB_AGENT"
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._agent_state = AgentState()
        self._safe_locations = set()
        self._action_list = []
        # --------------------------------------------------------------------------------------------------
        # [Assignment 3]
        # --------------------------------------------------------------------------------------------------
        self._visited_locations = set()
        self._breeze_locations = set()
        self._stench_locations = set()
        self._heard_scream = False

        self._inferred_pit_prob: float = 0.0
        self._inferred_wum_prob: float = 0.0

        self._matrix = [[Cell(x, y, False) for y in range(self._grid_height)] for x in
                        range(self._grid_width)]

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

        # --------------------------------------------------------------------------------------------------
        # [Assignment 3]
        # --------------------------------------------------------------------------------------------------
        is_visiting_new_location: bool = True
        for loc in self._visited_locations:
            if self._agent_state.location.x == loc.x and self._agent_state.location.y == loc.y:
                is_visiting_new_location = False
                break

        if is_visiting_new_location:
            self._visited_locations.add(self._agent_state.location)

        # new_breeze_locations
        if percept.breeze():
            self._breeze_locations.add(self._agent_state.location)

        # new_stench_locations
        if percept.stench():
            self._stench_locations.add(self._agent_state.location)

        self._heard_scream = self._heard_scream or percept.scream()
        # --------------------------------------------------------------------------------------------------

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

        elif percept.glitter() and not self._agent_state.has_gold:
            self._agent_state.has_gold = True
            self.has_gold = True  # Needed because Environment is looking on Agent and not the agent state.
            action_int = 3  # Grab

        elif percept.stench() and self._agent_state.has_arrow:
            self._agent_state.use_arrow = True

        else:
            # --------------------------------------------------------------------------------------------------
            # [Assignment 3]
            # --------------------------------------------------------------------------------------------------
            # ask one question each time the agent is considering moving to a location in the grid it has never been
            if is_visiting_new_location:
                self._inferred_pit_prob = self.__get_cell_probability_having_pit(percept)
                self._inferred_wum_prob = self.__get_cell_probability_having_wumpus(percept)

            action_int = self.__search_for_gold(percept, 0.40)
            # --------------------------------------------------------------------------------------------------

        return Action.get_by_id(action_int)

    def __search_for_gold(self, percept: Percept, tolerance: float):
        print(f"__search_for_gold : self._inferred_pit_prob: {self._inferred_pit_prob}, self._inferred_wum_prob: "
              f"{self._inferred_wum_prob}, tolerance: {tolerance}")

        """
        val forwardLocation = agentState.forward(gridWidth, gridHeight).location
            if (percept.bump || forwardLocation == agentState.location || !safeLocations.contains(forwardLocation))
              (agentState.turnRight, TurnRight)
            else randGen.nextInt(3) match {
              case 0 => (agentState.forward(gridWidth, gridHeight), Forward)
              case 1 => (agentState.forward(gridWidth, gridHeight), Forward)
              case 2 => (agentState.turnRight, TurnRight)
            }
        """

        forward_location = self._agent_state.forward(self._grid_width, self._grid_height, False)

        if percept.bump() or (
                forward_location.x == self._agent_state.location.x and forward_location.y == self._agent_state.location.y):
            action_int = 2  # Turn Right (Copied from Scala)
        else:
            # Your agent will need to take risks and occasionally die to play its long-run best.
            # Arjie: There are better way to do this.....
            indexes = [i for i in range(3)]
            action_int = choice(indexes)

        """
        if self._inferred_pit_prob < tolerance or self._inferred_wum_prob < tolerance:
            if percept.bump():
                action_int = 1  # Turn Right (Copied from Scala)
            else:
                action_int = 0  # Forward
        else:
            # Your agent will need to take risks and occasionally die to play its long-run best.
            # Arjie: There are better way to do this.....
            indexes = [i for i in range(3)]
            action_int = choice(indexes)
        """

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

    def __find_adjacent_cells(self, cell: Cell):
        x = cell.x
        y = cell.y
        adjacent_cells = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < self._grid_width and 0 <= j < self._grid_height and (i, j) != (x, y) and abs(i - x) + abs(
                        j - y) == 1:
                    adjacent_cells.append(self._matrix[i][j])
        return adjacent_cells

    def __is_cell_visited(self, cell: Cell):
        is_visited = -1
        for coord in self._visited_locations:
            if coord.get()[0] == cell.x and coord.get()[1] == cell.y:
                is_visited = 0
                break
        return is_visited

    def __get_cell_probability_having_pit(self, percept: Percept) -> float:

        adjacent_cells = self.__find_adjacent_cells(
            Cell(self._agent_state.location.x, self._agent_state.location.y))
        num_of_adjacent_cells = len(adjacent_cells)

        print(
            f"[{self._agent_state.location.x}][{self._agent_state.location.y}] The number of adjacent cells {num_of_adjacent_cells}")

        """
        # You will only need to ask one question at a time, each time the agent is considering moving to a location
        # in the grid it has never been
        # You'll be interested in the probability of there being a hazard (a pit or the Wumpus) in all of the locations
        # the agent can get to without stepping outside locations it has previously been and choose the safest one to
        # go to (or beeline out if the risk is too great)
        # Prepare a list with 0 for every pit location the agent has been (because its safe: the agent didn't die),
        # -1 for all others; and for the breeze locations: 0 if no breeze detected there, 1 if so, -1 if unknown
        # Then call predict_proba() and pull out the probabilities of interest
        """

        proba = 0.0

        is_breeze = 0
        if percept.breeze():
            is_breeze = 1

        if num_of_adjacent_cells == 2:
            loc01 = Predicate(0.2).toCategorical()
            loc02 = Predicate(0.2).toCategorical()

            breeze = ConditionalCategorical([[
                [[1.0, 0.0], [0.0, 1.0]],
                [[0.0, 1.0], [0.0, 1.0]]
            ]])

            variables = [loc01, loc02, breeze]
            edges = [(loc01, breeze), (loc02, breeze)]

            pits_model = BayesianNetwork(variables, edges)

            # This the original tensor from the example:
            # X = torch.tensor([[-1, -1, 0],  # pit12?, pit21?, breeze is false
            #                  [-1, -1, 1],  # pit12?, pit21?, breeze is true
            #                  [-1, -1, -1],  # pit12?, pit21?, breeze?
            #                  [1, -1, -1]  # pit12 is true, pit21?, breeze?
            #                  ])

            adjacent_cell01_possible_pit = self.__is_cell_visited(adjacent_cells[0])
            adjacent_cell02_possible_pit = self.__is_cell_visited(adjacent_cells[1])

            print(f"Tensor: [{adjacent_cell01_possible_pit}, {adjacent_cell02_possible_pit}, {is_breeze}]")
            X = torch.tensor([
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, 0],
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, 1]
            ])
            # X = torch.tensor([
            #     [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, is_breeze],
            # ])

            X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)

            predicted_pits_proba = pits_model.predict_proba(X_masked)

            print(f"TWO parents: {predicted_pits_proba}")
            if is_breeze:
                proba = predicted_pits_proba[1][1][1]
                print(f"is_breeze: 1, proba: {proba}")
            else:
                proba = predicted_pits_proba[0][1][1]
                print(f"is_breeze: 0, proba: {proba}")

        elif num_of_adjacent_cells == 3:
            loc01 = Predicate(0.2).toCategorical()
            loc02 = Predicate(0.2).toCategorical()
            loc03 = Predicate(0.2).toCategorical()

            breeze = ConditionalCategorical([[
                [
                    [[1.0, 0.0], [0.0, 1.0]],
                    [[0.0, 1.0], [0.0, 1.0]]
                ],
                [
                    [[1.0, 0.0], [0.0, 1.0]],
                    [[0.0, 1.0], [0.0, 1.0]]
                ]
            ]])

            variables = [loc01, loc02, loc03, breeze]
            edges = [(loc01, breeze), (loc02, breeze), (loc03, breeze)]

            pits_model = BayesianNetwork(variables, edges)

            # X = torch.tensor([[-1, -1, -1, 0],
            #                  [-1, -1, -1, 1],
            #                  [-1, -1, -1, -1],
            #                  [1, -1, -1, -1],
            #                  [0, -1, -1, -1]
            #                  ])

            adjacent_cell01_possible_pit = self.__is_cell_visited(adjacent_cells[0])
            adjacent_cell02_possible_pit = self.__is_cell_visited(adjacent_cells[1])
            adjacent_cell03_possible_pit = self.__is_cell_visited(adjacent_cells[2])

            print(
                f"Tensor: [{adjacent_cell01_possible_pit}, {adjacent_cell02_possible_pit}, {adjacent_cell03_possible_pit}, {is_breeze}]")
            X = torch.tensor([
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit, 0],
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit, 1]
            ])
            # X = torch.tensor([
            #    [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit, is_breeze]
            # ])

            X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)

            predicted_pits_proba = pits_model.predict_proba(X_masked)
            print(f"THREE parents: {predicted_pits_proba}")
            # proba = predicted_pits_proba[0][1][0]
            if is_breeze:
                proba = predicted_pits_proba[1][1][1]
                print(f"is_breeze: 1, proba: {proba}")
            else:
                proba = predicted_pits_proba[0][1][1]
                print(f"is_breeze: 0, proba: {proba}")

        elif num_of_adjacent_cells == 4:
            loc01 = Predicate(0.2).toCategorical()
            loc02 = Predicate(0.2).toCategorical()
            loc03 = Predicate(0.2).toCategorical()
            loc04 = Predicate(0.2).toCategorical()

            breeze = ConditionalCategorical([[
                [
                    [
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[0.0, 1.0], [0.0, 1.0]]
                    ],
                    [
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[0.0, 1.0], [0.0, 1.0]]
                    ]
                ],
                [
                    [
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[0.0, 1.0], [0.0, 1.0]]
                    ],
                    [
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[0.0, 1.0], [0.0, 1.0]]
                    ]
                ]
            ]])

            variables = [loc01, loc02, loc03, loc04, breeze]
            edges = [(loc01, breeze), (loc02, breeze), (loc03, breeze), (loc04, breeze)]

            pits_model = BayesianNetwork(variables, edges)

            # X = torch.tensor([[-1, -1, -1, -1, 0],
            #                  [-1, -1, -1, -1, 1],
            #                  [-1, -1, -1, -1, -1],
            #                  [1, -1, -1, -1, -1]
            #                  ])

            adjacent_cell01_possible_pit = self.__is_cell_visited(adjacent_cells[0])
            adjacent_cell02_possible_pit = self.__is_cell_visited(adjacent_cells[1])
            adjacent_cell03_possible_pit = self.__is_cell_visited(adjacent_cells[2])
            adjacent_cell04_possible_pit = self.__is_cell_visited(adjacent_cells[3])

            print(
                f"Tensor: [{adjacent_cell01_possible_pit}, {adjacent_cell02_possible_pit}, {adjacent_cell03_possible_pit}, {adjacent_cell04_possible_pit}, {is_breeze}]")
            X = torch.tensor([
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit,
                 adjacent_cell04_possible_pit, 0],
                [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit,
                 adjacent_cell04_possible_pit, 1]
            ])
            # X = torch.tensor([
            #    [adjacent_cell01_possible_pit, adjacent_cell02_possible_pit, adjacent_cell03_possible_pit,
            #      adjacent_cell04_possible_pit, is_breeze]
            # ])

            X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)

            predicted_pits_proba = pits_model.predict_proba(X_masked)
            print(f"FOUR parents: {predicted_pits_proba}")
            # proba = predicted_pits_proba[0][1][0]
            if is_breeze:
                proba = predicted_pits_proba[1][1][1]
                print(f"is_breeze: 1, proba: {proba}")
            else:
                proba = predicted_pits_proba[0][1][1]
                print(f"is_breeze: 0, proba: {proba}")

        return proba

    def __get_cell_probability_having_wumpus(self, percept: Percept) -> float:
        return self.__get_cell_probability_having_pit(percept)  # TODO
