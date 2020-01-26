import discord
from discord.ext import commands
import asyncio
import os
import re
import json

class Role_Panel(commands.Cog):  # 役職パネルの機能
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        # -----------
        with open('./date/rolepanel.json', 'r') as f:
            self.dates = json.load(f)

    @commands.group(aliases=["rp"])
    async def rolepanel(self, ctx):
        return

    @rolepanel.command(aliases=["rpaa", "alphaadd", "aa"])
    @commands.has_guild_permissions(administrator=True)
    async def _rolepanel_alpha_add(self, ctx, emoji, role: discord.Role, tag='通常'):
        def check(m):
            return (
                m.author == self.bot.user and m.embeds
                and tag in m.embeds[0].title
            )
        break1 = False
        history = await self.bot.get_channel(616530487229546518).history(oldest_first=True, limit=None)\
            .filter(check).flatten()
        for m in history:
            embed = m.embeds[0]
            description = embed.description
            lines = description.splitlines()
            for i in range(20):
                if emoji not in description:
                    new_lines = '\n'.join(
                        lines[0:i]
                        + ['{0}:{1}'.format(emoji, role.mention)]
                        + lines[i:len(lines) + 1]
                    )
                    embed.description = new_lines
                    await m.edit(embed=embed)
                    await m.add_reaction(emoji)
                    break1 = True
                    break
            if break1:
                break
        else:
            embed = discord.Embed(
                title='役職パネルα({1})({0}ページ目)'.format(len(history) + 1, tag),
                description='{1}:{0}'.format(role.mention, emoji),
                color=0x000000
            )
            m = await self.bot.get_channel(616530487229546518).send(embed=embed)
            await m.add_reaction(emoji)

    @rolepanel.command(aliases=["rpga", "gammaadd", "ga"])
    @commands.has_guild_permissions(administrator=True)
    async def _rolepanel_gamma_add(self, ctx, _message_id, emoji, role: discord.Role):
        self.dates[_message_id] = {}
        self.dates[_message_id][emoji] = role.id
        with open("./date/rolepanel.json", "w") as f:
            json.dump(self.dates, f, indent=4)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if user == self.bot.user: #自分のをハネる
            return
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

def setup(airlinia):
    airlinia.add_cog(Role_Panel(airlinia))
