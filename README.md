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
