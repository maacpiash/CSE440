## Assignment 2
Submitted on October 28, 2017<br>
 
### Problem: Applying Minimax to build an AI MaxConnect4 player
The task here is to implement an agent that plays the Max-Connect4 game using the depth-limited version of MiniMax, with alpha-beta pruning. Here is [a quick guide](http://web.mit.edu/sp.268/www/2010/connectFourSlides.pdf) that explains how the game is supposed to work.

#### Input format:
There are two modes of the game: Interactive and One-Move mode.<br/><br/>
**Interactive Mode:**<br/>
In interactive mode, the game should run from the command line with the following arguments:
```
$ python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]
```
For example:
`$ python maxconnect4.py interactive input1.txt computer-next 7`
- Argument `interactive` specifies that the program runs in interactive mode.
- Argument `[input_file]` specifies an input file that contains an initial board state. This way we can start the program from a non-empty board state. If the input file does not exist, the program should just create an empty board state and start again from there.
- Argument `[computer-next/human-next]` specifies whether the computer should make the next move or the human.
- Argument `[depth]` specifies the number of moves in advance that the computer should consider while searching for its next move. In other words, this argument specifies the depth of the search tree. Essentially, this argument will control the time takes for the computer to make a move.

After reading the input file, the program gets into the following loop:

1. If computer-next, goto 2, else goto 5.
2. Print the current board state and score. If the board is full, exit.
3. Choose and make the next move.
4. Save the current board state in a file called computer.txt (in same format as input file).
5. Print the current board state and score. If the board is full, exit.
6. Ask the human user to make a move (make sure that the move is valid, otherwise repeat request to the user). The user should specify a move by simply entering a column number, from 0 (for the leftmost column) to 6 (for the rightmost column).
7. Save the current board state in a file called human.txt (in same format as input file).
8. Goto 2.

**One-Move Mode:**<br/>
The purpose of the one-move mode is to make it easy for programs to compete against each other, and communicate their moves to each other using text files. The one-move mode is invoked as follows:
```
$ python maxconnect4.py one-move [input_file] [output_file] [depth]
```
For example:
`$ python maxconnect4.py one-move red_next.txt green_next.txt 5`<br/>
In this case, the program simply makes a single move and terminates. In particular, the program should:
1. Read the input file and initialize the board state and current score, as in interactive mode.
2. Print the current board state and score. If the board is full, exit.
3. Choose and make the next move.
4. Print the current board state and score.
5. Save the current board state to the output file IN EXACTLY THE SAME FORMAT THAT IS USED FOR INPUT FILES.
6. Exit