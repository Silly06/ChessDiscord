import asyncio
import os
import gameData
import images
import checkBoard
import checkAllMoves
import saveChessboard
import possibleMoves
import piece
import moveFunctions
import json

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message.content)
    rawSaveData = open("savedChessGame.json")
    saveData = json.load(rawSaveData)
    if message.content.startswith("sc start") and len(message.mentions) == 1 \
            and message.channel.id == 1090209014496899102:
        await message.channel.send('creating new game...')
        threadName = message.author.name + "'s and "+ message.mentions[0].name + "'s chess game"
        thread = await message.create_thread(name=threadName, auto_archive_duration=10080)
        await thread.send(f"<@{message.mentions[0].id}> Would you like to play white or black?")
        def playerPickedColour(m):
            return (m.content == 'white' or m.content == 'black') \
                   and m.channel == thread and m.author.id == message.mentions[0].id
        try:
            challengedColour = await client.wait_for('message', check=playerPickedColour, timeout=60.0)
            users = [message.author.id, message.mentions[0].id]
            if challengedColour.content == "white":
                users = [message.mentions[0].id, message.author.id]
            game = gameData.GameData([
                ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
                ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
                ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
            ], "white", [[True, True, True], [True, True, True]], False, users)
            saveChessboard.saveChessBoard(game, thread.id)
            embed = discord.Embed(
                title=f"{game.currentTurn} to move",
                color=discord.Colour.blurple(),
                description="yes"
            )
            images.generateBoard(game, thread.id)
            file = discord.File(f"C:/Users/aidan/Documents/chess bot/imagesToSend/board{thread.id}.png", filename=f"board{thread.id}.png")
            embed.set_image(url=f"attachment://board{thread.id}.png")
            await thread.send(f"<@{game.users[0]}>", file=file, embed=embed)
        except asyncio.TimeoutError:
            await thread.delete()


    elif str(message.channel.id) in saveData:
        channelDataList = saveData[str(message.channel.id)]
        channelData = gameData.GameData(channelDataList[0], channelDataList[1], channelDataList[2], channelDataList[3], channelDataList[4], )
        if channelData.users[0] == message.author.id and len(message.content) == 5:
            chessboard = channelData.chessboard
            inCheck = checkBoard.checkState(chessboard, channelData.currentTurn)

            if message.content[0] in moveFunctions.columnToNumber and message.content[1] in moveFunctions.validRowNumbers\
                    and message.content[2] == " " \
                    and message.content[3] in moveFunctions.columnToNumber and message.content[4] in moveFunctions.validRowNumbers:
                initialX = int(moveFunctions.columnToNumber.index(message.content[0]))
                initialY = abs(int(message.content[1]) - 8)
                validMoves = possibleMoves.findMoves(channelData, initialX, initialY, inCheck)
                initialPiece = piece.Piece(chessboard[initialY][initialX])
                if initialPiece.colour == channelData.currentTurn and len(validMoves) != 0:
                    # outputs a list of valid moves if there are any
                    moveFunctions.validMovesOut(validMoves)
                    inputMovedPosition = message.content[3] + message.content[4]
                    movedX = int(moveFunctions.columnToNumber.index(inputMovedPosition[0]))
                    movedY = abs(int(inputMovedPosition[1]) - 8)
                    if [movedX, movedY] in validMoves:
                        moveFunctions.movePiece(channelData, initialX, initialY, movedX, movedY,
                                                initialPiece)
                        channelData.currentTurn = moveFunctions.turns[
                            abs(moveFunctions.turns.index(channelData.currentTurn) - 1)]
                        channelData.users.reverse()
                        saveChessboard.saveChessBoard(channelData, message.channel.id)


                        noMoves = checkAllMoves.checkNoMoves(channelData, inCheck)
                        inCheck = checkBoard.checkState(chessboard, channelData.currentTurn)

                        title = ""
                        ping = f"<@{channelData.users[0]}>"
                        if inCheck and noMoves:
                            title = f"Checkmate! Winner is <@{str(channelData.users[abs(moveFunctions.turns.index(channelData.currentTurn) - 1)])}>!"
                            saveChessboard.deleteGame(str(message.channel.id))
                            ping = ""
                        elif noMoves:
                            title = "Game is a tie!"
                            saveChessboard.deleteGame(str(message.channel.id))
                            ping = ""
                        else:
                            title = f"{channelData.currentTurn} to move"
                        embed = discord.Embed(
                            title=title,
                            color=discord.Colour.blurple(),
                        )
                        images.generateBoard(channelData, message.channel.id)
                        file = discord.File(f"C:/Users/aidan/Documents/chess bot/imagesToSend/board{message.channel.id}.png",
                                            filename=f"board{message.channel.id}.png")
                        embed.set_image(url=f"attachment://board{message.channel.id}.png")
                        await message.channel.send(ping, file=file, embed=embed)
                    else:
                        await message.channel.send("That's not one of the valid moves")
                else:
                    await message.channel.send("That's not a piece your can move!")


@client.event
async def on_thread_remove(thread):
    saveChessboard.deleteGame(str(thread.id))

@client.event
async def on_thread_delete(thread):
    saveChessboard.deleteGame(str(thread.id))



client.run(TOKEN)
