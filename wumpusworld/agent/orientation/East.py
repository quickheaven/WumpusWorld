from typing import TYPE_CHECKING

from wumpusworld.agent.Orientation import Orientation

if TYPE_CHECKING:
    from wumpusworld.agent.orientation.North import North
    from wumpusworld.agent.orientation.South import South


class East(Orientation):

    def turn_left(self) -> Orientation:
        return North()

    def turn_right(self) -> Orientation:
        return South()
