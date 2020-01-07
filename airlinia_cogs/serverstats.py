# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio
import os # .env読み込みスターズ。
import json

def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.all_channel_id = 663297143909515274
        self.member_channel_id = 663297196531253249
        self.bot_channel_id = 663297233453842452
        self.online_channel_id = 663297268455309332
        self.idle_channel_id = 664160147886833678
        self.dnd_channel_id = 664160201125003295
        self.offline_channel_id = 663297305847398421
        self.message_channel_id = 663297421417119754
        self.time_channel_id = 663297453621116988
        self.data = load_json("./data/stats.json")

    async def channel_name_edit():
        self.all_channel : discord.VoiceChannel = self.bot.get_channel(self.all_channel_id)
        self.member_channel : discord.VoicetChannel = self.bot.get_channel(self.member_channel_id)
        self.bot_channel : discord.VoiceChannel = self.bot.get_channel(self.bot_channel_id)
        self.online_channel : discord.VoiceChannel = self.bot.get_channel(self.online_channel_id)
        self.idle_channel : discord.VoiceChannel = self.bot.get_channel(self.idle_channel_id)
        self.dnd_channel : discord.VoiceChannel = self.bot.get_channel(self.dnd_channel_id)
        self.offline_channel : discord.VoiceChannel = self.bot.get_channel(self.offline_channel_id)
        self.message_channel : discord.VoiceChannel = self.bot.get_channel(self.message_channel_id)
        self.time_channel : discord.VoiceChannel = self.bot.get_channel(self.time_channel_id)

        await self.all_channel.edit(name=f'all : {self.data.get('all', 'Nodata')}')
        await self.member_channel.edit(name=f'member : {self.data.get('member', 'Nodata')}')
        await self.bot_channel.edit(name=f'bot : {self.data.get('bot', 'Nodata')}')
        await self.online_channel.edit(name=f'online : {self.data.get('online', 'Nodata')}')
        await self.idle_channel.edit(name=f'idle : {self.data.get('idle', 'Nodata')}')
        await self.dnd_channel.edit(name=f'dnd : {self.data.get('dmd', 'Nodata')}')
        await self.offline_channel.edit(name=f'offline : {self.data.get('offline', 'Nodata')}')
        await self.message_channel.edit(name=f'message : {self.data.get('message', 'Nodata')}')
        await self.time.all_channel.edit(name=f'time : {self.data.get('time', 'Nodata')}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member, server: discord.Member.Guild):
        self.bot[str(server.id)]['all'] = {len(server.members)}
        self.bot[str(server.id)]['member'] = {len([member for member in server.members if not member.bot])}
        self.bot[str(server.id)]['bot'] = {len([member for member in server.members if member.bot])}
        channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        self.bot[str(server.id)]['message'] += 1
        channel_name_edit()

    @tasks.loop(seconds=1, loop=loop)
    async def member_online(self, member: discord.Member, server: discord.Member.Guild):
        self.bot[str(server.id)]['online'] = {len([member for member in server.members if member.status.online])}
        self.bot[str(server.id)]['idle'] = {len([member for member in server.members if member.status.idle])}
        self.bot[str(server.id)]['dnd'] = {len([member for member in server.members if member.status.dnd])}
        self.bot[str(server.id)]['offline'] = {len([member for member in server.members if member.status.offline])}
        channel_name_edit()

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
