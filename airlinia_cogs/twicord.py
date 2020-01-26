# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

class Twicord(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji.id == 670860075736236032: # Retweet
            embed_retweet = discord.Embed(title=f'Retweet!',
            url=reaction.message.jump_url,
            description=reaction.message.content,
            color=0x0080ff)
            embed_retweet.set_footer(text=f'{user.display_name} - {user.id}', icon_url=user.avatar_url)
            embed_retweet.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar_url)
            embed_retweet.set_thumbnail(url=reaction.message.author.avatar_url)
            if len(reaction.message.attachments) > 0:
                embed_retweet.set_image(url=reaction.message.attachments[0].url)
            await self.bot.get_channel(670589954765750294).send(embed=embed_retweet)
            if user.permissions_in(reaction.message.channel).send_messages:
                await reaction.message.channel.send(embed=embed_retweet)
        #if reaction.emoji.id == 670860096028409879: # いいね
        #if reaction.emoji.id == 670860076327632908: # ブックマーク

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji.id == 670860075736236032: # Retweet
            async for message in reaction.message.channel.history(limit=None, after=reaction.message.created_at):
                if len(message.embeds) > 0:
                    if (
                        message.embeds[0].description == reaction.message.content
                        and str(user.id) in message.embeds[0].footer.text
                    ):
                        await message.delete()
                        break
            async for message in self.bot.get_channel(670589954765750294).history(limit=None, after=reaction.message.created_at):
                if len(message.embeds) > 0:
                    if (
                        message.embeds[0].description == reaction.message.content
                        and str(user.id) in message.embeds[0].footer.text
                    ):
                        await message.delete()
                        break

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        for reaction in message.reactions:
            if reaction.emoji.id == 670860075736236032:
                async for _message in message.channel.history(limit=None, after=reaction.message.created_at):
                    if len(_message.embeds) > 0 and _message.embeds[0].description == reaction.message.content:
                            await _message.delete()
                async for _message in self.bot.get_channel(670589954765750294).history(limit=None, after=reaction.message.created_at):
                    if len(_message.embeds) > 0 and _message.embeds[0].description == reaction.message.content:
                            await _message.delete()

def setup(airlinia):
    airlinia.add_cog(Twicord(airlinia))
