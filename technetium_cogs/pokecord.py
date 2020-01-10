# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import os # .env読み込みスターズ。

import json
from io import BytesIO
from PIL import Image
import imagehash

import schedule
import requests

class Discord_Game_Bot(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。

    @commands.command(name='pokemon')
    async def pokemon_image(self, ctx, *, arg):
        r = requests.get(arg)
        if r.status_code == 200:
            hash = str(imagehash.dhash(Image.open(BytesIO(r.content))))
            date = json.load(open('./date/pokemon.json', 'r'))

            pokemon = date.get(hash, '...ごめん、わからん')
            await message.channel.send(f'このポケモン...もしかして「{pokemon}」かなぁ。\r ```command : p!catch {pokemon}```')

    @commands.command(name='hash')
    async def pokemon_hash(self, ctx, *, arg):
        r = requests.get(arg)
        if r.status_code == 200:
            hash = str(imagehash.dhash(Image.open(BytesIO(r.content))))
            await ctx.message.channel.send(f'この画像のhashは「{hash}」だよ～ん。') # 返信メッセージを送信

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 365975655608745985 or not message.embeds:
            return
        e = message.embeds[0]
        if e.title == '\u200c\u200cA wild pokémon has аppeаred!':
            print('pokecordのメッセージを検知')
            r = requests.get(e.image.url)
            if r.status_code == 200:
                hash = str(imagehash.dhash(Image.open(BytesIO(r.content))))
                date = json.load(open('./date/pokemon.json', 'r'))

                pokemon = date.get(hash, '...ごめん、わからん')
                await message.channel.send(f'このポケモン...もしかして「{pokemon}」かなぁ。\r ```command : p!catch {pokemon}```')
        else:
            print("pokecordのメッセージ（非判定）")

def setup(technetium):
    technetium.add_cog(Discord_Game_Bot(technetium))
