# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import os # .env読み込みスターズ。
import json

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
        self.data = json.load(open('./data/pokemon.json', 'r'))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member, server: discord.Member.guild):
        datas[str(server.id)]['all'] = len(server.members)
        datas[str(server.id)]['member'] = len([member for member in server.members if not member.bot])
        datas[str(server.id)]['bot'] = len([member for member in server.members if member.bot])
        with open('./data/pokemon.json', "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit(server.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        datas[str(server.id)]['message'] += 1
        server = message.guild
        with open('./data/pokemon.json', "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit(server.id)

    @tasks.loop(seconds=5)
    async def member_online(self, member: discord.Member, server: discord.Member.guild):
        datas[str(server.id)]['online'] = len([member for member in server.members if member.status.online])
        datas[str(server.id)]['idle'] = len([member for member in server.members if member.status.idle])
        datas[str(server.id)]['dnd'] = len([member for member in server.members if member.status.dnd])
        datas[str(server.id)]['offline'] = len([member for member in server.members if member.status.offline])
        with open('./data/pokemon.json', "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit(server.id)

    async def channel_name_edit(server_id):
        data = self.data
        self.all_channel : discord.VoiceChannel = self.bot.get_channel(self.all_channel_id)
        self.member_channel : discord.VoicetChannel = self.bot.get_channel(self.member_channel_id)
        self.bot_channel : discord.VoiceChannel = self.bot.get_channel(self.bot_channel_id)
        self.online_channel : discord.VoiceChannel = self.bot.get_channel(self.online_channel_id)
        self.idle_channel : discord.VoiceChannel = self.bot.get_channel(self.idle_channel_id)
        self.dnd_channel : discord.VoiceChannel = self.bot.get_channel(self.dnd_channel_id)
        self.offline_channel : discord.VoiceChannel = self.bot.get_channel(self.offline_channel_id)
        self.message_channel : discord.VoiceChannel = self.bot.get_channel(self.message_channel_id)
        self.time_channel : discord.VoiceChannel = self.bot.get_channel(self.time_channel_id)

        await self.all_channel.edit(name=f'all : {data[server_id]["all"]}')
        await self.member_channel.edit(name=f'member : {data[server_id]["member"]}')
        await self.bot_channel.edit(name=f'bot : {data[server_id]["bot"]}')
        await self.online_channel.edit(name=f'online : {data[server_id]["online"]}')
        await self.idle_channel.edit(name=f'idle : {data[server_id]["idle"]}')
        await self.dnd_channel.edit(name=f'dnd : {data[server_id]["dmd"]}')
        await self.offline_channel.edit(name=f'offline : {data[server_id]["offline"]}')
        await self.message_channel.edit(name=f'message : {data[server_id]["message"]}')
        await self.time.all_channel.edit(name=f'time : {data[server_id]["time"]}')

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
