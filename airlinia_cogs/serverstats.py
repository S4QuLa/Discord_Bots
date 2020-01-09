# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import os # .env読み込みスターズ。
import json

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        with open('./data/stats.json', 'r') as f:
            self.datas = json.load(f)
            print(self.datas)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        self.datas["all"] = len(server.members)
        self.datas["member"] = len([member for member in server.members if not member.bot])
        self.datas["bot"] = len([member for member in server.members if member.bot])
        with open("./data/pokemon.json", "w") as f:
            json.dump(self.datas, f, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        server = message.guild
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.datas["message"] += 1
        with open("./data/pokemon.json", "w") as f:
            json.dump(f, datas, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_member_updata(self, before, after):
        server = after.guild
        self.datas["online"] = len([member for member in server.members if member.status.online])
        self.datas["idle"] = len([member for member in server.members if member.status.idle])
        self.datas["dnd"] = len([member for member in server.members if member.status.dnd])
        self.datas["offline"] = len([member for member in server.members if member.status.offline])
        with open("./data/pokemon.json", "w") as f:
            json.dump(f, datas, indent=4)
        await channel_name_edit()

    # async def channel_name_edit():
        # await self.bot.get_channel(663297143909515274).all_channel.edit(name=f"all : {self.datas["all"]}")
        # await self.bot.get_channel(663297196531253249).member_channel.edit(name=f"member : {datas["member"]}")
        # await self.bot.get_channel(663297233453842452).bot_channel.edit(name=f"bot : {datas["bot"]}")
        # await self.bot.get_channel(663297268455309332).online_channel.edit(name=f"online : {datas["online"]}")
        # await self.bot.get_channel(664160147886833678).idle_channel.edit(name=f"idle : {datas["idle"]}")
        # await self.bot.get_channel(664160201125003295).dnd_channel.edit(name=f"dnd : {datas["dnd"]}")
        # await self.bot.get_channel(663297305847398421).offline_channel.edit(name=f"offline : {datas["offline"]}")
        # await self.bot.get_channel(663297421417119754).message_channel.edit(name=f"message : {datas["message"]}")
        # await self.bot.get_channel(663297453621116988).time.all_channel.edit(name=f"time : {datas["time"]}")

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
