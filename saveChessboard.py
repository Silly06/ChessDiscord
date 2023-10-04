import json
import os

# function takes the game data and saves it in a JSON file
def saveChessBoard(gameData, threadID):
    listToExport = [gameData.chessboard, gameData.currentTurn, gameData.castlingStates, gameData.lastDouble, gameData.users]
    rawSaveData = open("savedChessGame.json")
    saveData = json.load(rawSaveData)
    print(type(saveData))
    saveData.update({str(threadID):listToExport})
    jsonSave = json.dumps(saveData, indent=4)
    # Writing to savedChessGame.json
    with open("savedChessGame.json", "w") as outfile:
        outfile.write(jsonSave)


def deleteGame(threadID):
    rawSaveData = open("savedChessGame.json")
    saveData = json.load(rawSaveData)
    if threadID in saveData:
        saveData.pop(str(threadID))
    jsonSave = json.dumps(saveData, indent=4)
    with open("savedChessGame.json", "w") as outfile:
        outfile.write(jsonSave)
    if os.path.exists(f"imagesToSend/board{threadID}.png"):
        os.remove(f"imagesToSend/board{threadID}.png")
