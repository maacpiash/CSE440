#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)
    currentGame.aiPlay() # Make a move
    print('Game state after move:')
    currentGame.printGameBoard()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame):
    while currentGame.pieceCount < 42:
        if currentGame.currentTurn == 1:
            human = int(input("Enter number of column (1-7, inclusive): "))
            if not 0 < human < 8:
                print("Sorry, invalid column number. Input must be between 1 and 7 inclusive.")
                continue
            placement = currentGame.playPiece(human - 1)
            if not placement:
                print("Sorry, this column is full. Please try another column between 1 and 7 inclusive.")
                continue
            try:
                currentGame.gameFile = open("human.txt", 'w')
            except IOError:
                currentGame.gameFile = open("human.txt", 'w+')
                print("New file 'human.txt' was created.")
            except:
                sys.exit("Error opening 'human.txt' file")
        else:
            currentGame.aiPlay()
            try:
                currentGame.gameFile = open("computer.txt", 'w')
            except IOError:
                currentGame.gameFile = open("computer.txt", 'w+')
                print("New file 'computer.txt' was created.")
            except:
                sys.exit("Error opening 'computer.txt' file")
        
        print('\n\nMove no. %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, human + 1))
        currentGame.currentTurn = (currentGame.currentTurn % 2) + 1
        print("Game state after move: ")
        currentGame.countScore()
        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        currentGame.printGameBoardToFile()
    currentGame.gameFile.close()




def main(argv):
    # Make sure we have enough command-line arguments
    print("Arglen = " + str(len(argv)))
    if len(argv) < 5 or len(argv) > 6:
        print('Four or five command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    if len(argv) == 5:
        depth = argv[4]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.maxDepth = depth
    currentGame.gameFile.close()

    print('\nMaxConnect-4 game\n')
    print('Game state before move:')
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        interactiveGame(currentGame) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)



