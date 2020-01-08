# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import os # .env読み込みスターズ。
import json

def json_load(path):
    with open(path, "r") as f:
        return json.load(f)

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.datas = json_load("./data/pokemon.json")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        datas = self.datas
        server = member.guild
        datas["all"] = len(server.members)
        datas["member"] = len([member for member in server.members if not member.bot])
        datas["bot"] = len([member for member in server.members if member.bot])
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        datas = self.datas
        server = message.guild
        if message.author.bot:  # ボットのメッセージをハネる
            return
        datas["message"] += 1
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_member_updata(self, before, after):
        datas = self.datas
        server = after.guild
        datas["online"] = len([member for member in server.members if member.status.online])
        datas["idle"] = len([member for member in server.members if member.status.idle])
        datas["dnd"] = len([member for member in server.members if member.status.dnd])
        datas["offline"] = len([member for member in server.members if member.status.offline])
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    async def channel_name_edit():
        datas = self.datas
        await self.bot.get_channel(663297143909515274).edit(name=f"all : {datas["all"]}")
        await self.bot.get_channel(663297196531253249).edit(name=f"member : {datas["member"]}")
        await self.bot.get_channel(663297233453842452).edit(name=f"bot : {datas["bot"]}")
        await self.bot.get_channel(663297268455309332).edit(name=f"online : {datas["online"]}")
        await self.bot.get_channel(664160147886833678).edit(name=f"idle : {datas["idle"]}")
        await self.bot.get_channel(664160201125003295).edit(name=f"dnd : {datas["dnd"]}")
        await self.bot.get_channel(663297305847398421).edit(name=f"offline : {datas["offline"]}")
        await self.bot.get_channel(663297421417119754).edit(name=f"message : {datas["message"]}")
        await self.bot.get_channel(663297453621116988).edit(name=f"time : {datas["time"]}")

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
