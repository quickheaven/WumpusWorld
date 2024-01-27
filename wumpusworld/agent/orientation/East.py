from wumpusworld.agent.Orientation import Orientation


class East(Orientation):

    def turn_left(self) -> Orientation:
        from wumpusworld.agent.orientation.North import North
        return North()

    def turn_right(self) -> Orientation:
        from wumpusworld.agent.orientation.South import South
        return South()

    def __str__(self):
        return 'East'
