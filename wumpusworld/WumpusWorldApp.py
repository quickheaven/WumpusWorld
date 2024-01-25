from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.NaiveAgent import NaiveAgent
from wumpusworld.env.Environment import Environment
from wumpusworld.env.dto.Percept import Percept


def run_episode(env: Environment, agent: Agent, percept: Percept):
    if percept.is_terminated():
        print("Game Over.")
    else:
        # Get the next action of the Player
        action = agent.next_action(percept)

        # Apply the action of the Player and Get the latest Perception
        percept_result = env.apply_action(action)

        # Display the Environment
        env.draw()
        print('\n\n')

        # Run again an Episode
        run_episode(env, agent, percept_result)


if __name__ == '__main__':
    player = NaiveAgent()

    # Create the Cave
    environment = Environment(4, 4, False, 0.2)

    # Player enters the Cave
    environment.add_agent(player)

    # Initialize the perception of the Player
    percept = Percept(False, False, False, False, False, False, 0.0)

    # Display the initial setup of the Cave
    print('********* Game Starts *********')
    print('The Player Initial Perception: {}'.format(percept))
    environment.draw()

    run_episode(environment, player, percept)
