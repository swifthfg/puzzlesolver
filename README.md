# puzzlesolver

An artificial intelligence that solves the sliding block puzzle using _A*-search_ Algorithm. It takes the board's initial position and the final position. From a certain state it moves blocks one unit at a time, namely _right_, _left_, _up_ or _down_, to the empty spaces in certain combinations to get a certain block out of the grid, i.e the final state. 

In this project, _Manhattan distance_ and _direct Euclidean distance_ heuristics are used. Those heuristic can be set while giving input to the program.

#### Here is the example game play using graphical interface:
![alt text][example-game-play]

[example-game-play]: https://github.com/swifthfg/puzzlesolver/blob/master/resources/example-game-play.png