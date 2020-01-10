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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        server_members = server.members
        self.datas["all"] = len(server.members)
        self.datas["member"] = len([member for member in server.members if not member.bot])
        self.datas["bot"] = len([member for member in server.members if member.bot])
        with open("./data/pokemon.json", "w") as f:
            json.dump(self.datas, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.datas["message"] += 1
        with open("./data/pokemon.json", "w") as f:
            json.dump(self.datas, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server = after.guild
        self.datas["online"] = len([member for member in server.members if member.status.online])
        self.datas["idle"] = len([member for member in server.members if member.status.idle])
        self.datas["dnd"] = len([member for member in server.members if member.status.dnd])
        self.datas["offline"] = len([member for member in server.members if member.status.offline])
        with open("./data/pokemon.json", "w") as f:
            json.dump(self.datas, f, indent=4)
        await self.channel_name_edit()

    async def channel_name_edit(self):
        await self.bot.get_channel(663297143909515274).edit(name=f"all : {self.datas['all']}")
        await self.bot.get_channel(663297196531253249).edit(name=f"member : {self.datas['member']}")
        await self.bot.get_channel(663297233453842452).edit(name=f"bot : {self.datas['bot']}")
        await self.bot.get_channel(663297268455309332).edit(name=f"online : {self.datas['online']}")
        await self.bot.get_channel(664160147886833678).edit(name=f"idle : {self.datas['idle']}")
        await self.bot.get_channel(664160201125003295).edit(name=f"dnd : {self.datas['dnd']}")
        await self.bot.get_channel(663297305847398421).edit(name=f"offline : {self.datas['offline']}")
        await self.bot.get_channel(663297421417119754).edit(name=f"message : {self.datas['message']}")
        await self.bot.get_channel(663297453621116988).edit(name=f"time : {self.datas['time']}")

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
