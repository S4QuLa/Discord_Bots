# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

class Voice_Channel(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        # -----------
        with open('./date/voicechannel.json', 'r') as f:
            self.dates = json.load(f)

    @property
    def category(self):
        return self.bot.get_channel(655274860708364288)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            after.channel is not None
            and (before.channel is None or before.channel != after.channel)
        ):
            if after.channel.id == 655274902600941579:
                await self._channel_create(member)
            else:
                try:
                    text_channel = self.bot.get_channel(self.dates[after.chaneel.id])
                except KeyError:
                    pass
                else:
                    embed = discord.Embed(title='ボイスチャンネル入室通知',
                    description=f'{member.mention}さんが入室しました。',
                    color=0x00ff00)
                    await text_channel.send(embed=embed, delete_after=180)

        if (
            before.channel is not None
            and (after.channel is None or before.channel != after.channel)
        ):
            try:
                text_channel = self.bot.get_channel(self.dates[before.channel.id])
            except KeyError:
                pass
            else:
                embed = discord.Embed(title='ボイスチャンネル退出通知',
                description=f'{member.mention}さんが退出しました。',
                color=0xff0000)
                await text_channel.send(embed=embed, delete_after=180)
                if before.channel.members is None:
                    before.channel.delete()
                    text_channel.delete()
                    del self.dates[before.channel.id]
                    with open("./date/voicechannel.json", "w") as f:
                        json.dump(self.dates, f, indent=4)

        if (
            after.channel is not None and before.channel is not None
            and before.channel != after.channel
        ):
            if after.channel.id == 655274902600941579:
                try:
                    text_channel = self.bot.get_channel(self.dates[before.channel.id])
                except KeyError:
                    pass
                else:
                    embed = discord.Embed(title='ボイスチャンネル退出通知',
                    description=f'{member.mention}さんが退出しました。',
                    color=0xff0000)
                    await text_channel.send(embed=embed, delete_after=180)
                    await self._channel_create(member)
                    if before.channel.members is None:
                        before.channel.delete()
                        text_channel.delete()
                        del self.dates[before.channel.id]
                        with open("./date/voicechannel.json", "w") as f:
                            json.dump(self.dates, f, indent=4)
            else:
                try:
                    after_text_channel = self.bot.get_channel(
                        self.dates[after.channel.id])
                    before_text_channel = self.bot.get_channel(
                        self.dates[before.channel.id])
                except KeyError:
                    pass
                else:
                    after_embed = discord.Embed(title='ボイスチャンネル入室通知',
                    description=f'{member.mention}さんが入室しました。',
                    color=0x00ff00)
                    before_embed = discord.Embed(title='ボイスチャンネル退出通知',
                    description=f'{member.mention}さんが退出しました。',
                    color=0xff0000)
                    await after_text_channel.send(embed=after_embed, delete_after=180)
                    await before_text_channel.send(embed=before_embed, delete_after=180)

　# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

    async def _channel_create(self, member):
        category = self.category
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
        voice_channel = await category.create_voice_channel(member.display_name, overwrites=overwrites)
        text_channel = await category.create_text_channel(member.display_name, overwrites=overwrites, position=3)
        self.dates[voice_channel.id] = text_channel.id
        with open("./date/voicechannel.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        embed = discord.Embed(title='ボイスチャンネル作成通知',
        description=f'{member.mention}さん、ようこそ！',
        color=0x0080ff)
        await text_channel.send(embed=embed, delete_after=180)
        member.move_to(voice_channel)

　# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――


def setup(airlinia):
    airlinia.add_cog(Voice_Channel(airlinia))
