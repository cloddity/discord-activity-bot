import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from datetime import datetime, date, time

Client = discord.Client()
client = commands.Bot(command_prefix = "^")

chat_filter = ["PINEAPPLE", "APPLE", "CHROME"]
bypass_list = []

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content == "ping":
        await client.send_message(message.channel, "Pong!")

#message detection: ping, say
@client.event
async def on_message(message):
    if message.content.upper().startswith('^PING'):
        userID = message.author.id
        await client.send_message(message.channel, "<@%s> Pong!" % (userID))
    if message.content.upper().startswith('^SAY'):
        if message.author.id == "206881350513459210":
            args = message.content.split(" ")
            await client.send_message(message.channel, "%s" % (" ".join(args[1:])))
        else:
            await client.send_message(message.channel, "You do not have suffient permissions.")
    if message.content.upper().startswith('^ADMIN'):
        if "516476301272678424" in [role.id for role in message.author.roles]:
            await client.send_message(message.channel, "You are an admin.")
        else:
            await client.send_message(message.channel, "You are not an admin.")
    contents = message.content.split(" ") #contents is a list type
    for word in contents:
        if word.upper() in chat_filter:
            if not message.author.id in bypass_list:
                try:
                    await client.delete_message(message)
                    await client.send_message(message.channel, "**Hey!** You're not allowed to use that word here.")
                except discord.errors.NotFound:
                    return

@client.event
async def on_message(message):
    def get_channel(channels, channel_name):
        count = 0
        for channel in client.get_all_channels():
            #print(channel)
            if channel.name == channel_name:
                if count == 0:
                    return channel
        count += 1
        return message.channel

    general_channel = get_channel(client.get_all_channels(), 'bot-test')
    gambling = get_channel(client.get_all_channels(), 'gambling')
    screencaps = get_channel(client.get_all_channels(), 'screencaps')
    vent = get_channel(client.get_all_channels(), 'gambling')
    #await client.send_message(general_channel, 'test msg')
    ###
    #for server in client.servers:
        #for channel in server.channels:
            #await client.send_message(message.channel, channel)
    #listChannels = Client.get_all_channels()
    #await client.send_message(message.channel, listChannels)
    
    if message.content.startswith('!stat'):
        array = message.content.split(" ")
        #ymd = datetime(int(array[1]), int(array[2]), int(array[3]))
        ymdA = datetime(int(array[1]), int(array[2]), int(array[3]), 7, 59, 59)
        ymdB = datetime(int(array[1]), int(array[2]), int(array[3]) + 1, 8, 0, 0)
        mesg = await client.send_message(general_channel, 'Calculating...')
        counter = 0
        async for msg in client.logs_from(gambling, limit=10000, before=ymdB, after=ymdA):
            if msg.author == message.author:
                counter += 1
        #async for msg in client.logs_from(516507986147934215, limit=100, before=ymdB, after=ymdA):
            #if msg.author == message.author:
                #counter += 1
        await client.edit_message(mesg, '{} has {} messages in #{}.'.format(message.author, str(counter), gambling))
        print(str(counter))
        
client.run("NTE2NDc2MzAxMjcyNjc4NDI0.Dt0OSA.YyuxgPfNDMZ74krs7EllFp7AZsY")

#args[0] = !SAY
#args[1] = a
#args[2] = b
#args[1:] = a b
