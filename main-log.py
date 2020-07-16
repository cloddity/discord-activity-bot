import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time as t
from datetime import datetime, date, time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import timeit

Client = discord.Client()
client = commands.Bot(command_prefix = "^")

@client.event
async def on_ready():
    print("Bot is ready!")
    data = open('data.txt', 'w')
    print("0", file = data)
    data.close()

###########################################################
# available commands: add, ask, data, engrish*, triangle*, play*, help, count, stop, file*
# v1B: case sensitivity + search by weekday

@client.event
async def on_message(message):
    if message.content.startswith("^add"):
        arr = message.content.split(" ")
        array = arr[1].split("+")
        sum = int(array[0]) + int(array[1])
        await client.send_message(message.channel, str(sum))
    if message.content.startswith("^ask"):
        num = random.randint(1,4)
        if num == 1:
            await client.send_message(message.channel, 'No.')
        elif num == 2:
            await client.send_message(message.channel, 'Yes.')
        elif num == 3:
            await client.send_message(message.channel, 'Likely.')
        else:
            await client.send_message(message.channel, 'Impossible.')
    if message.content == "^check":
        await client.send_message(message.channel, "`[start_date]` and `[end_date]` - format: mm/dd/yy or mm-dd-yy\n`[user_id]` - right click user and click 'Copy ID' to obtain ID\n`[keyword]` - search term\n`[t_zone]` - integer between 0 and 23 (0 = PST, 3 = EST, etc.)\n`[-c]` - enable case sensitivity for keyword\n`[-w#]` - filter searches for a weekday (-w1 = Monday, -w7 = Sunday, etc.)\n(Order can be arbitrary for optional tags. By default, `^count` clears the spreadsheet. To append, use `^countc` instead.)")
    if message.content.startswith("^data"):
        await client.send_file(message.channel, r"data.txt",filename="data.txt")
    if message.content == "^info":
        await client.send_message(message.channel, "format: `^count` `[start_date]` `[end_date]` `[channel_name]`\noptional tags: `[user_id]` `[keyword]` `[t_zone]` `[-c]` `[-w#]`\n(Refer to `^check` for additional info.)")
    if message.content == "^stop":
        data = open('data.txt', 'w')
        print('stop')
        print("2", file = data)
        data.close()
    #-------------------------
    def get_channel(channels, channel_name):
        count = 0
        for channel in client.get_all_channels():
            if channel.name == channel_name:
                if count == 0:
                    return channel
        count += 1
        return message.channel
    #-------------------------
    def truncate(f, n):
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])
    #-------------------------
    def count(array, bool1, bool2, bool3, word, counter, user_id, msg): 
        #if msg.author.id == "206881350513459210": #clod
        if bool1 and bool2:
            if str(msg.author.id) == str(user_id) and (msg.content.lower().find(word.lower()) >= 0):
                if not bool3 or (bool3 and msg.content.find(word) >= 0):
                    counter += 1
        elif bool1:
            # print(str(msg.author.id) + " " + str(user_id))
            # t.sleep(0.5)
            if str(msg.author.id) == str(user_id):
                counter += 1
        elif bool2:
            if msg.content.lower().find(word.lower()) >= 0:
                if not bool3 or (bool3 and msg.content.find(word) >= 0):
                    counter += 1
        else:
            counter += 1
        return counter
    #-------------------------
    def f_read(file, num):
        rline = file.readline()
        # print("data: " + str(rline))
        if str(rline) == str(num) + "\n":
            print('lock')
            data.close()
            return False
        return True
    #-------------------------
    if message.content.startswith('^count'):
        #-------------------------
        start = timeit.default_timer()
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('Discord Sheets-cdfb5f771348.json', scope)
        gc = gspread.authorize(credentials)
        end = timeit.default_timer()
        # print("time: " + str(end - start))

        spr = gc.open_by_url('https://docs.google.com/spreadsheets/d/1UY3xoQo1zf2T_s91yaFYtkYm8ODeuoY_RiWlZ_-8vWc/edit?usp=sharing')
        wks = spr.worksheet('Main')
        #-------------------------
        arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

        bot_test = get_channel(client.get_all_channels(), 'bot-test')
        gambling = get_channel(client.get_all_channels(), 'general')
        screencaps = get_channel(client.get_all_channels(), 'screencaps')

        general = get_channel(client.get_all_channels(), 'general')
        offtopic = get_channel(client.get_all_channels(), 'offtopic')
        owners_only = get_channel(client.get_all_channels(), 'owners_only')
        serverwide_games = get_channel(client.get_all_channels(), 'serverwide_games')
        #-------------------------
        start = timeit.default_timer()
        print(datetime.utcnow()) #
        flag_error = True
        flag_id = False
        flag_word = False
        flag_case = False
        flag = True
        flag_api = False
        flag_ast = False
        flag_proc = True
        flag_wait = False
        flag_errcode = False
        #--------------------------
        try:
            array = message.content.split(" ", 4)
            date1 = array[1].split("/")
            date2 = array[2].split("/")
            if len(date1) == 1:
                date1 = array[1].split("-")
                date2 = array[2].split("-")
            if len(array) >= 4:
                channel_name = get_channel(client.get_all_channels(), array[3])
            else:
                channel_name = get_channel(client.get_all_channels(), "general")
            # channel_name = get_channel(client.guilds[message.guild.id].channels, array[3])
            m = int(date1[0]) # do not input 3 or 11
            d = int(date1[1])
            y = int(date1[2])
            mA = int(date2[0])
            dA = int(date2[1])
            yA = int(date2[2])
            aH = 7
            bH = 8
            #--------------------------
            tz = 0
            user_id = 0
            word = ""
            week = 0 # changes with -w flag
            if (len(array) == 5): # parameter parser
                array_end = array[4].split(" ")
                for i in range(len(array_end)): 
                    try:
                        if int(array_end[i]) < 24:
                            tz = int(array_end[i])
                        elif int(array_end[i]) > 10**16:
                            user_id = int(array_end[i])
                            flag_id = True
                    except:
                        if (array_end[i] == "-c"):
                            flag_case = True
                        elif (array_end[i].startswith("-w")):
                            array_week = array_end[i].split("w")
                            try:
                                week = int(array_week[1])
                                if week < 1 or week > 7:
                                    flag_error = False
                            except:
                                flag_error = False
                        else:
                            if flag_word:
                                word += " " + array_end[i]
                            else:
                                word = array_end[i]
                            flag_word = True
            aH = 7 - tz
            bH = 8 - tz
            if m >= 3 and m < 11: # DST on(6, 7), off(7, 8)
                aH -= 1
                bH -= 1
            if aH < 0:
                aH += 24
            print(str(aH) + " " + str(bH)) #
            # if (m == 3 or m == 11): # DST error
                # flag_error = False
            if y < 100:
                y += 2000
            if yA < 100:
                yA += 2000
            if (m > 12 or mA > 12) or (d > int(arr[1][m - 1]) or dA > int(arr[1][m - 1])) or (y >= 2100 or y < 2000 or yA >= 2100 or yA > 2100):
                flag_error = False
            if (y > yA or (y == yA and m > mA) or (y == yA and m == mA and d > dA)):
                flag_error = False
        except ValueError:
            flag_error = False

        data = open('data.txt', 'r') #
        flag_proc = f_read(data, 1)
            
        if flag_error and flag_proc:
            await client.send_message(message.channel, '<https://t.ly/kmvkA>')
            mesg = await client.send_message(message.channel, '`Processing...`')
            if array[0] == "^count":
                try:
                    wks.clear()
                    wks.append_row(['Date', '# of Messages'])
                except:
                    flag = False
                    flag_api = True
        #---------------------------
        DAY0 = str(m) + "/" + str(d) + "/" + str(y - 2000)
        flagS = False
        flagE = False
        total = 0
        while flag and flag_error and flag_proc:
            data = open('data.txt', 'w')
            print("1", file = data)
            data.close()
            while (d <= int(arr[1][m - 1]) or (m == 2 and d == 29 and y % 4 == 0)) and flag:
                if (m == mA and d == dA and y == yA):
                    flag = False
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
                if aH < 0:
                    aH += 24
                if bH < 0:
                    bH += 24
                #--------------------------    
                if m == 12 and d == 31: # new year
                    ymdB = datetime(y + 1, 1, 1, bH, 0, 0)
                elif d + 1 > int(arr[1][m - 1]) and (m != 2 or d != 28 or y % 4 != 0): # new month
                    ymdB = datetime(y, m + 1, 1, bH, 0, 0)
                else: # new day
                    ymdB = datetime(y, m, d + 1, bH, 0, 0)
                #--------------------------
                counter = 0
                DAY1 = str(m) + "/" + str(d) + "/" + str(y - 2000) # variable
                DAY2 = str(mA) + "/" + str(dA) + "/" + str(yA - 2000) # constant
                try:
                    if week == 0 or ymdA.isoweekday() == week:
                        async for msg in client.logs_from(channel_name, limit=30686, before=ymdB, after=ymdA, reverse=True): ###
                            counter = count(array, flag_id, flag_word, flag_case, word, counter, user_id, msg)
                        total += counter
                        line = DAY1 + " " + str(counter)
                        wks.append_row([DAY1, counter]) # to sheet
                        print('{}/{}/{} {}'.format(str(m), str(d), str(y - 2000), str(counter))) # to console
                        # print(line, file = data) # to file
                        # await client.edit_message(mesg, "`" + line + "`") # to discord    
                    d += 1
                except:
                    print('wait') #
                    await client.edit_message(mesg, "`Waiting... (use \'^stop\' to terminate if necessary)`")
                    flag_ast = True
                    flag_wait = True
                    t.sleep(3)
                    await client.edit_message(mesg, "`Processing...`")
                data = open('data.txt', 'r') #
                if not f_read(data, "2"):
                    strd = str(d)
                    if d < 10:
                        strd = "0" + str(d)
                    flag = False
                    flag_errcode = True
                data.close()
                #--------------------------    
            if m == 12 and d > 31:
                m = 0
                y += 1
            m += 1
            d = 1
        print('end')
        end = timeit.default_timer()
        str_time = "(" + str(truncate(end - start, 2)) + "s)"
        
        if flag_api:
            await client.send_message(message.channel, "`Error: API request overload.`")
        elif not flag_proc:
            await client.send_message(message.channel, "`Currently busy.`")
        elif flag_error:
            data = open('data.txt', 'w')
            print("0", file = data)
            data.close() #
            line2 = str(total) + ' message(s) accounted for. '
            if flag_errcode:
                errcode = 'ERR_CODE: ' + str(m - 1) + strd + str(y - 2000) + ' ' 
                line2 += errcode
            result = line2 + str_time
            if flag_ast:
                result += "*"
            # await client.delete_message(mesg)
            await client.edit_message(mesg, "`" + result + "`")
        else:
            await client.send_message(message.channel, "`Invalid parameters.`")
            
client.run("NTE2NDc2MzAxMjcyNjc4NDI0.XLa_kA.V0Lp47mbh2twr8qZsEE0RBQq1NM")

