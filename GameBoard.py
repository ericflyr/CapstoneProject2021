class tttGameBoard:

    # initializes a gameboard
    def __init__(self, boardSize):

        self.board = self.createBoard(boardSize) # always use 3. checkWin doesn't work for other sizes
        self.moveCount = 0
        self.boardSize = boardSize

    # creates a new, empty board
    def createBoard(self, boardSize):
        newBoard = []

        for _ in range(0, boardSize):
            rowList = []
            for _ in range(0, boardSize):
                rowList.append("-")
            newBoard.append(rowList)

        return newBoard

    # clears the board and starts a new game
    def startNewGame(self):
        
        for row in range(0, self.boardSize):
            for col in range(0, self.boardSize):
                self.board[row][col] = "-"

        self.moveCount = 0

    # prints the board to the screen
    def printBoard(self):
        # print("move", self.moveCount)
        for row in self.board:
            for col in row:
                print(col, end = " ")
            print()

    # returns the current board-state
    def getBoardState(self):
        newBoard = self.createBoard(self.boardSize)

        # copies board values over
        for row in range(0, self.boardSize):
            for col in range(0, self.boardSize):
                newBoard[row][col] = self.board[row][col]

        return newBoard

    # returns the move number the game is on
    def getMoveNumber(self):
        return self.moveCount

    # returns the board size
    def getBoardSize(self):
        return self.boardSize

    # player plays a move
    def playMove(self, player, row, col):

        self.moveCount += 1

        # check if player char is 'x' or 'o'
        if(player != "x" and player != "o"):
            raise Exception("Non-valid player character, move", self.moveCount)

        # check if row / col are in bounds
        if(row >= self.boardSize or col >= self.boardSize):
            raise Exception("move out of bounds, move", self.moveCount)

        # check if spot is empty
        if(self.board[row][col] != "-"):
            raise Exception("move already played, move", self.moveCount)

        # plays the move
        self.board[row][col] = player

    # checks if move is available
    def checkIfMoveAvailable(self, row, col):
        if(self.board[row][col] != "-"):
            return False
        return True

    # checks if no available moves are left
    def checkForDraw(self):
        if(self.moveCount == self.boardSize ** 2):
            return True
        return False

    # check if win. only works for 3x3 boards
    def checkForWin(self):


        # check rows
        for row in range(0, self.boardSize):
            if(self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] != "-"):
                return True

        #check cols
        for col in range(0, self.boardSize):
            if(self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != "-"):
                return True

        #check diagonals
        # TL -> BR
        if(self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "-"):
                return True

        # TR -> BL
        if(self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "-"):
                return True
        
        return False
