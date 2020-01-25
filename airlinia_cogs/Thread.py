# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

class Thread(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print("category_id:", reaction.message.channel.category_id, "\nemoji_id:",  reaction.emoji.id)
        if reaction.message.channel.category_id == 668142017175617546 or reaction.message.channel.category_id == 668374572080562177:
            if reaction.emoji.id == 665462194116493313:
                member = [reaction.message.member, user]
                channel = _free_channel_create(reaction.message.channel.category, member, "Thread")
                embed = discord.Embed(title='チャンネル作成しました。',
                description=f'{channel.mention}\rスレッドを作成しました。',
                color=0x0080ff)
                channel.send(embed=embed, content=f"{user.mention}、{reaction.message.user.mention}")

    async def _free_channel_create(self, category, member, name):
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
        channel = await category.create_text_channel(name, overwrites=overwrites)
        return channel

def setup(airlinia):
    airlinia.add_cog(Thread(airlinia))
