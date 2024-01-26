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

    def apply_action(self, action: Action):
        print('Action: {}'.format(action))
        action_id = Action.get_by_value(str(action))

        # TODO
        # a. Study the scala implementation about coordinates.
        # b. Find a way to improve the use of CASE statement in Python
        # c. Remove the Agent from its previous cell. (DONE)
        # d. Develop the concept of Coordinates and find a better way to move around the matrix. Find a better way to limit the movement of the agent within the matrix.
        # f. Develop other actions.
        # g. Develop the concept of rewards.
        cell_agent, agent = self.get_cell_agent()

        percept = None
        match action_id:
            case 0:
                # FORWARD
                x = cell_agent.x
                y = cell_agent.y + 1
                print('OldCell x:{}, y: {} -- NewCell: x:{}, y:{}'.format(cell_agent.x, cell_agent.y, x, y))

                is_bump = x > self._width or y > self._height
                # is_bump = x > self._width - 1
                if is_bump:
                    percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, True,
                                      cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)
                else:
                    new_cell_agent = self._matrix[x][y]
                    new_cell_agent.add_item(agent)
                    is_terminated = self.__is_terminated(new_cell_agent)

                    cell_agent.items.remove(agent)

                    percept = Percept(new_cell_agent.has_stench, new_cell_agent.has_breeze, new_cell_agent.has_glitter,
                                      False, new_cell_agent.has_scream, is_terminated, -1)

            case 1:
                # TURN_LEFT
                x = cell_agent.x + 1
                y = cell_agent.y - 1
                print('OldCell x:{}, y: {} -- NewCell: x:{}, y:{}'.format(cell_agent.x, cell_agent.y, x, y))

                # is_bump = y == -1
                is_bump = x > self._width - 1
                if is_bump:
                    percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, True,
                                      cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)
                else:
                    new_cell_agent = self._matrix[x][y]
                    new_cell_agent.add_item(agent)
                    is_terminated = self.__is_terminated(new_cell_agent)
                    new_cell_agent.is_alive = is_terminated == False

                    cell_agent.items.remove(agent)

                    percept = Percept(new_cell_agent.has_stench, new_cell_agent.has_breeze, new_cell_agent.has_glitter,
                                      False, new_cell_agent.has_scream, is_terminated, -1)

            case 2:
                # TURN_RIGHT
                x = cell_agent.x + 1
                y = cell_agent.y + 1
                print('OldCell x:{}, y: {} -- NewCell: x:{}, y:{}'.format(cell_agent.x, cell_agent.y, x, y))

                is_bump = x > self._width - 1
                if is_bump:
                    percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, True,
                                      cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)
                else:
                    new_cell_agent = self._matrix[x][y]
                    new_cell_agent.add_item(agent)
                    is_terminated = self.__is_terminated(new_cell_agent)
                    new_cell_agent.is_alive = is_terminated == False

                    cell_agent.items.remove(agent)

                    percept = Percept(new_cell_agent.has_stench, new_cell_agent.has_breeze, new_cell_agent.has_glitter,
                                      False, new_cell_agent.has_scream, is_terminated, -1)

            case 3:
                # SHOOT TODO
                print('Unsupported action.')
                percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, False,
                                  cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)

            case 4:
                # GRAB TODO
                print('Unsupported action.')
                percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, False,
                                  cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)
                print(percept)
                return percept

            case 5:
                # CLIMB TODO
                if (self._allow_climb_without_gold == True or (cell_agent.x == 0 and cell_agent == 0)):
                    x = cell_agent.x
                    y = cell_agent.y + 1
                    new_cell_agent = self._matrix[x][y]
                    new_cell_agent.add_item(agent)
                    is_terminated = self.__is_terminated(new_cell_agent)
                    new_cell_agent.is_alive = is_terminated == False

                    cell_agent.items.remove(agent)

                    percept = Percept(new_cell_agent.has_stench, new_cell_agent.has_breeze, new_cell_agent.has_glitter,
                                      False, new_cell_agent.has_scream, is_terminated, -1)

                else:
                    percept = Percept(cell_agent.has_stench, cell_agent.has_breeze, cell_agent.has_glitter, False,
                                      cell_agent.has_scream, self.__is_terminated(cell_agent), 0.0)

        print('Player Perception after the moved: {}'.format(percept))
        return percept

    def __is_terminated(self, cell: Cell):
        return cell.has_wumpus or cell.has_pit


if __name__ == '__main__':
    print('Creating environment')
    env = Environment(4, 4)
    env.draw()
