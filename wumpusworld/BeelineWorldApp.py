from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.MovePlanningAgent import MovePlanningAgent
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
        env.visualize()
        print('\n')

        # Run again an Episode
        run_episode(env, agent, percept_result)


if __name__ == '__main__':
    player = MovePlanningAgent(4, 4)

    # Create the Cave
    index_display_start_on_zero: bool = True  # Set this False if we want to display the grid as [1][1].
    environment = Environment(4, 4, False, 0.0, index_display_start_on_zero)

    # Player enters the Cave
    environment.add_agent(player)

    # Initialize the perception of the Player
    percept = Percept(False, False, False, False, False, False, 0.0)

    # Display the initial setup of the Cave
    print('********* Game Starts *********')
    print('{}'.format(player.to_string()))
    print('{}'.format(percept))
    environment.visualize()

    run_episode(environment, player, percept)
