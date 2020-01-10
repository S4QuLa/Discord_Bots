# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import os # .env読み込みスターズ。
import json
import schedule
import datetime

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        with open('./date/stats.json', 'r') as f:
            self.dates = json.load(f)
        schedule.every(1).minutes.do(self.time)
        schedule.every(1).hours.do(self.hour_time_reset)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        server_members = server.members
        self.dates["all"] = len(server.members)
        self.dates["member"] = len([member for member in server.members if not member.bot])
        self.dates["bot"] = len([member for member in server.members if member.bot])
        with open("./date/stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.dates["message"] += 1
        self.dates["hour_message"] += 1
        with open("./date/stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server = after.guild
        self.dates["online"] = len([member for member in server.members if member.status == discord.Status.online])
        self.dates["idle"] = len([member for member in server.members if member.status == discord.Status.idle])
        self.dates["dnd"] = len([member for member in server.members if member.status == discord.Status.dnd])
        self.dates["offline"] = len([member for member in server.members if member.status == discord.Status.offline])
        self.dates["mobile"] = len([member for member in server.members if member.mobile_status])
        self.dates["desktop"] = len([member for member in server.members if member.desktop_status])
        with open("./date/stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    async def time(self):
        yobi = ["月","火","水","木","金","土","日"]
        tobi_today = yobi[datetime.date.today().weekday()]
        nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d' + yobi_today + '%H:%M:%S')
        self.dates["time"] = nowtime
        with open("./date/stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    async def hour_time_reset(self):
        self.dates["hour_message"] = 0
        with open("./date/stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    async def channel_name_edit(self):
        await self.bot.get_channel(663297143909515274).edit(name=f"all : {self.dates['all']}")
        await self.bot.get_channel(663297196531253249).edit(name=f"member : {self.dates['member']}")
        await self.bot.get_channel(663297233453842452).edit(name=f"bot : {self.dates['bot']}")
        # ---------------
        await self.bot.get_channel(663297268455309332).edit(name=f"online : {self.dates['online']}")
        await self.bot.get_channel(664160147886833678).edit(name=f"idle : {self.dates['idle']}")
        await self.bot.get_channel(664160201125003295).edit(name=f"dnd : {self.dates['dnd']}")
        await self.bot.get_channel(663297305847398421).edit(name=f"offline : {self.dates['offline']}")
        # ---------------
        await self.bot.get_channel(665106455371972609).edit(name=f"mobile : {self.dates['mobile']}")
        await self.bot.get_channel(665106507125358603).edit(name=f"desktop : {self.dates['desktop']}")
        # ---------------
        await self.bot.get_channel(663297421417119754).edit(name=f"message : {self.dates['message']}")
        await self.bot.get_channel(665106327319609359).edit(name=f"hour_message : {self.dates['hour_message']}")
        # ---------------
        await self.bot.get_channel(663297453621116988).edit(name=f"time : {self.dates['time']}")

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
