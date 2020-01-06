# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import os # .env読み込みスターズ。

import requests
import ImageHash

class Discord_Game_Bot(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == 365975655608745985:  # ボットのメッセージをハネる
            e = message.embed
            if e.title == 'A wild pokémon has аppeаred!':
                r = requests.get(e.image.url)
                if r.status_code == 200:
                    hash = imagehash.dhash(Image.open(BytesIO(r.content)))
                    msg = json.load(open('./json/pokemon.json'))
                    await message.channel.send(msg) # 返信メッセージを送信

def setup(technetium):
    technetium.add_cog(Discord_Game_Bot(technetium))
