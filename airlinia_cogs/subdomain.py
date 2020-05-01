# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio

import os
from cloudflare_ddns import CloudFlare
import argparse

class Sub_Domain(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia
        self.cf = CloudFlare("amazakura0804@gmail.com", os.environ["CLOUDFLARE_API_KEY"], "iufs.jp")
        self.cf.sync_dns_from_my_ip()

    @commands.command(name='url')
    async def _url(self, ctx, sub_domain, ip_address):
        res = requests.post('https://kutt.it/api/v2/links', data=payload, headers=headers)
        cf.create_record('A', sub_domain+".gov.iufs.jp", ip_address)
        await ctx.send(f'短縮URLを作成しました！{data["link"]}') # 返信メッセージを送信

def setup(airlinia):
    airlinia.add_cog(Sub_Domain(airlinia))
