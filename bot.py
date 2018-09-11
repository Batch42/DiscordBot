import discord
from discord.ext import commands
from threading import Thread
import time
import json
import asyncio
import sys
from collections import defaultdict

#Application Variables
file = 'data.json'
temp=open(file)
data=json.loads(temp.read())
temp.close()
#End


description = 'The system which suports all of Steven\'s shitty machinations'
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def shutdown(ctx):
    name = str(ctx.message.author)
    if name == data['me']:
        writer = open(file,'w')
        writer.write(json.dumps(data))
        writer.close()
        await bot.close()
''' Security Hazard
@bot.command(pass_context=True)
async def debug(ctx, cmd):
    name = str(ctx.message.author)
    bob='hi'
    if name == me:
        exec('print (' + cmd + ')',globals(),locals())
'''
@bot.command(pass_context=True)
async def join(ctx):
    name = str(ctx.message.author)
    if name not in data['players']:
        data['players'].append(name)
        await broadcast(ctx.message.channel)

@bot.command(pass_context=True)
async def when(ctx):
    await broadcast(ctx.message.channel)

def broadcast(chan):
    date = 'Friday at 7pm.'
    msg = 'Endless Space 2 is occuring ' + date + '\n'
    msg += 'The following souls have surrendered themselves to it:\n'
    for player in data['players']:
        msg+= player.split('#')[0] + "\n"
    msg+='\nTo sign yourself up, simply enter "!join"'
    return bot.send_message(chan,msg)

async def on_time():
    await bot.wait_until_ready()
    flag=True
    while not bot.is_closed:
        if time.localtime()[3] % 12 == 0:
            if flag:
                for server in bot.servers:
                    for chan in server.channels:
                        if "eneral" in chan.name and chan.type == discord.ChannelType.text:
                            await broadcast(chan)
                flag = False
        else:
            flag = True
        await asyncio.sleep(4)

token = open('token.dnp').read()[:-1]
bot.loop.create_task(on_time())
bot.run(token)
