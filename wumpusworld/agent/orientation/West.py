from typing import TYPE_CHECKING

from wumpusworld.agent.Orientation import Orientation

if TYPE_CHECKING:
    from wumpusworld.agent.orientation.South import South
    from wumpusworld.agent.orientation.North import North


class West(Orientation):

    def turn_left(self) -> Orientation:
        return South()

    def turn_right(self) -> Orientation:
        return North()
