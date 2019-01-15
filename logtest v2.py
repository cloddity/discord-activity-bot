import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from datetime import datetime, date, time

Client = discord.Client()
client = commands.Bot(command_prefix = "^")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content == "^ping":
        await client.send_message(message.channel, "Pong!")

###########################################################

@client.event
async def on_message(message):
    def get_channel(channels, channel_name):
        count = 0
        for channel in client.get_all_channels():
            if channel.name == channel_name:
                if count == 0:
                    return channel
        count += 1
        return message.channel
    #-------------------------
    arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

    general_channel = get_channel(client.get_all_channels(), 'bot-test')
    gambling = get_channel(client.get_all_channels(), 'gambling')
    screencaps = get_channel(client.get_all_channels(), 'screencaps')
    vent = get_channel(client.get_all_channels(), 'gambling')
    
    if message.content.startswith('!stat'):
        array = message.content.split(" ")
        mesg = await client.send_message(general_channel, 'Calculating...')
        month = int(array[1])
        day = int(array[2])
        m = 9
        d = 1
        print(datetime.utcnow())
        while m <= 9:
            while d < (int(arr[1][m - 1]) + 1):
                ymdA = datetime(int(array[1]), m, d, 7, 59, 59)
                if d + 1 > int(arr[1][m - 1]):
                    ymdB = datetime(int(array[1]), m + 1, 1, 8, 0, 0)
                    print(ymdB)
                else:
                    ymdB = datetime(int(array[1]), m, d + 1, 8, 0, 0)
                    print(ymdB)
                counter = 0
                async for msg in client.logs_from(gambling, limit=10000, before=ymdB, after=ymdA):
                    if msg.author == message.author:
                        counter += 1
                print('{}/{} {}'.format(str(m), str(d), str(counter)))
                d += 1
            m += 1
            d = 1

        await client.edit_message(mesg, '{} has {} messages in #{}.'.format(message.author, str(counter), gambling))
        
        
client.run("NTE2NDc2MzAxMjcyNjc4NDI0.Dt0OSA.YyuxgPfNDMZ74krs7EllFp7AZsY")


