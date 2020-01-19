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
        if after.channel == None:
            return
   # -----------------------------
        if self.dates[after.chaneel.id] is not None:
            embed = discord.Embed(title='ボイスチャンネル入室通知',
            description=f'{member.mention}さんが入室しました。',
            color=0x2aa81e)
            await self.bot.get_channel(self.dates[after.chaneel.id]).send(embed=embed)
        if self.dates[before.chaneel.id] is not None:
            embed = discord.Embed(title='ボイスチャンネル退出通知',
            description=f'{member.mention}さんが退出しました。',
            color=0x660a0a)
            await self.bot.get_channel(self.dates[before.chaneel.id]).send(embed=embed)
            if before.chaneel.members is None:
                self.bot.get_channel(self.dates[before.chaneel.id]).delete()
                self.bot.get_channel(before.chaneel.id).delete()
                self.dates[channel_voice.id] = None
                with open("./date/voicechannel.json", "w") as f:
                    json.dump(self.dates, f, indent=4)
   # -----------------------------
        if after.channel.id == 655274902600941579:
            channel_text = await self._free_channel_create(member, member.display_name, VC=False)
            channel_voice = await self._free_channel_create(member, member.display_name, VC=True)
            self.dates[channel_voice.id] = channel_text.id
            with open("./date/voicechannel.json", "w") as f:
                json.dump(self.dates, f, indent=4)
            member.move_to(channel_voice)

    async def _free_channel_create(self, member, name, VC=False):
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
        if VC:
            channel = await category.create_voice_channel(name, overwrites=overwrites)
            return channel
        else:
            channel = await category.create_text_channel(name, overwrites=overwrites, position=3)
            return channel


def setup(airlinia):
    airlinia.add_cog(Voice_Channel(airlinia))
