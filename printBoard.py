# prints the board
def printChessBoard(chessboard):
    currentRow = 9
    # iterates through each row
    boardOut = ""
    for row in chessboard:
        # prints seperator
        currentRow = currentRow - 1
        boardOut += "```———————————————————————————————————————————————————\n"
        # prints out the row number, the actual row, separated by a space and a pipe
        if currentRow % 2 == 0:
            boardOut += f"{currentRow} ⎟  {row[0]}  ⎟[|{row[1]}|]⎟  {row[2]}  ⎟[|{row[3]}|]⎟  {row[4]}  ⎟[|{row[5]}|]⎟  {row[6]}  ⎟[|{row[7]}|]⎟\n"
        else:
            boardOut += f"{currentRow} ⎟[|{row[0]}|]⎟  {row[1]}  ⎟[|{row[2]}|]⎟  {row[3]}  ⎟[|{row[4]}|]⎟  {row[5]}  ⎟[|{row[6]}|]⎟  {row[7]}  ⎟\n"

    # bottom of the chessboard, with column names
    boardOut += "———————————————————————————————————————————————————\n"
    boardOut += "  |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |```"
    return boardOut