from GameBoard import *
from minimaxAI import TTTMinimaxAI
from reinforcementLearningAI import TTTReinforcementLearningAI


# gets human input and returns a "players move"
def getHumanInput():
    
    # gets input from human player
    print("Player", currentPlayer, end = ", ")
    playerInput = input("where do you want to play? (x, y): ").split()

    # check for correct input (2 arguments, numbers, inbounds, move is available)
    inputCorrect = False
    while(inputCorrect == False):

        if(len(playerInput) != 2):
            print("Please only send 2 arguments")
            print("Player", currentPlayer, end = ", ")
            playerInput = input("where do you want to play? (x, y): ").split()
        elif(playerInput[0].isdigit() == False or playerInput[1].isdigit() == False):
            print("Please only input numbers")
            print("Player", currentPlayer, end = ", ")
            playerInput = input("where do you want to play? (x, y): ").split()
        elif(int(playerInput[0]) < 0 or int(playerInput[0]) >= gameBoard.getBoardSize()):
            print("Input out of bounds")
            print("Player", currentPlayer, end = ", ")
            playerInput = input("where do you want to play? (x, y): ").split()
        elif(int(playerInput[1]) < 0 or int(playerInput[1]) >= gameBoard.getBoardSize()):
            print("Input out of bounds")
            print("Player", currentPlayer, end = ", ")
            playerInput = input("where do you want to play? (x, y): ").split()
        elif(gameBoard.checkIfMoveAvailable(int(playerInput[0]), int(playerInput[1])) != True):
            print("Move not available.")
            print("Player", currentPlayer, end = ", ")
            playerInput = input("where do you want to play? (x, y): ").split()
        else:
            inputCorrect = True
    
    return [int(playerInput[0]), int(playerInput[1])]

gameBoard = tttGameBoard(3)

mmAI_X = TTTMinimaxAI("x", 3)
mmAI_O = TTTMinimaxAI("o", 3)
rlAI_X = TTTReinforcementLearningAI("x", 3)
rlAI_O = TTTReinforcementLearningAI("o", 3)



# use these variables to declare which engine is running which player
# just comment / uncomment them as needed

#enginePlayerX = "Human"
enginePlayerX = "MM AI"
#enginePlayerX = "RL AI"

#enginePlayerO = "Human"
#enginePlayerO = "MM AI"
enginePlayerO = "RL AI"


keepPlaying = True
while keepPlaying:
    
    gameOver = False
    currentPlayer = "o" # X plays first, so we initialize it to O

    while(not gameOver):

        # switches the current player
        if(currentPlayer == "o"):
            currentPlayer = "x"
        elif(currentPlayer == "x"):
            currentPlayer = "o"


        if(currentPlayer == "x"):

            # checks for which AI / human to use
            if(enginePlayerX == "MM AI"):
                getResult = mmAI_X.getBestMove(currentPlayer, gameBoard.getBoardState(), gameBoard.getMoveNumber())
                playerMove = [getResult[0], getResult[1]]
            elif(enginePlayerX == "RL AI"):
                playerMove = rlAI_X.getBestMove(currentPlayer, gameBoard.getBoardState())
            else: # human
                playerMove = getHumanInput()
        else:

            if(enginePlayerO == "MM AI"):
                getResult = mmAI_O.getBestMove(currentPlayer, gameBoard.getBoardState(), gameBoard.getMoveNumber())
                playerMove = [getResult[0], getResult[1]]
            elif(enginePlayerO == "RL AI"):
                playerMove = rlAI_O.getBestMove(currentPlayer, gameBoard.getBoardState())
            else: # human
                playerMove = getHumanInput()
            



        # makes the move
        gameBoard.playMove(currentPlayer, playerMove[0], playerMove[1])

        if(currentPlayer == "x"):
            print("Move", gameBoard.getMoveNumber(), "-", enginePlayerX, currentPlayer, "plays", playerMove)
        else:
            print("Move", gameBoard.getMoveNumber(), "-", enginePlayerO, currentPlayer, "plays", playerMove)

        gameBoard.printBoard()

        # checks if there's a winner
        if(gameBoard.checkForWin()):
            gameOver = True
            print("Player", currentPlayer, "has won the game!")
        elif(gameBoard.checkForDraw()):
            gameOver = True
            print("Draw!")



    playerInput = input("Play again? (y/n): ")

    # checks if input is valid
    while(playerInput.lower() != 'y' and playerInput.lower() != 'n'):
        print("input not recognized.")
        playerInput = input("Play again? (y/n): ")

    if(playerInput.lower() == "y"):
        keepPlaying = True
        gameBoard.startNewGame()
    elif(playerInput.lower() == "n"):
        keepPlaying = False

    
