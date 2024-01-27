from wumpusworld.agent.Orientation import Orientation


class North(Orientation):

    def turn_left(self) -> Orientation:
        from wumpusworld.agent.orientation.West import West
        return West()

    def turn_right(self) -> Orientation:
        from wumpusworld.agent.orientation.East import East
        return East()

    def __str__(self):
        return 'North'
