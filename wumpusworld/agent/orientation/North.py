from typing import TYPE_CHECKING

from wumpusworld.agent.Orientation import Orientation

if TYPE_CHECKING:
    from wumpusworld.agent.orientation.East import East
    from wumpusworld.agent.orientation.West import West


class North(Orientation):

    def turn_left(self) -> Orientation:
        return West()

    def turn_right(self) -> Orientation:
        return East()
