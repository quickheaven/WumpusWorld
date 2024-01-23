from wumpusworld.agent.Agent import Agent


class NaiveAgent(Agent):

    def __init__(self):
        super().__init__()
        self._name = "NAIVE_AGENT"

    def __str__(self):
        return '{}'.format(self._name)

    def next_action(self):
        pass