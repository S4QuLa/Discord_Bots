# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio
import os # .env読み込みスターズ。

import datetime

class Free_Category(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @property
    def category(self):
        return self.bot.get_channel(655411710244552714)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        if message.channel.id == 663288946494537758:
            name = message.content
            embed = discord.Embed(title='🗃️チャンネルを作成しますか？',
            description=f'チャンネル名:{name}\n\n✅：チャンネルを作成します。\n❎：チャンネルの作成をキャンセルします。\n（15秒反応がない場合、自動的にキャンセルします。）',
            color=0x0080ff)
            embed.set_author(name=f'{name} - 作成許可待ちです。',icon_url='https://i.imgur.com/yRCJ26G.gif')

            embed_no = discord.Embed(title='🗃️🚫チャンネル作成をキャンセルしました。',
            description=f'チャンネル名:{name}',
            color=0xff0000)
            embed_no.set_author(name=f'{name} - 作成をキャンセルしました。',icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQLFHFV5AuInaxeSHFkAtvJV-HT3xa6Ua7M61pXgsADOC6Y0Czj',url="https://airlinia.ml")

            msg = await message.channel.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❎')

            try:
                def check(r, u):
                    return (
                            r.me and message.author == u
                            and r.message.id == message.id
                            and r.message.channel == message.channel
                    )
                react = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                if react[0].emoji == '✅':
                    channel = await self._free_channel_create(message, message.content, VC=False)
                    if channel is not None:
                        nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d %H:%M:%S')
                        embed_ok = discord.Embed(title='🗃️チャンネルを作成しました！',
                        description=f'チャンネル名:{name}\nチャンネル作成先：{channel.mention}\n現在時刻：{nowtime}\n残りチャンネル作成可能数：{50 - len(channel.category.channels)}',
                        color=0x00ff00)
                        embed_ok.set_author(name=f'{name} - 作成しました。',icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSkiyk4R_ppUp-6qcfobj3OI9eEEdwxFTQocIy6aZ0jQ27zhMhq',url="https://airlinia.ml")
                        await msg.edit(embed=embed_ok)
                        await msg.clear_reactions()
                elif react[0].emoji == '❎':
                    await msg.edit(embed=embed_no)
                    await msg.clear_reactions()
            except asyncio.TimeoutError:
                await msg.edit(embed=embed_no)
                await msg.clear_reactions()

    async def _free_channel_create(self, message, name, VC=False):
        category = self.category
        if len(category.channels) >= 50:
            await ctx.send(textwrap.dedent(
            """
            チャンネルが一杯でこのカテゴリには作成できません。
            """
            ))
            return

        overwrites = {
            self.bot.user:
                discord.PermissionOverwrite.from_pair(discord.Permissions.all(), discord.Permissions.none()),
            message.author:
                discord.PermissionOverwrite.from_pair(discord.Permissions(66448721), discord.Permissions.none()),
            category.guild.default_role:
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            category.guild.get_role(635149066795483137): #ミュート。
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            category.guild.get_role(655412328052949012): #閲覧できる役職
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129)),
        }
        if VC:
            channel = await category.create_voice_channel(name, overwrites=overwrites)
            return channel
        else:
            channel = await category.create_text_channel(name, overwrites=overwrites)
            return channel

def setup(airlinia):
    airlinia.add_cog(Free_Category(airlinia))
