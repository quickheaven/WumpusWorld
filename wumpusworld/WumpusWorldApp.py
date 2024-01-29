from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.NaiveAgent import NaiveAgent
from wumpusworld.agent.Percept import Percept
from wumpusworld.env.Environment import Environment


def run_episode(env: Environment, agent: Agent, env_percept: Percept):
    if env_percept.is_terminated():
        print("Game Over.")
    else:
        # Get the next action of the Player
        action = agent.next_action(env_percept)

        # Apply the action of the Player and Get the latest Perception
        percept_result = env.apply_action(action)

        # Display the Environment
        env.draw()
        print('\n')

        # Run again an Episode
        run_episode(env, agent, percept_result)


if __name__ == '__main__':
    player = NaiveAgent()

    # Create the Cave
    index_display_start_on_zero: bool = True
    environment = Environment(4, 4, False, 0.0, index_display_start_on_zero)

    # Player enters the Cave
    environment.add_agent(player)

    # Initialize the perception of the Player
    percept = Percept(False, False, False, False, False, False, 0.2)

    # Display the initial setup of the Cave
    print('********* Game Starts *********')
    print('{}'.format(player.to_string()))
    print('{}'.format(percept))
    environment.draw()

    run_episode(environment, player, percept)
