# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os
from kutt import kutt

class Short_Url(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia

    @commands.command(name='url')
    async def _url(self, ctx, url, pass):
        obj = kutt.submit(os.environ['KUTT_API_KEY'], url, password=pass, customurl="xn--gk8h.ml")
        await ctx.send(f"短縮URLを作成しました！{obj['address']}") # 返信メッセージを送信

def setup(airlinia):
    airlinia.add_cog(Short_Url(airlinia))
