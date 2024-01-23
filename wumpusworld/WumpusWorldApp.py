from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.NaiveAgent import NaiveAgent
from wumpusworld.env.Environment import Environment


def run_episode(env: Environment, agent: Agent):
    env.add_agent(agent)
    env.draw()


if __name__ == '__main__':
    env = Environment(4, 4, False, 0.2)
    agent = NaiveAgent()

    run_episode(env, agent)
