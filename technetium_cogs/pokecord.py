# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import os # .env読み込みスターズ。
import json
import requests
import imagehash

class Discord_Game_Bot(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。
        self.json = open('./json/pokemon.json', 'r')
        self.data = json.load(self.json)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 365975655608745985 or not message.embeds:
            return
        e = message.embeds[0]
        if e.title == '\u200c\u200cA wild pokémon has аppeаred!':
            print('pokecordのメッセージを検知')
            r = requests.get(e.image.url)
            if r.status_code == 200:
                hash = imagehash.dhash(Image.open(BytesIO(r.content)))
                await message.channel.send(f'このポケモン...もしかして「{self.data[hash]}」かなぁ。') # 返信メッセージを送信
        else:
            print("pokecordのメッセージ（非判定）")

def setup(technetium):
    technetium.add_cog(Discord_Game_Bot(technetium))
