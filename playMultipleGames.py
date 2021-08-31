from GameBoard import *
from minimaxAI import TTTMinimaxAI
from reinforcementLearningAI import TTTReinforcementLearningAI



gameBoard = tttGameBoard(3)

mmAI_X = TTTMinimaxAI("x", 3)
mmAI_O = TTTMinimaxAI("o", 3)
rlAI_X = TTTReinforcementLearningAI("x", 3)
rlAI_O = TTTReinforcementLearningAI("o", 3)


# use these variables to declare which engine is running which player
# just comment / uncomment them as needed

#enginePlayerX = "MM AI"
enginePlayerX = "RL AI"

#enginePlayerO = "MM AI"
enginePlayerO = "RL AI"


numIterations = 100
playerWinsX = 0
playerWinsO = 0
drawWins = 0
totalMoves = 0

for iteration in range(0, numIterations):
    
    gameOver = False
    currentPlayer = "o" # X plays first, so we initialize it to O

    while(not gameOver):

        # switches the current player
        if(currentPlayer == "o"):
            currentPlayer = "x"
        elif(currentPlayer == "x"):
            currentPlayer = "o"


        if(currentPlayer == "x"):

            if(enginePlayerX == "MM AI"):
                getResult = mmAI_X.getBestMove(currentPlayer, gameBoard.getBoardState(), gameBoard.getMoveNumber())
                playerMove = [getResult[0], getResult[1]]
            elif(enginePlayerX == "RL AI"):
                playerMove = rlAI_X.getBestMove(currentPlayer, gameBoard.getBoardState())

        else:

            if(enginePlayerO == "MM AI"):
                getResult = mmAI_O.getBestMove(currentPlayer, gameBoard.getBoardState(), gameBoard.getMoveNumber())
                playerMove = [getResult[0], getResult[1]]
            elif(enginePlayerO == "RL AI"):
                playerMove = rlAI_O.getBestMove(currentPlayer, gameBoard.getBoardState())

            

        # makes the move
        gameBoard.playMove(currentPlayer, playerMove[0], playerMove[1])



        # checks if there's a winner
        if(gameBoard.checkForWin()):
            gameOver = True
            totalMoves += gameBoard.getMoveNumber()
            if(currentPlayer == "x"):
                playerWinsX += 1
            else:
                playerWinsO += 1
            gameBoard.startNewGame()
            print("Game", iteration, "Complete")

        elif(gameBoard.checkForDraw()):
            gameOver = True
            totalMoves += gameBoard.getMoveNumber()
            drawWins += 1
            gameBoard.startNewGame()
            print("Game", iteration, "Complete")

print("---")
print("Games Complete,", totalMoves, "Moves Total")
print(enginePlayerX, "wins as x:", playerWinsX)
print(enginePlayerO, "wins as o:", playerWinsO)
print("Number of draws:", drawWins)
