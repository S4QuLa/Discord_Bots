# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio

import pymongo
import os

class Level(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium

def setup(technetium):
    technetium.add_cog(Event(technetium))
