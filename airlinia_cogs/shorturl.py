# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os
from kutt import kutt

class Short_Url(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia

    @commands.command()
    async def url(self, ctx, url1, pass):
        obj = kutt.submit(os.environ['KUTT_API_KEY'], url1, password=pass, customurl="xn--gk8h.ml")
        await message.channel.send(f"短縮URLを作成しました！{obj['address']}") # 返信メッセージを送信

def setup(airlinia):
    airlinia.add_cog(Short_Url(airlinia))
