import discord
from discord.ext import commands
import asyncio
import os
import re

class Role_panel(commands.Cog):  # 役職パネルの機能
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.channel = self.bot.get_channel(616530487229546518)

    @commands.group(aliases=["rp"])
    async def rolepanel(self, ctx):
        return

    @rolepanel.command(aliases=["ea", "embedadd", "embed"])
    @rolepanel.has_permissions(manage_server=True)
    async def embed_add(self, ctx, title, content):
        embed = discord.Embed(title=title,
        description=content,
        color=0x0080ff)
        embed.set_footer(text='国際空創国家連合', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
        embed.set_author(name='役職パネル')
        panel = ctx.send(embed=embed)
        matchs1 = re.findall(r'(.|<:.*:(\d*)>):<@&(\d*)>', content)
        matchs2 = []
        for match in matchs1:
            if match.group(2) is None:
                matchs2.apped(match.group(1))
            else:
                matchs2.apped(match.group(2))
        for match in matchs2:
            await panel.reaction_add(match)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user: #自分のをハネる
            return
        message = reaction.message
        if message.channel == self.channel and message.author == self.client.user: #役職申請チャンネル且つメッセージがBot
            if '役職パネルα' in message.embeds[0].title:
                await message.remove_reaction(reaction, user) #取り消す
                match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                if match2:
                    role = message.guild.get_role(int(match2.group(1)))
                    if role not in user.roles:
                        await user.add_roles(role)
                        description = '{0}の役職を付与しました。'.format(role.mention)
                        await message.channel.send(
                            user.mention,
                            embed=discord.Embed(description=description),
                            delete_after=10
                        )
                    else:
                        await user.remove_roles(role)
                        description = '{0}の役職を解除しました'.format(role.mention)
                        await message.channel.send(
                            user.mention,
                            embed=discord.Embed(description=description),
                            delete_after=10
                        )
# --------------------------------------------------------------------------------------------------------
            elif '役職パネルβ' in message.embeds[0].title:
                match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                if match2:
                    role = message.guild.get_role(int(match2.group(1))) # Roleを取得
                    if role not in user.roles:
                        await user.add_roles(role)
                        description = '{0}の役職を付与しました。'.format(role.mention)
                        await message.channel.send(
                            user.mention,
                            embed=discord.Embed(description=description),
                            delete_after=10
                        )

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user == self.client.user: #自分のをハネる
            return
        message = reaction.message
        if message.channel == self.channel and message.author == self.client.user: #役職申請チャンネル且つメッセージがBot
            await message.remove_reaction(reaction, user) #取り消す
            if '役職パネルβ' in message.embeds[0].title:
                match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                if match2:
                    role = message.guild.get_role(int(match2.group(1))) # Roleを取得
                    if role in user.roles:
                        await user.remove_roles(role)
                        description = '{0}の役職を解除しました'.format(role.mention)
                        await message.channel.send(
                            user.mention,
                            embed=discord.Embed(description=description),
                            delete_after=10
                        )
