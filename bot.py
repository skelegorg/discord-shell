import discord
from discord.ext import commands
import getpass
import json
import time
import os
import platform
import socket
import ctypes

if(platform.system() == "Windows"):
    os.system('color')

ctypes.windll.kernel32.SetConsoleTitleW("Discord")

settings = {}
with open("settings.json", "r") as stg:
    settings = json.loads(stg.read())

client = commands.Bot(command_prefix=">")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with the shell'))
    # configure headless boot
    if(settings["HEADLESS_BOOT"] == "True"):
        guild = client.get_guild(int(settings["DEFAULT_SERVER_ID"]))
        await open_terminal(guild, "headless")

@client.command()
async def terminal(ctx, arg):
    if(arg == "start"):
        await ctx.send("loading session.")
        await open_terminal(ctx.guild, str(ctx.author))
    elif(arg == "close"):
        # end the active session
        await ctx.send("ending session.")
        quit()

async def open_terminal(guild, auth):
    inTerminal = True
    level = "ca"
    active_guild = guild

    # load categories
    activeCategory = ""
    categoryList = {}
    for category in active_guild.categories:
        name = category.name.lower()
        categoryList.update({name: category})
    
    # channel data
    activeChannel = ""
    channelList = {}
    messages = []

    # user vanity
    user = auth
    userspl = user.split("#")
    tag = userspl[0]

    compname = str(socket.gethostname())
    uname = str(getpass.getuser())

    # run interactive shell
    while(inTerminal):
        command = input(f"{uname}@{compname}: ~/{tag}/{active_guild.name}/{activeCategory} $ ")
        parsedCommand = command.split()
        for item in parsedCommand:
            item = item.lower()
        if(parsedCommand[0] == "ls"):
            if(level == "ca"):
                for item in categoryList:
                    print(item)
            elif(level == "ch"):
                # list each channel under activeCategory
                for channel in categoryList[activeCategory].text_channels:
                    print(channel.name)
        elif(parsedCommand[0] == "cd"):
            try:
                if(level == "ca"):
                    if(parsedCommand[1] in categoryList):
                        level = "ch"
                        activeCategory = parsedCommand[1]
                        for channel in categoryList[activeCategory].text_channels:
                            channelList.update({channel.name.lower(): channel})
                    else:
                        print(f"no such category \'{parsedCommand[1]}\' found.")
                elif(level == "ch"):
                    activeCategory = ""
                    level = "ca"
                else:
                    print("i fucked up")
            except IndexError:
                print('supply a path.')
        elif(parsedCommand[0] == "snap"):
            try:
                if(parsedCommand[1] in channelList):
                    activeChannel = parsedCommand[1]
                    activeChannelObject = channelList[activeChannel]
                    # swap ctx channel
                    # ctx.channel = activeChannelObject.id
                    # get the last 15 messages in the channel
                    messages = await activeChannelObject.history(limit=15).flatten()
                    messages.reverse()
                    for message in messages:
                        authorOutp = str(message.author)
                        if(not bool(settings['PRINT_IDENTIFIERS'])):
                            authorSpl = str(message.author).split("#")
                            authorOutp = authorSpl[0]
                        print(f"{bcolors.OKGREEN}{authorOutp}:{bcolors.ENDC} {message.content}")
                else:
                    print(f"no such channel {parsedCommand[1]}.")
            except IndexError:
                print("supply a path.")
        elif(parsedCommand[0] == "watch"):
            try:
                if(parsedCommand[1] in channelList):
                    activeChannel = parsedCommand[1]
                    activeChannelObject = channelList[activeChannel]
                    # swap ctx channel
                    # ctx.channel = activeChannelObject.id
                    messages = await activeChannelObject.history(limit=15).flatten()
                    messages.reverse()
                    lastMessage = await getRecentMsg(activeChannelObject)
                    sendMode = True
                    for message in messages:
                        authorOutp = str(message.author)
                        if(not bool(settings['PRINT_IDENTIFIERS'])):
                            authorSpl = str(message.author).split("#")
                            authorOutp = authorSpl[0]
                        print(f"{bcolors.OKGREEN}{authorOutp}:{bcolors.ENDC} {message.content}")
                    while(sendMode):
                        time.sleep(0.05)
                        curMsg = await getRecentMsg(activeChannelObject)
                        checc = cacheRefresh(curMsg, lastMessage)
                        if(checc):
                            authorOutp = str(curMsg.author)
                            if(not bool(settings['PRINT_IDENTIFIERS'])):
                                authorSpl = str(curMsg.author).split("#")
                                authorOutp = authorSpl[0]
                            print(f"{bcolors.OKGREEN}{authorOutp}:{bcolors.ENDC} {message.content}")
                            lastMessage = curMsg
                else:
                    print(f"no such channel \"{parsedCommand[1]}\".")
            except IndexError:
                print("supply a path")
        elif(parsedCommand[0] == "send"):
            # send [channel] [message]
            msg = ""
            for i in range(len(parsedCommand)):
                if(i > 1):
                    msg += f"{parsedCommand[i]} "
            # get channel associated with parsedcommand[1]
            if parsedCommand[1] in channelList:
                activeChannel = parsedCommand[1]
                activeChannelObject = channelList[activeChannel]
                await activeChannelObject.send(msg)
            else: 
                print(f"no such channel \"{parsedCommand[i]}\"")
        elif(parsedCommand[0] == "stream"):
            # stream with message refresh (enter)
            try:
                if(parsedCommand[1] in channelList):
                    activeChannel = parsedCommand[1]
                    activeChannelObject = channelList[activeChannel]
                    # swap ctx channel
                    # ctx.channel = activeChannelObject.id
                    messages = await activeChannelObject.history(limit=15).flatten()
                    messages.reverse()
                    lastMessage = await getRecentMsg(activeChannelObject)
                    sendMode = True
                    for message in messages:
                        authorOutp = str(message.author)
                        if(not bool(settings['PRINT_IDENTIFIERS'])):
                            authorSpl = str(message.author).split("#")
                            authorOutp = authorSpl[0]
                        print(f"{bcolors.OKGREEN}{authorOutp}:{bcolors.ENDC} {message.content}")
                    while(sendMode):
                        curMsg = await getRecentMsg(activeChannelObject)
                        checc = cacheRefresh(curMsg, lastMessage)
                        if(checc):
                            authorOutp = str(curMsg.author)
                            if(not bool(settings['PRINT_IDENTIFIERS'])):
                                authorSpl = str(curMsg.author).split("#")
                                authorOutp = authorSpl[0]
                            print(f"{bcolors.OKGREEN}{authorOutp}:{bcolors.ENDC} {curMsg.content}")
                            lastMessage = curMsg
                        sned = input()
                        if(sned == "estream"):
                            sendMode = False
                        elif(sned != ""):
                            await activeChannelObject.send(sned)
                    else:
                        print(f"no such channel \"{parsedCommand[1]}\".")
            except IndexError:
                print(f"no such channel {parsedCommand[1]} found.")
        elif(parsedCommand[0] == "exit"):
            inTerminal = False
        else:
            print(f"no such command \'{parsedCommand[0]}\' found.")

async def getRecentMsg(channel):
    ret = await channel.history(limit=1).flatten()
    return ret[0]

def cacheRefresh(curMsg, lastMessage):
    if(curMsg != lastMessage):
        return True
    return False

client.run(settings['TOKEN'])