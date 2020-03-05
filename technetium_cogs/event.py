# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import os # .env読み込みスターズ。
import json

import random

class Event(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            after.channel is not None
            and (before.channel is None or before.channel != after.channel)
        ):
            embed = discord.Embed(title='ボイスチャンネル入室通知',
            description=f'{member.mention}さんが入室しました。',
            color=0x00ff00)
            await self.bot.get_channel(596668583728119809).send(embed=embed, delete_after=180)

        if (
            before.channel is not None
            and (after.channel is None or before.channel != after.channel)
        ):
            embed = discord.Embed(title='ボイスチャンネル退出通知',
            description=f'{member.mention}さんが退出しました。',
            color=0xff0000)
            await self.bot.get_channel(596668583728119809).send(embed=embed, delete_after=180)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cl = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(title=f"利用規約はここから",
                              description=f"{member.guild.name}へようこそ！{member.name}さん！\n{len(member.guild.members)}人目の参加者です！\n> 何か困ったことがあればぜひとも運営にメンションをしてください。\n> 基本一人は常駐してます。",
                              url="https://www.elegraph.cf/?page_id=24",
                              color=cl)
        embed.set_author(name=f"{member.display_name}さんが参加しました～！")
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.get_channel(596668568909643817).send(embed=embed)

def setup(technetium):
    technetium.add_cog(Event(technetium))
