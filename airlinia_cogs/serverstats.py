# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import arrow
import os # .env読み込みスターズ。
import json

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.time.start()
        self.hour_reset.start()
        # -----------
        with open('./date/airlinia_stats.json', 'r') as f:
            self.dates = json.load(f)

    def cog_unload(self):
        self.time.cancel()
        self.hour_reset.cancel()

 #######################################################################

    @tasks.loop(seconds=1, loop=bot.loop) # minutes
    async def time(self):
        date_time = arrow.now('Asia/Tokyo').format(fmt='YYYY/MM/DD(ddd)HH:mm:ss', locale='ja')
        await self.bot.get_channel(665355834498351154).edit(name=f"time : {date_time}")

    @time.before_loop
    async def before_time(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1, loop=bot.loop) # hours
    async def hour_reset(self):
        self.dates["hour_message"] = 0
        ########################
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.bot.get_channel(665356237038419990).edit(name=f"hour_message : {self.dates['hour_message']}")

    @hour_reset.before_loop
    async def before_hour_reset(self):
        await self.bot.wait_until_ready()

 #######################################################################

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        server_members = server.members
        await self.bot.get_channel(665355267231449090).edit(name=f"all : {len(server.members)}")
        await self.bot.get_channel(665355410672189471).edit(name=f"member : {len([member for member in server.members if not member.bot])}")
        await self.bot.get_channel(665355451793276955).edit(name=f"bot : {len([member for member in server.members if member.bot])}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        server = member.guild
        server_members = server.members
        await self.bot.get_channel(665355267231449090).edit(name=f"all : {len(server.members)}")
        await self.bot.get_channel(665355410672189471).edit(name=f"member : {len([member for member in server.members if not member.bot])}")
        await self.bot.get_channel(665355451793276955).edit(name=f"bot : {len([member for member in server.members if member.bot])}")

  # -------------------------

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.dates["message"] += 1
        self.dates["hour_message"] += 1
        await self.bot.get_channel(665356186983333909).edit(name=f"message : {self.dates['message']}")
        await self.bot.get_channel(665356237038419990).edit(name=f"hour_message : {self.dates['hour_message']}")
        ########################
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server = after.guild
        online = len([member for member in server.members if member.status == discord.Status.online])
        idle = len([member for member in server.members if member.status == discord.Status.idle])
        dnd = len([member for member in server.members if member.status == discord.Status.dnd])
        await self.bot.get_channel(665355545548554270).edit(name=f"online : {online + idle + dnd}")
        await self.bot.get_channel(665355714084208679).edit(name=f"offline : {len([member for member in server.members if member.status == discord.Status.offline])}")
        # -------------------------------
        await self.bot.get_channel(665355793742430268).edit(name=f"mobile : {len([member for member in server.members if member.is_on_mobile()])}")
        await self.bot.get_channel(665355766131326996).edit(name=f"desktop : {len([member for member in server.members if not member.is_on_mobile()])}")
        ########################
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
