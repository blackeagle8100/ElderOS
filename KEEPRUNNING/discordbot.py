#!/usr/bin/env python3

import subprocess
import nest_asyncio
nest_asyncio.apply()
import time
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # Enable message content updates
bot = commands.Bot(command_prefix='!', intents=intents)

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='webcam', help='webcamcontrol')
async def webcam(ctx):
    #await ctx.send('Webcam wordt bestuurd.')
    subprocess.run([vastsysteem_path+"/KEEPRUNNING/botcam.py"])


@bot.command(name='join', help='join channel')
async def join(ctx):
    #await ctx.send('Webcam wordt bestuurd.')
    subprocess.run(["xdotool", "keydown", "Control","keydown","Shift","key","L","keyup","Control","keyup","Shift"])
    # Additional delay to ensure the window is fully activated
    time.sleep(1)
    subprocess.run(['wmctrl','-a','MAIN'])
    

@bot.command(name='ping', help='Ping command')
async def ping(ctx):
    await ctx.send('pongdongelong')

# Replace 'YOUR_BOT_TOKEN' with the actual bot token
bot.run('YOUR_BOT_TOKEN')#FILL IN WITH SETUP PLZ
