import random
from texttable import Texttable

from wumpusworld.agent.Agent import Agent
from wumpusworld.enums.Action import Action
from wumpusworld.enums.CellState import CellState
from wumpusworld.env.dto.Cell import Cell
from wumpusworld.env.dto.Gold import Gold
from wumpusworld.env.dto.Percept import Percept
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

    def __init__(self, width, height, allow_climb_without_gold=False, pit_prob=0.2):
        self._width = width
        self._height = height
        self._allow_climb_without_gold = allow_climb_without_gold
        self._pit_prob = pit_prob

        self.__reset()

    def __reset(self):
        # Build the initial matrix
        # The matrix is also the Cave while the Cell is the Room.
        self._matrix = [[Cell(x, y) for y in range(self._height)] for x in range(self._width)]

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

        # TODO used _pit_prob
        matrix_excluding_first_two_element = [x[2:] for x in self._matrix]
        cell_pit = random.choice(random.choice(matrix_excluding_first_two_element))
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

        #table = Texttable()
        #table.add_rows(self._matrix
                       # This will reverse the order so the bottom index [0][0] will be displayed in the bottom.
        #               , header=None)
        #print(table.draw())

    def add_agent(self, agent: Agent):
        cell_agent = self._matrix[0][0]
        cell_agent.add_item(agent)

    def apply_action(self, action: Action):
        print('Action: {}'.format(action))
        action_id = Action.get_by_value(str(action))

        # TODO study the scala implementation and do the same here.
        # Find a way to improve the use of case statement in Python
        match action_id:
            case 0:
                pass
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case _:
                pass
        return Percept(False, False, False, False, False, True, 0.0)


if __name__ == '__main__':
    print('Creating environment')
    env = Environment(4, 4)
    env.draw()
