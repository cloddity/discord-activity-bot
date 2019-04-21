import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from datetime import datetime, date, time
import os

Client = discord.Client()
client = commands.Bot(command_prefix="^")


@client.event
async def on_ready():
    print("Bot is ready!")


###########################################################

@client.event
async def on_message(message):
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    show = ""
    blank = ":white_small_square:"
    os = ":o:"
    xs = ":x:"
    turncount = 1

    def move(num, turn):
        if turn > 0:
            board[num - 1] = 1
        elif turn < 0:
            board[num - 1] = 2

    def display():
        show = ""
        newline = 0
        for x in board:
            if x == 0:
                show += blank
            if x == 1:
                show += os
            if x == 2:
                show += xs
            if newline == 2:
                show += "\n"
                newline = -1
            newline += 1
        return show

    def invalid(num):
        if (board[num - 1] > 0):
            return True
        else:
            return False

    def representsInt(s):
        try:
            int(s)
            return False
        except ValueError:
            return True

    if message.content.startswith("^redefine"):
        temp = message.content.split(" ", 2)
        if ((temp[1] == "O" or temp[1] == "o") and temp[2].startswith(":")):
            os = temp[2]
            await client.send_message(message.channel, ":thumbsup:")
        elif ((temp[1] == "X" or temp[1] == "x") and temp[2].startswith(":")):
            xs = temp[2]
            await client.send_message(message.channel, ":thumbsup:")

    if message.content.startswith("^play"):
        main = message.author
        turn = 1
        if (message.mentions.__len__() > 0):
            for user in message.mentions:
                opponent = user
                await client.send_message(message.channel,
                                          opponent.mention + " " + main.nick + " wishes to challenge you! Do you accept?\n`(Y/N)`")
                response = await client.wait_for_message(author=opponent, timeout=60)
                while (response.content != "Y" and response.content != "y" and response.content != "N" and response.content != "n"):
                    response = await client.wait_for_message(author=opponent, timeout=60)
                if response.content == ("n") or response.content == ("N"):
                    await client.send_message(message.channel, "Game declined.")
                elif response.content == ("y") or response.content == ("Y"):
                    await client.send_message(message.channel, "Use 1-9 to place Os/Xs.")
                    show = display()
                    await client.send_message(message.channel, show)
                response = await client.wait_for_message()
                while ((response.author != main and response.author != opponent) or representsInt(response.content) or (
                        int(response.content) < 1 or int(response.content) > 9)):
                    response = await client.wait_for_message()
                if (response.author == main):
                    playera = main
                    playerb = opponent
                else:
                    playera = opponent
                    playerb = main
                move(int(response.content), turn)
                turn *= -1
                show = display()
                await client.send_message(message.channel, show)
                while (turncount < 9):
                    response = await client.wait_for_message()
                    if (turn == 1):
                        while ((response.author != playera) or representsInt(response.content) or (
                                int(response.content) < 1 or int(response.content) > 9) or invalid(
                                int(response.content))):
                            response = await client.wait_for_message()
                    elif (turn == -1):
                        while ((response.author != playerb) or representsInt(response.content) or (
                                int(response.content) < 1 or int(response.content) > 9) or invalid(
                                int(response.content))):
                            response = await client.wait_for_message()
                    move(int(response.content), turn)
                    turn *= -1
                    show = display()
                    await client.send_message(message.channel, show)
                    turncount += 1
                    if (board[0] == board[1] == board[2] != 0 or board[3] == board[4] == board[5] != 0 or board[6] ==
                            board[7] == board[8] != 0 or board[0] == board[3] == board[6] != 0 or board[1] == board[
                                4] == board[7] != 0 or board[2] == board[5] == board[8] != 0 or board[0] == board[4] ==
                            board[8] != 0 or board[2] == board[4] == board[6] != 0):
                        await client.send_message(message.channel, "**" + response.author.nick + " wins!**")
                        break
                if (turncount == 9):
                    await client.send_message(message.channel, "**Draw!**")

        # temp = message.content.split(" ", 1)
        # await client.send_message(message.channel, temp[1].id)
        # await client.send_message(message.channel, message.author.nick)

    if message.content.startswith("^engrish") or message.content.startswith("^er"):
        temp = message.content.split(" ", 1)
        del temp[0]
        s = ''.join(temp)
        array = list(s)
        count = 0
        for x in array:
            if x == "l":
                array[count] = "r"
            elif x == "r":
                array[count] = "l"
            elif x == "L":
                array[count] = "R"
            elif x == "R":
                array[count] = "L"
            elif x == "x":
                array[count] = "cksu"
            count += 1
        string = ''.join(array)
        await client.send_message(message.channel, string)
    if message.content == "^triangle":
        await client.send_message(message.channel, "▲")
        # -------------------------

    def get_channel(channels, channel_name):
        count = 0
        for channel in client.get_all_channels():
            if channel.name == channel_name:
                if count == 0:
                    return channel
        count += 1
        return message.channel

    # -------------------------
    arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

    general_channel = get_channel(client.get_all_channels(), 'bot-test')
    gambling = get_channel(client.get_all_channels(), 'gambling')
    screencaps = get_channel(client.get_all_channels(), 'screencaps')

    if message.content.startswith('^stats'):
        array = message.content.split(" ")
        # mesg = await client.send_message(general_channel, 'Calculating...')
        m = 10
        d = 1
        y = 2016
        if m >= 3 and m < 11:  # DST on
            aH = 6
            bH = 7
        else:  # DST off
            aH = 7
            bH = 8
        flagS = False
        flagE = False
        flag = False
        print(datetime.utcnow())
        while m <= (12):
            while d <= int(arr[1][m - 1]):
                # while d < (3):
                ymdA = datetime(y, m, d, aH, 59, 59)
                if flagS == True:
                    aH -= 1
                    flagS = False
                if m == 3 and d >= 8 and d <= 14 and ymdA.isoweekday() == 7:
                    bH -= 1
                    flagS = True
                    print('on')
                if flagE == True:
                    aH += 1
                    flagE = False
                if m == 11 and d >= 1 and d <= 7 and ymdA.isoweekday() == 7:
                    bH += 1
                    flagE = True
                    print('off')
                # print(ymdA)
                if m == 12 and d == 31:
                    if y == 2018:
                        m = 13
                        ymdB = datetime(2019, 1, 1, bH, 0, 0)
                    else:
                        ymdB = datetime(y + 1, 1, 1, bH, 0, 0)
                elif d + 1 > int(arr[1][m - 1]):
                    ymdB = datetime(y, m + 1, 1, bH, 0, 0)
                    # print(ymdB)
                else:
                    ymdB = datetime(y, m, d + 1, bH, 0, 0)
                    # print(ymdB)
                counter = 0
                async for msg in client.logs_from(gambling, limit=30686, before=ymdB, after=ymdA, reverse=True):
                    # if msg.author.id == "172002275412279296": #tatsu
                    # if msg.author.id == "206881350513459210": #clod
                    counter += 1

                print('{}/{}/{} {}'.format(str(m), str(d), str(y - 2000), str(counter)))
                if m == 12 and d == 31 and y != 2018:
                    m = 0
                    flag = True
                d += 1
            m += 1
            d = 1
            if flag == True:
                y += 1
                flag = False
        # await client.edit_message(mesg, '{} has {} messages in #{}.'.format(message.author, str(counter), gambling))

client.run(os.environ.get("TOKEN"))