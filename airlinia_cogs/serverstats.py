# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import arrow
import os # .env読み込みスターズ。
import json
import locale

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        with open('./date/airlinia_stats.json', 'r') as f:
            self.dates = json.load(f)
        # -----------
        self.time.start()
        self.hour_reset.start()

    def cog_unload(self):
        self.time.stop()
        self.hour_reset.stop()

 #######################################################################

    @tasks.loop(seconds=3.0) # minutes
    async def time(self):
        date_time = arrow.now('Asia/Tokyo').format(fmt='YYYY/MM/DD(ddd)HH:mm:ss', locale='ja')
        await self.bot.get_channel(665355834498351154).edit(name=f"time : {date_time}")

    @time.before_loop
    async def time_wait(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1.0) # hours
    async def hour_reset(self):
        self.dates["hour_message"] = 0
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    @hour_reset.before_loop
    async def hour_reset_wait(self):
        await self.bot.wait_until_ready()

 #######################################################################

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        server_members = server.members
        self.dates["all"] = len(server.members)
        self.dates["member"] = len([member for member in server.members if not member.bot])
        self.dates["bot"] = len([member for member in server.members if member.bot])
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        server = member.guild
        server_members = server.members
        self.dates["all"] = len(server.members)
        self.dates["member"] = len([member for member in server.members if not member.bot])
        self.dates["bot"] = len([member for member in server.members if member.bot])
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()
  # -------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.dates["message"] += 1
        self.dates["hour_message"] += 1
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server = after.guild
        self.dates["all_status"]["online"] = len([member for member in server.members if member.status == discord.Status.online])
        self.dates["all_status"]["idle"] = len([member for member in server.members if member.status == discord.Status.idle])
        self.dates["all_status"]["dnd"] = len([member for member in server.members if member.status == discord.Status.dnd])
        self.dates["all_status"]["offline"] = len([member for member in server.members if member.status == discord.Status.offline])
        self.dates["mobile"] = len([member for member in server.members if member.is_on_mobile()])
        self.dates["desktop"] = len([member for member in server.members if not member.is_on_mobile()])
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        await self.channel_name_edit()

 #######################################################################

    async def channel_name_edit(self):
        await self.bot.get_channel(665355267231449090).edit(name=f"all : {self.dates['all']}")
        await self.bot.get_channel(665355410672189471).edit(name=f"member : {self.dates['member']}")
        await self.bot.get_channel(665355451793276955).edit(name=f"bot : {self.dates['bot']}")
        # ---------------
        await self.bot.get_channel(665355545548554270).edit(name=f"online : {self.dates['all_status']['online']}")
        await self.bot.get_channel(665355588674387978).edit(name=f"idle : {self.dates['all_status']['idle']}")
        await self.bot.get_channel(665355615572459520).edit(name=f"dnd : {self.dates['all_status']['dnd']}")
        await self.bot.get_channel(665355714084208679).edit(name=f"offline : {self.dates['all_status']['offline']}")
        # ---------------
        await self.bot.get_channel(665355793742430268).edit(name=f"mobile : {self.dates['mobile']}")
        await self.bot.get_channel(665355766131326996).edit(name=f"desktop : {self.dates['desktop']}")
        # ---------------
        await self.bot.get_channel(665356186983333909).edit(name=f"message : {self.dates['message']}")
        await self.bot.get_channel(665356237038419990).edit(name=f"hour_message : {self.dates['hour_message']}")

 # ----------------------------------------------

    @commands.command(name='serverstatus')
    async def status(self, ctx):
        server = ctx.guild
        self.dates["desktop_status"]["online"] = len([member for member in server.members if member.desktop_status == discord.Status.online])
        self.dates["desktop_status"]["idle"] = len([member for member in server.members if member.desktop_status == discord.Status.idle])
        self.dates["desktop_status"]["dnd"] = len([member for member in server.members if member.desktop_status == discord.Status.dnd])
        self.dates["web_status"]["online"] = len([member for member in server.members if member.web_status == discord.Status.online])
        self.dates["web_status"]["idle"] = len([member for member in server.members if member.web_status == discord.Status.idle])
        self.dates["web_status"]["dnd"] = len([member for member in server.members if member.web_status == discord.Status.dnd])
        self.dates["mobile_status"]["online"] = len([member for member in server.members if member.mobile_status == discord.Status.online])
        self.dates["mobile_status"]["idle"] = len([member for member in server.members if member.mobile_status == discord.Status.idle])
        self.dates["mobile_status"]["dnd"] = len([member for member in server.members if member.mobile_status == discord.Status.dnd])
        with open("./date/airlinia_stats.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        embed=discord.Embed(title="サーバーステータス", description=f"サーバー名：{ctx.guild.name}\nサーバー地域：{ctx.guild.region}\nサーバー所有者：{ctx.guild.owner.name}")
        embed.set_author(name=f"{ctx.guild.name} - ステータス")
        embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.add_field(name="メンバー人数", value=f"all : {self.dates['all']}\nmember : {self.dates['member']}\nbot : {self.dates['bot']}", inline=True)
        embed.add_field(name="メッセージ数", value=f"message : {self.dates['message']}\nhour message : {self.dates['hour_message']}", inline=True)
        embed.add_field(name="メンバーステータス", value=f"online : {self.dates['all_status']['online']}\nidle : {self.dates['all_status']['idle']}\ndnd : {self.dates['all_status']['dnd']}\noffline : {self.dates['all_status']['offline']}", inline=False)
        embed.add_field(name="desktop", value=f"online : {self.dates['desktop_status']['online']}\nidle : {self.dates['desktop_status']['idle']}\ndnd : {self.dates['desktop_status']['dnd']}", inline=True)
        embed.add_field(name="web", value=f"online : {self.dates['web_status']['online']}\nidle : {self.dates['web_status']['idle']}\ndnd : {self.dates['web_status']['dnd']}", inline=True)
        embed.add_field(name="mobile", value=f"online : {self.dates['mobile_status']['online']}\nidle : {self.dates['mobile_status']['idle']}\ndnd : {self.dates['mobile_status']['dnd']}", inline=True)
        await ctx.message.channel.send(embed=embed)


def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
