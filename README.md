# WumpusWorld

@author Arjie Cristobal
<pre>
The app was developed using OOP with Python. The basic design is based on the following: <br/>
A. The Wumpus World HAS-A Environment.
  Environment HAS-A Matrix (Cave).
  Each element of Matrix IS-A Cell (Room).
  The Cell HAS-A Item(s) that can be Gold, Pit and Wumpus (extends the Item).
  The Cell HAS-A State(s) that can be Stench, Breeze, Glitter, Scream.

B. The Wumpus World also HAS-A Agent (Player) that will explore the Environment.
  The Agent have a behavior to perform the 'next action' which can be Forward, Turn Left, Turn Right, Shoot, Grab and Climb.
  The Agent HAS-A 'Orientation' and 'Perception'.
  
</pre>
Below is sample start and game ends.

*The Environment parameter index_display_start_on_zero is set to False.*

The WumpusWorld Game starts:

```
********* Game Starts *********
NAIVE_AGENT Gold: False, Arrow: True, Alive: True, Coords: (0,0), Orientation: East
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: False, Reward: 0.0
+---------------------+--------------------+-------------------+---------------+
| Cell [3][0]:        | Cell [3][1]:       | Cell [3][2]:      | Cell [3][3]:  |
| STENCH              | WUMPUS (A)         | STENCH BREEZE     |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [2][0]:        | Cell [2][1]:       | Cell [2][2]: PIT  | Cell [2][3]:  |
|                     | STENCH BREEZE      |                   | BREEZE        |
+---------------------+--------------------+-------------------+---------------+
| Cell [1][0]:        | Cell [1][1]:       | Cell [1][2]: GOLD | Cell [1][3]:  |
|                     |                    | GLITTER BREEZE    |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [0][0]:        | Cell [0][1]:       | Cell [0][2]:      | Cell [0][3]:  |
| NAIVE_AGENT (A)     |                    |                   |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
```

After the the agent made several moves, the game ends after the agent steps to a Pit.

```
The Agent dies a miserable death because it enters a cell containing a Pit.
NAIVE_AGENT Gold: False, Arrow: False, Alive: False, Coords: (2,2), Orientation: East
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: True, Reward: -1001
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]: WUMPUS   | Cell [3][2]:         | Cell [3][3]:  |
| STENCH        | (A)                   | STENCH BREEZE        |               |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]: PIT     | Cell [2][3]:  |
|               | STENCH BREEZE         | NAIVE_AGENT (D)      | BREEZE        |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]:          | Cell [1][2]: GOLD    | Cell [1][3]:  |
|               |                       | GLITTER BREEZE       |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+


Game Over.
```

## Move Planning Agent
This agent is capable of returning back safely after grabbing the gold.

```
MovePlanningAgent.next_action: 
agent_state: location: (1,2), orientation: North, has_gold: False, has_arrow: False, is_alive: True, 
safe_locations: {(0, 1), (0, 2), (1, 2), (0, 0)}, 
Environment apply_action: FORWARD
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (1,2), Orientation: North
PERCEPTION Stench: True, Breeze: False, Glitter: True, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (↑)              |               |
|               |                       | GLITTER STENCH       |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
Environment apply_action: GRAB
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (1,2), Orientation: North
PERCEPTION Stench: True, Breeze: False, Glitter: True, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (↑)              |               |
|               |                       | GLITTER STENCH       |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Building the escape plan using networkx.
Source Node: (1, 2), Target Node: (0, 0)
The shortest path: [(1, 2), (0, 2), (0, 1), (0, 0)]
__direction fr_location: (1,2), to_location: (0,2)
__rotate: node_orientation: South, agent_orientation: North
__direction fr_location: (1,2), to_location: (0,2)
__rotate: node_orientation: South, agent_orientation: East
__direction fr_location: (1,2), to_location: (0,2)
__direction fr_location: (0,2), to_location: (0,1)
__rotate: node_orientation: West, agent_orientation: South
__direction fr_location: (0,2), to_location: (0,1)
__direction fr_location: (0,1), to_location: (0,0)
The action list of the escape plan [2, 2, 0, 2, 0, 0].
Environment apply_action: TURN_RIGHT
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (1,2), Orientation: East
PERCEPTION Stench: True, Breeze: False, Glitter: True, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (→)              |               |
|               |                       | GLITTER STENCH       |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Execute the escape plan based on action_list [2, 0, 2, 0, 0].
Environment apply_action: TURN_RIGHT
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (1,2), Orientation: South
PERCEPTION Stench: True, Breeze: False, Glitter: True, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (↓)              |               |
|               |                       | GLITTER STENCH       |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Execute the escape plan based on action_list [0, 2, 0, 0].
Environment apply_action: FORWARD
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (0,2), Orientation: South
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | GLITTER STENCH       |               |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (↓)              |               |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Execute the escape plan based on action_list [2, 0, 0].
Environment apply_action: TURN_RIGHT
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (0,2), Orientation: West
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+-----------------------+----------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:          | Cell [3][2]:         | Cell [3][3]:  |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:          | Cell [2][2]:         | Cell [2][3]:  |
|               | STENCH                |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS   | Cell [1][2]: GOLD    | Cell [1][3]:  |
| STENCH        | (A)                   | GLITTER STENCH       |               |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:          | Cell [0][2]:         | Cell [0][3]:  |
|               | STENCH                | MOVE_PLANNING_AGENT  |               |
|               |                       | (A) (←)              |               |
|               |                       |                      |               |
+---------------+-----------------------+----------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Execute the escape plan based on action_list [0, 0].
Environment apply_action: FORWARD
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (0,1), Orientation: West
PERCEPTION Stench: True, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------+--------------------------+-------------------+---------------+
| Cell [3][0]:  | Cell [3][1]:             | Cell [3][2]:      | Cell [3][3]:  |
|               |                          |                   |               |
+---------------+--------------------------+-------------------+---------------+
| Cell [2][0]:  | Cell [2][1]:             | Cell [2][2]:      | Cell [2][3]:  |
|               | STENCH                   |                   |               |
+---------------+--------------------------+-------------------+---------------+
| Cell [1][0]:  | Cell [1][1]: WUMPUS (A)  | Cell [1][2]: GOLD | Cell [1][3]:  |
| STENCH        |                          | GLITTER STENCH    |               |
+---------------+--------------------------+-------------------+---------------+
| Cell [0][0]:  | Cell [0][1]:             | Cell [0][2]:      | Cell [0][3]:  |
|               | MOVE_PLANNING_AGENT (A)  |                   |               |
|               | (←)                      |                   |               |
|               | STENCH                   |                   |               |
+---------------+--------------------------+-------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
Execute the escape plan based on action_list [0].
Environment apply_action: FORWARD
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (0,0), Orientation: West
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: False, Reward: -1
+---------------------+--------------------+-------------------+---------------+
| Cell [3][0]:        | Cell [3][1]:       | Cell [3][2]:      | Cell [3][3]:  |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [2][0]:        | Cell [2][1]:       | Cell [2][2]:      | Cell [2][3]:  |
|                     | STENCH             |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [1][0]:        | Cell [1][1]:       | Cell [1][2]: GOLD | Cell [1][3]:  |
| STENCH              | WUMPUS (A)         | GLITTER STENCH    |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [0][0]:        | Cell [0][1]:       | Cell [0][2]:      | Cell [0][3]:  |
| MOVE_PLANNING_AGENT | STENCH             |                   |               |
| (A) (←)             |                    |                   |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
```

```
The agent have the gold. Performing the escape plan.
**** The agent wins the game. ****
Environment apply_action: CLIMB
MOVE_PLANNING_AGENT Gold: True, Arrow: False, Alive: True, Coords: (0,0), Orientation: West
PERCEPTION Stench: False, Breeze: False, Glitter: False, Bump: False, Scream: False, Is_Terminated: True, Reward: 999
+---------------------+--------------------+-------------------+---------------+
| Cell [3][0]:        | Cell [3][1]:       | Cell [3][2]:      | Cell [3][3]:  |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [2][0]:        | Cell [2][1]:       | Cell [2][2]:      | Cell [2][3]:  |
|                     | STENCH             |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [1][0]:        | Cell [1][1]:       | Cell [1][2]: GOLD | Cell [1][3]:  |
| STENCH              | WUMPUS (A)         | GLITTER STENCH    |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+
| Cell [0][0]:        | Cell [0][1]:       | Cell [0][2]:      | Cell [0][3]:  |
| MOVE_PLANNING_AGENT | STENCH             |                   |               |
| (A) (←)             |                    |                   |               |
|                     |                    |                   |               |
+---------------------+--------------------+-------------------+---------------+

Game Over.
```
