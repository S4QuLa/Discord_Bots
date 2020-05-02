# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import json

import random

class Event(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.bump_notice1.start()

    def cog_unload(self):
        self.bump_notice1.cancel()

    @tasks.loop(reconnect=True)
    async def bump_notice1(self):
        disboard_bot = self.bot.get_user(302050872383242240)
        channel = self.bot.get_channel(655399719971061802)
        mention = '<@&617326967368187944>'
        Interval = datetime.timedelta(hours=2)
        def check1(m):
            return m.author == disboard_bot and ':thumbsup:' in m.embeds[0].description
        mes = await channel.history().filter(check1).next()
        if mes is not None and "Bump canceled" not in channel.topic:
            timedata1 = datetime.datetime.utcnow() - mes.created_at
            if timedata1 >= Interval:
                embed1 = discord.Embed(title='⏫Bunp Reminder..!!!',
                description=f'Bumpされてから結構経ちましたよー。\r!d bumpをしてほしいんね。',
                color=0x0080ff)
                await channel.send(mention, embed=embed1)
            else:
                try:
                    # クライアントクローズか2時間経過するのを待つ
                    await asyncio.wait_for(
                        self.asyncio.Event(loop=self.bot.loop).wait(),
                        (Interval - timedata1).total_seconds()
                    )
                except asyncio.TimeoutError:
                    # 2時間経過
                    embed2 = discord.Embed(title='⏫Bunp Reminder!!!!!',
                    description=f'Bumpができますよー。\r!d bumpをしてほしいんね。',
                    color=0x0080ff)
                    await channel.send(mention, embed=embed2)
                else:
                    # クライアントクローズ
                    pass

    @bump_notice1.before_loop
    async def before_bump_notice1(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cl = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(title=f"利用規約はここから",
                              description=f"{member.guild.name}へようこそ！{member.mention}さん！\n{len(member.guild.members)}人目の参加者です！\n> 何か困ったことがあればぜひとも運営にメンションをしてください。\n> 基本一人は常駐してます。",
                              url="https://www.elegraph.cf/?page_id=24",
                              color=cl)
        embed.set_author(name=f"{member.display_name}さんが参加しました～！")
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.get_channel(596668568909643817).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title=f"さようなら。",
                              description=f"{member.display_name}さん、さようなら。\n現在、このサーバーには{len(member.guild.members)}人がいます。",)
        embed.set_author(name=f"{member.display_name}さんが退出されました。")
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.get_channel(596668568909643817).send(embed=embed)

def setup(technetium):
    technetium.add_cog(Event(technetium))
