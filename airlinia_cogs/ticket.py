import discord
from discord.ext import commands
import asyncio
import os
import re
import traceback
import json

class Role_Panel(commands.Cog):  # 役職パネルの機能
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        # -----------
        with open('./date/airlinia_stats.json', 'r') as f:
            self.dates = json.load(f)

    @property
    def category(self):
        return self.bot.get_channel(668142017175617546)

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel: discord.TextChannel = self.bot.get_channel(655260036741988352)
        async for message in self.bot.get_channel(655260036741988352).history().filter(lambda m: m.author == self.bot.user):
            for reaction in message.reactions:
                async for user in reaction.users().filter(lambda u: u != self.bot.user):
                    self.bot.loop.create_task(message.remove_reaction(reaction, user))
            self.bot._connection._messages.append(message)

    @commands.group(aliases=["sp"])
    async def supportpanel(self, ctx):
        return

    @supportpanel.command(aliases=["spa", "spadd", "add"])
    @commands.has_guild_permissions(administrator=True)
    async def supportpanel_add(self, ctx, emoji, role: discord.Role, ticket):
        await self._supportpanel_add(emoji, role, ticket)

    async def _supportpanel_add(self, emoji, role, ticket):
        def check(m):
            return (
                m.author == self.bot.user and m.embeds
                and tag in m.embeds[0].title
            )
        break1 = False
        history = await self.bot.get_channel(655260036741988352).history(oldest_first=True, limit=None)\
            .filter(check).flatten()
        for m in history:
            embed = m.embeds[0]
            description = embed.description
            lines = description.splitlines()
            for i in range(20):
                if emoji not in description:
                    new_lines = '\n'.join(
                        lines[0:i]
                        + ['{0}:{1}{2}'.format(emoji, role.mention, ticket)]
                        + lines[i:len(lines) + 1]
                    )
                    embed.description = new_lines
                    embed.color = 0xfefefe
                    await m.edit(embed=embed)
                    await m.add_reaction(emoji)
                    break1 = True
                    break
            if break1:
                break
        else:
            embed = discord.Embed(
                title='サポートチケット￤Support Ticket',
                description='{0}:{1}{2}'.format(emoji, role.mention, ticket),
                color=0xfefefe
            )
            embed.set_footer(text='サポートチケット', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
            m = await self.bot.get_channel(655260036741988352).send(embed=embed)
            await m.add_reaction(emoji)

    async def _channel_create(self, name, member, ticket_role, ticket_category):
        category = self.category
        guild = member.guild
        role_1 = category.guild.get_role(654943500193890310)
        position = self.bot.get_channel(670849143530586173).position + 1
        overwrites = {
            self.bot.user:
                discord.PermissionOverwrite.from_pair(discord.Permissions.all(), discord.Permissions.none()),
            guild.default_role:
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            guild.get_role(635149066795483137): #ミュート。
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            guild.get_role(655254335030034442): #本部役員
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129)),
            ticket_role: #閲覧できる役職
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129)),
            member:
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129))
        }
        text_channel = await guild.create_text_channel(name, topic=f'{ticket_category} - {member.id}', overwrites=overwrites, category=category, position=position)
        return text_channel

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if user == self.bot.user: #自分のをハネる
            return
        if message.channel.id == 655260036741988352 and message.author == self.bot.user: #役職申請チャンネル且つメッセージがBot
            if 'サポートチケット' in message.embeds[0].title:
                await message.remove_reaction(reaction, user) #取り消す
                try:
                    match2 = re.search(reaction.emoji + r':<@&(\d*)>(.*)', message.embeds[0].description) #取り出す
                except TypeError:
                    emoji_text = f"<:{reaction.emoji.name}:{reaction.emoji.id}>"
                    match2 = re.search(emoji_text + r':<@&(\d*)>(.*)', message.embeds[0].description)
                x = False
                if match2:
                    ticket_role = message.guild.get_role(int(match2.group(1)))
                    ticket_category = int(match2.group(2))
                    for self.category.text_channels in channel:
                        if user.id in channel.topic: #もう開いてる？
                            embed = discord.Embed(description='別のチケットが開かれています。チケットを閉じてから新しく開いてください。', color=0xffff00)
                            embed.set_footer(text='サーバーチケット', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                            await message.channel.send(user.mention, embed=embed, delete_after=10)
                            x = True
                    if x == False:
                        self.dates["ticket_number"] += 1
                        with open("./date/airlinia_stats.json", "w") as f:
                            json.dump(self.dates, f, indent=4)
                        name = f'ticket-{self.dates["ticket_number"].zfill(3)}_open'
                        channel = await self._channel_create(self, name, user.name, ticket_role, ticket_category)
                        embed = discord.Embed(description=f'{member.mention}さん、ようこそ。',color=0x0080ff)
                        embed.set_footer(text='Iufs Support - Airlinia', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                        await channel.send(content=f'{member.mention}、{ticket_role.mention}', embed=embed)


def setup(airlinia):
    airlinia.add_cog(Role_Panel(airlinia))
