# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os

import argparse
from kutt import kutt

class Short_Url(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia

    @commands.command(name='url')
    async def _url(self, ctx, *, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('url')
        parser.add_argument('--password', '-p')
        parser.add_argument('--customurl', '-c')
        args = parser.parse_args()
        obj = kutt.submit(os.environ['KUTT_API_KEY'], args.url, customurl=args.customurl, password=args.password, customurl="xn--gk8h.ml")
        await ctx.send(f"短縮URLを作成しました！{obj['address']}") # 返信メッセージを送信

def setup(airlinia):
    airlinia.add_cog(Short_Url(airlinia))
