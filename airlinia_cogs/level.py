# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio

import pymongo

class Level(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia

        mongo_connection = pymongo.MongoClient("ds161505.mlab.com", 61505, retryWrites=False)
        mongo_db = mongo_connection["heroku_stfrs35p"]
        mongo_db.authenticate("heroku_stfrs35p", os.environ['MONGODB_PASSWORD'])
        self.mongo_coll = mongo_db['subdomain']

def setup(airlinia):
    airlinia.add_cog(Level(airlinia))
