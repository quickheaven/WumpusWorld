from typing import TYPE_CHECKING

from wumpusworld.agent.Orientation import Orientation

if TYPE_CHECKING:
    from wumpusworld.agent.orientation.East import East
    from wumpusworld.agent.orientation.West import West


class South(Orientation):

    def turn_left(self) -> Orientation:
        return East()

    def turn_right(self) -> Orientation:
        return West()
