# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os

import argparse

class Short_Url(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia

    @commands.command(name='url')
    async def _url(self, ctx, *, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('url')
        parser.add_argument('--password', '-p')
        parser.add_argument('--customurl', '-c')
        parser.add_argument('--domain', '-d', default='xn--gk8h.ml')
        args = parser.parse_args()
        payload = {}
        payload['target'] = args.url
        payload['domain'] = args.domain
        if customurl:
            payload['customurl'] = args.customurl
        if password:
            payload['password'] = args.password
        res = requests.post('https://kutt.it/api/v2/links', data=payload, headers=headers)
        data = res.json()
        await ctx.send(f"短縮URLを作成しました！{data['address']}") # 返信メッセージを送信

    @commands.command(name='domain')
    async def _urldomain(self, ctx, domain):
        payload = {}
        payload['address'] = domain

        res = requests.post('https://kutt.it/api/v2/domains', data=payload, headers=headers)
        data = res.json()
        await ctx.send(f"短縮URLのドメインに追加しました！{data['address']}") # 返信メッセージを送信

def setup(airlinia):
    airlinia.add_cog(Short_Url(airlinia))
