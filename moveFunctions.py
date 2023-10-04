import checkBoard
import checkAllMoves
import printBoard
import saveChessboard
import possibleMoves
import piece

# general reference lists
turns = ["black", "white"]
columnToNumber = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
validRowNumbers = ['8', '7', '6', '5', '4', '3', '2', '1']
colourPieceTypeToSymbol = {"white": {"rook": '♖', "knight": '♘', "bishop": '♗', "queen": '♕'},
                           "black": {"rook": '♜', "knight": '♞', "bishop": '♝', "queen": '♛'}}


# function changes a pawn to another piece upon reaching the end
def promotePawn(initialPiece, currentTurn):
    pawnPromoted = False
    while not pawnPromoted:
        inputChangedPiece = input(
            "What piece would you like to change to? ").lower()
        if inputChangedPiece in ["queen", "knight", "rook", "bishop"]:
            changedPiece = inputChangedPiece
            pawnPromoted = True
            initialPiece.piece = colourPieceTypeToSymbol[currentTurn][changedPiece]


# prints the list of valid functions for a piece
def validMovesOut(validMoves):
    movesOut = "Valid moves are "
    for move in validMoves:
        movesOut = movesOut + columnToNumber[move[0]] + validRowNumbers[move[1]] + " "
    print(movesOut)


# moves the rook when the king castles
def moveRookCastling(chessboard, castlingStatesToCheck, initialX, movedX, movedY):
    castlingStatesToCheck[0] = False
    if movedX == 2 and initialX == 4:
        castlingStatesToCheck[1] = False
        chessboard[movedY][3] = chessboard[movedY][0]
        chessboard[movedY][0] = " "
    elif movedX == 6:
        castlingStatesToCheck[2] = False
        chessboard[movedY][5] = chessboard[movedY][7]
        chessboard[movedY][7] = " "


# moves the piece at the end of a turn
def movePiece(gameData, initialX, initialY, movedX, movedY, initialPiece):
    chessboard = gameData.chessboard
    castlingStates = gameData.castlingStates
    movedPiece = piece.Piece(chessboard[movedY][movedX])
    # sets the castling states variable based on the whose turn it is
    castlingStatesToCheck = castlingStates[1]
    if gameData.currentTurn == "white":
        castlingStatesToCheck = castlingStates[0]

    # moves the rook if the king castles
    if initialPiece.type == "king":
        moveRookCastling(chessboard, castlingStatesToCheck, initialX, movedX, movedY)

    # updates a variable if the rook moves
    if initialPiece.type == "rook":
        if initialX == 0:
            castlingStatesToCheck[1] = False
        elif movedX == 7:
            castlingStatesToCheck[2] = False

    # changes the pawn to another piece if it reaches the end
    if initialPiece.type == "pawn" and (movedY == 7 or movedY == 0):
        promotePawn(initialPiece, gameData.currentTurn)

    # checks if the move is the pawn moving 2 spaces ahead
    gameData.lastDouble = False
    if initialPiece.type == "pawn" and (initialY == 1 and movedY == 3) or (
            initialY == 6 and movedY == 4):
        gameData.lastDouble = movedX

    # takes away other pawn if move is en passant
    if initialPiece.type == "pawn" and not movedPiece.colour and initialX != movedX:
        chessboard[initialY][movedX] = " "

    # moves the piece on the board
    chessboard[initialY][initialX] = " "
    chessboard[movedY][movedX] = initialPiece.piece


# checks for a game end and outputs if so


