from wumpusworld.agent.Agent import Agent
from wumpusworld.agent.NaiveAgent import NaiveAgent
from wumpusworld.agent.Percept import Percept
from wumpusworld.env.Environment import Environment

"""
The Wumpus World App.

@author Arjie Cristobal

The app was developed using OOP with Python. The basic design is based on the following:
A.  The Wumpus World HAS-A Environment.
    Environment HAS-A Matrix (Cave).
    Each element of Matrix IS-A Cell (Room).
    The Cell HAS-A Item(s) that can be Gold, Pit and Wumpus (extends the Item).
    The Cell HAS-A State(s) that can be Stench, Breeze, Glitter, Scream. 

B.  The Wumpus World also HAS-A Agent (Player) that will explore the Environment.
    The Agent have a behavior to perform the 'next action' which can be Forward, Turn Left, Turn Right, Shoot, Grab and Climb.
    The Agent HAS-A 'Orientation' and 'Perception'.
"""


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
    player = NaiveAgent()

    # Create the Cave
    index_display_start_on_zero: bool = True
    environment = Environment(4, 4, False, 0.2, index_display_start_on_zero)

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
