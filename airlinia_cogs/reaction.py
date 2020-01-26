# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

class Reaction(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji.id == 670860075736236032: # Retweet
            embed_retweet = discord.Embed(title=f'Retweet!',
            description=f'{reaction.message.content}',
            color=0x0080ff)
            embed_retweet.set_footer(text=f"{user.display_name} - {user.id}", icon_url=user.avatar_url)
            embed_retweet.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar_url)
            embed_retweet.set_thumbnail(url=reaction.message.author.avatar_url)
            if len(reaction.message.attachments) > 0:
                embed_retweet.set_image(url=reaction.message.attachments[0].url)
            reaction.message.channel.send(embed=embed_retweet)
            self.bot.get_channel(670589954765750294).send(embed=embed_retweet)
        #if reaction.emoji.id == 670860096028409879: # いいね
        #if reaction.emoji.id == 670860076327632908: # ブックマーク
        if reaction.message.channel.category_id == 668142017175617546 or reaction.message.channel.category_id == 668374572080562177:
            if reaction.emoji.id == 665462194116493313:
                members = [reaction.message.author, user]
                channel = await self._channel_create(reaction.message.channel.category, members, "Thread")
                embed_1 = discord.Embed(title='チャンネル作成しました。',
                description=f'{channel.mention}\rスレッドを作成しました。',
                color=0x0080ff)
                await reaction.message.channel.send(embed=embed_1, content=f"{user.mention}、{reaction.message.author.mention}")

                embed_2 = discord.Embed(description=f'{reaction.message.content}',
                color=0x0080ff)
                embed_2.set_footer(text="国際空創国家連合", icon_url="https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif")
                embed_2.set_author(name=user.display_name, icon_url=user.avatar_url)
                embed_2.set_thumbnail(url=reaction.message.author.avatar_url)
                if len(reaction.message.attachments) > 0:
                    embed_2.set_image(url=reaction.message.attachments[0].url)
                await channel.send(embed=embed_2, content=f"{user.mention}、{reaction.message.author.mention}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji.id == 670860075736236032: # Retweet
            for message in reaction.message.channel.Messageable.history(limit=None):
                if len(reaction.message.embeds) > 0:
                    if (
                        message.embeds[0].description == reaction.message.content
                        and message.embeds[0].footer.text in f"{user.id}"
                    ):
                        message.delete()
                        break
            for message in self.bot.get_channel(670589954765750294).Messageable.history(limit=None):
                if len(reaction.message.embeds) > 0:
                    if (
                        message.embeds[0].description == reaction.message.content
                        and message.embeds[0].footer.text in f"{user.id}"
                    ):
                        message.delete()
                        break

    async def _channel_create(self, category, members, name):
        overwrites = {
            self.bot.user:
                discord.PermissionOverwrite.from_pair(discord.Permissions.all(), discord.Permissions.none()),
            category.guild.default_role:
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            members[0]:
                discord.PermissionOverwrite.from_pair(discord.Permissions(66448721), discord.Permissions.none()),
            members[1]:
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
    airlinia.add_cog(Reaction(airlinia))
