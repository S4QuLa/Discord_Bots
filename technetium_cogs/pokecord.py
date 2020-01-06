# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import os # .env読み込みスターズ。

import requests
import imagehash

class Discord_Game_Bot(commands.Cog):
    data = json.load(open('./json/pokemon.json'))

    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == 365975655608745985:  # ボットのメッセージをハネる
            e = message.embed
            if e.title == 'A wild pokémon has аppeаred!':
                print('pokecordのメッセージを検知')
                r = requests.get(e.image.url)
                if r.status_code == 200:
                    hash = imagehash.dhash(Image.open(BytesIO(r.content)))
                    await message.channel.send(f'このポケモン...もしかして「{self.data[hash]}」かなぁ。') # 返信メッセージを送信

def setup(technetium):
    technetium.add_cog(Discord_Game_Bot(technetium))
