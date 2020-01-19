# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

class Thread(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        # -----------
        with open('./date/voicechannel.json', 'r') as f:
            self.dates = json.load(f)

    @commands.Cog.listener()
    async def on_reaction_add(reaction, user):
        if reaction.message.channel.category.id == 668142017175617546 or reaction.message.channel.category.id == 668374572080562177:
            member = [reaction.message.member, user]
            _free_channel_create(reaction.message.channel.category, member, "Thread")

    async def _free_channel_create(self, category, member, name, VC=False):
        overwrites = {
            self.bot.user:
                discord.PermissionOverwrite.from_pair(discord.Permissions.all(), discord.Permissions.none()),
            category.guild.default_role:
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            member:
                discord.PermissionOverwrite.from_pair(discord.Permissions(66448721), discord.Permissions.none()),
            category.guild.get_role(635149066795483137): #ミュート。
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            category.guild.get_role(617017694306435073): #閲覧できる役職
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129)),
        }
        if VC:
            channel = await category.create_voice_channel(name, overwrites=overwrites)
            return channel
        else:
            channel = await category.create_text_channel(name, overwrites=overwrites, position=3)
            return channel
