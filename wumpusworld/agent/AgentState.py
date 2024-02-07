from wumpusworld.agent.orientation.Coords import Coords
from wumpusworld.agent.orientation.East import East
from wumpusworld.agent.orientation.North import North
from wumpusworld.agent.orientation.South import South
from wumpusworld.agent.orientation.West import West
from wumpusworld.enums.Action import Action


class AgentState:

    def __init__(self):
        self._location = Coords(0, 0)
        self._orientation = East
        self._has_gold = False
        self._has_arrow = False
        self._is_alive = True

    @property
    def has_gold(self) -> bool:
        return self._has_gold

    @property
    def has_arrow(self) -> bool:
        return self._has_arrow

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @property
    def location(self) -> Coords:
        return self._location

    def turn_left(self):
        self._orientation = self._orientation.turn_left

    def turn_right(self):
        self._orientation = self._orientation.turn_right

    def forward(self, grid_width: int, grid_height: int):
        new_agent_location = None
        if isinstance(self._orientation, West):
            new_agent_location = Coords(self._location.x, max(0, self._location.y - 1))

        elif isinstance(self._orientation, East):
            new_agent_location = Coords(self._location.x, min(grid_height - 1, self._location.y + 1))

        elif isinstance(self._orientation, South):
            new_agent_location = Coords(max(0, self._location.x - 1), self._location.y)

        elif isinstance(self._orientation, North):
            new_agent_location = Coords(min(grid_width - 1, self._location.x + 1), self._location.y)

        self._location = new_agent_location

        return new_agent_location

    def use_arrow(self):
        self._hasArrow = False

    def apply_move_action(self, action: Action, grid_width: int, grid_height: int):
        action_id: int = Action.get_by_value(str(action))
        match action_id:
            case 0:  # FORWARD
                self.forward(grid_width, grid_height)
            case 1:  # TURN LEFT
                self.turn_left()
            case 2:  # TURN RIGHT
                self.turn_right()
