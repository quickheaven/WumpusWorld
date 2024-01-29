import random
from texttable import Texttable

from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.orientation.East import East
from wumpusworld.agent.orientation.North import North
from wumpusworld.agent.orientation.South import South
from wumpusworld.agent.orientation.West import West
from wumpusworld.enums.Action import Action
from wumpusworld.enums.CellState import CellState
from wumpusworld.env.dto.Cell import Cell
from wumpusworld.env.dto.Gold import Gold
from wumpusworld.agent.Percept import Percept
from wumpusworld.env.dto.Pit import Pit
from wumpusworld.env.dto.Wumpus import Wumpus

'''
Wumpus World HAS-A Environment:
Environment HAS-A Matrix (Cave).
Each element of Matrix IS-A Cell (Room).
The Cell HAS-A Item(s) that can be Gold, Pit and Wumpus (extends the Item).
The Cell HAS-A State(s) that can be Stench, Breeze, Glitter, Scream. 

Wumpus World HAS-A Agent:
The Agent HAS-A next action that can be Forward, Turn Left, Turn Right, Shoot, Grab and Climb.
The Agent HAS-A access to 'Perception'.
'''


class Environment:

    def __init__(self, width, height, allow_climb_without_gold=False, pit_prob=0.2,
                 index_display_start_on_zero: bool = False):
        self._width = width
        self._height = height
        self._allow_climb_without_gold = allow_climb_without_gold
        self._pit_prob = pit_prob
        self._index_display_start_on_zero = index_display_start_on_zero

        # print('Initializing Game...')
        # print('Grid width: {}, Grid height: {}, _allow_climb_without_gold: {}, pit_prob: {}'.format(self._width, self._height, self._allow_climb_without_gold, self._pit_prob))
        self.__reset()

    def __reset(self):
        # Build the initial matrix
        # The matrix is also the Cave while the Cell is the Room.
        self._matrix = [[Cell(x, y, self._index_display_start_on_zero) for y in range(self._height)] for x in
                        range(self._width)]

        # Put the Gold, Pit and Wumpus in random Cell (excluding the first Cell).
        matrix_excluding_first_element = [x[1:] for x in self._matrix]

        cell_gold = random.choice(random.choice(matrix_excluding_first_element))
        cell_gold.add_item(Gold())
        cell_gold.add_cell_state(CellState.GLITTER)

        cell_wumpus = random.choice(random.choice(matrix_excluding_first_element))
        cell_wumpus.add_item(Wumpus())

        adjacent_cells = self.__find_adjacent_cells(cell_wumpus)
        for cell in adjacent_cells:
            cell.add_cell_state(CellState.STENCH)

        pit_locations = []
        cell_indexes = [(x, y) for x in range(self._width) for y in range(self._height)]
        for cell in cell_indexes[1:]:
            if random.random() < self._pit_prob:
                pit_locations.append(cell)

        # print('Pit Locations: {}'.format(pit_locations))
        for pit_loc in pit_locations:
            cell_pit = self._matrix[pit_loc[0]][pit_loc[1]]
            if cell_pit.is_empty():
                cell_pit.add_item(Pit())
                adjacent_cells = self.__find_adjacent_cells(cell_pit)
                for cell in adjacent_cells:
                    cell.add_cell_state(CellState.BREEZE)

    def __find_adjacent_cells(self, cell: Cell):
        x = cell.x
        y = cell.y
        adjacent_cells = []
        # I researched this from the internet.
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < self._width and 0 <= j < self._height and (i, j) != (x, y) and abs(i - x) + abs(j - y) == 1:
                    adjacent_cells.append(self._matrix[i][j])
        return adjacent_cells

    def draw(self):
        table = Texttable()
        table.add_rows(self._matrix[::-1]
                       # This will reverse the order so the bottom index [0][0] will be displayed in the bottom.
                       , header=None)
        print(table.draw())

        # table = Texttable()
        # table.add_rows(self._matrix
        # This will reverse the order so the bottom index [0][0] will be displayed in the bottom.
        #               , header=None)
        # print(table.draw())

    def add_agent(self, agent: Agent):
        cell_agent = self._matrix[0][0]
        cell_agent.add_item(agent)

    def get_cell_agent(self):
        cell_agent = None
        agent = None
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                items = self._matrix[i][j].items
                for item in items:
                    if isinstance(item, Agent):
                        cell_agent = self._matrix[i][j]
                        agent = item
                        break
        return cell_agent, agent

    def get_cell_wumpus(self):
        cell_wumpus = None
        wumpus = None
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                items = self._matrix[i][j].items
                for item in items:
                    if isinstance(item, Wumpus):
                        cell_wumpus = self._matrix[i][j]
                        wumpus = item
                        break
        return cell_wumpus, wumpus

    def apply_action(self, action: Action):

        action_id = Action.get_by_value(str(action))
        print('Action: {}'.format(action))

        cell_of_agent, agent = self.get_cell_agent()

        percept = None

        match action_id:
            case 0:
                new_agent_location = agent.forward(self._width, self._height)
                new_cell_of_agent = self._matrix[new_agent_location.x][new_agent_location.y]

                bump = cell_of_agent.x == new_cell_of_agent.x and cell_of_agent.y == new_cell_of_agent.y

                cell_wumpus, wumpus = self.get_cell_wumpus()

                death = (new_cell_of_agent.has_wumpus and wumpus.is_alive) or new_cell_of_agent.has_pit

                agent.has_gold = new_cell_of_agent.has_glitter
                agent.is_alive = not death

                new_cell_of_agent.add_item(agent)
                cell_of_agent.items.remove(agent)

                reward: float = -1
                if not agent.is_alive:
                    reward: float = -1001

                percept = Percept(new_cell_of_agent.has_stench, new_cell_of_agent.has_breeze,
                                  new_cell_of_agent.has_glitter, bump, new_cell_of_agent.has_scream, death, reward)

            case 1:
                agent.turn_left()
                percept = Percept(cell_of_agent.has_stench, cell_of_agent.has_breeze, cell_of_agent.has_glitter, False,
                                  False, False, -1)
            case 2:
                agent.turn_right()
                percept = Percept(cell_of_agent.has_stench, cell_of_agent.has_breeze, cell_of_agent.has_glitter, False,
                                  False, False, -1)
            case 3:
                agent.has_gold = cell_of_agent.has_glitter

                percept = Percept(cell_of_agent.has_stench, cell_of_agent.has_breeze, cell_of_agent.has_glitter, False,
                                  False, False, -1)
            case 4:
                in_start_location: bool = cell_of_agent.x == 0 and cell_of_agent.y == 0
                success: bool = agent.has_gold and in_start_location
                is_terminated: bool = success or (self._allow_climb_without_gold and in_start_location)
                reward: float = -1
                if success:
                    reward = 999

                percept = Percept(cell_of_agent.has_stench, cell_of_agent.has_breeze, cell_of_agent.has_glitter, False,
                                  False, is_terminated, reward)
            case 5:
                had_arrow: bool = agent.has_arrow

                wumpus_killed: bool = self.__kill_attempt_successful(agent)
                agent.has_arrow = False

                reward: float = -1
                if had_arrow:
                    reward: float = -11

                percept = Percept(cell_of_agent.has_stench, cell_of_agent.has_breeze, cell_of_agent.has_glitter, False,
                                  False, wumpus_killed, reward)

        print(agent.to_string())
        print(percept)
        return percept

    def __kill_attempt_successful(self, agent: Agent) -> bool:
        cell_wumpus, wumpus = self.get_cell_wumpus()

        wumpus_in_line_of_fire: bool = False
        if isinstance(agent.orientation, West):
            wumpus_in_line_of_fire = agent.location.x == cell_wumpus.x and agent.location.y > cell_wumpus.y

        elif isinstance(agent.orientation, East):
            wumpus_in_line_of_fire = agent.location.x == cell_wumpus.x and agent.location.y < cell_wumpus.y

        elif isinstance(agent.orientation, South):
            wumpus_in_line_of_fire = agent.location.x > cell_wumpus.x and agent.location.y == cell_wumpus.y

        elif isinstance(agent.orientation, North):
            wumpus_in_line_of_fire = agent.location.x < cell_wumpus.x and agent.location.y == cell_wumpus.y

        wumpus_killed = agent.has_arrow and wumpus_in_line_of_fire and wumpus_in_line_of_fire
        wumpus.is_alive = not wumpus_killed
        print(
            'Orientation: {} Agent_Location:[{}][{}] Wumpus_Location:[{}][{}] Wumpus_Alive: {}'.format(agent.orientation,
                                                                                                    agent.location.x,
                                                                                                    agent.location.y,
                                                                                                    cell_wumpus.x,
                                                                                                    cell_wumpus.y,
                                                                                                    wumpus.is_alive))

        return wumpus_killed


if __name__ == '__main__':
    print('Creating environment')
    env = Environment(4, 4)
    env.draw()
