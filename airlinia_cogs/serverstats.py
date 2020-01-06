# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio
import os # .env読み込みスターズ。
import json

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
