
import discord

def gameStart(thread):


    # loop for a turn being processed, till game ends
    while gameRunning:
        gameRunning = makeMove.makeMove(gameData)
