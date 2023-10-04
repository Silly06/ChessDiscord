import gameData
from PIL import Image


def generateBoard(channelData, threadID):
    board = Image.open("assets/boardImageWhite.png")
    whitePawn = Image.open("assets/whitePawn.png")
    whiteRook = Image.open("assets/whiteRook.png")
    whiteBishop = Image.open("assets/whiteBishop.png")
    whiteQueen = Image.open("assets/whiteQueen.png")
    whiteKing = Image.open("assets/whiteKing.png")
    whiteKnight = Image.open("assets/whiteKnight.png")
    blackPawn = Image.open("assets/blackPawn.png")
    blackRook = Image.open("assets/blackRook.png")
    blackBishop = Image.open("assets/blackBishop.png")
    blackQueen = Image.open("assets/blackQueen.png")
    blackKing = Image.open("assets/blackKing.png")
    blackKnight = Image.open("assets/blackKnight.png")
    pieces = {'♜': blackRook, '♞': blackKnight, '♝':blackBishop, '♛':blackQueen, '♚':blackKing, '♟':blackPawn,
              '♖':whiteRook, '♘':whiteKnight, '♗':whiteBishop, '♕':whiteQueen, '♔':whiteKing, '♙':whitePawn}
    boardData = channelData.chessboard
    if channelData.currentTurn == "black":
        boardData.reverse()
        for row in boardData:
            row.reverse()
            board = Image.open("assets/boardImageBlack.png")

    for x in range(8):
        for y in range(8):
            pieceData = boardData[y][x]
            if pieceData != " ":
                pieceToPaste = pieces[pieceData]
                box = (x * 240 + 70, y * 240 + 28)
                board.paste(pieceToPaste, box, pieceToPaste)


    board.save(f"imagesToSend/board{threadID}.png", )
