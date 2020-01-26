# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio
import os # .env読み込みスターズ。

import datetime

class Bot_Owner_Command(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send('停止しやーす！！')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

def setup(airlinia):
    airlinia.add_cog(Bot_Owner_Command(airlinia))
