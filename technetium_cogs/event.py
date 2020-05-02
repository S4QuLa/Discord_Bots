# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import os # .env読み込みスターズ。
import json

from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random

class Event(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。
        self.accent_color = (255, 210, 0)
        self.font_path1 = "./fonts/NotoSansCJKjp-Medium.otf"
        self.font_path2 = "./fonts/Harenosora.otf"
        self.bump_notice2.start()

    def cog_unload(self):
        self.bump_notice2.cancel()

    @tasks.loop(minutes=1.0, reconnect=True)
    async def bump_notice2(self):
        disboard_bot = self.bot.get_user(302050872383242240)
        channel = self.bot.get_channel(617960149067366410)
        mention = '<@&596668500916043796>'
        Interval = datetime.timedelta(hours=2)
        def filter1(m):
            return m.author == disboard_bot and ':thumbsup:' in m.embeds[0].description

        mes = await channel.history().filter(filter1).next()
        if mes is not None and "Bump canceled" in channel.topic:
            timedata1 = datetime.datetime.utcnow() - mes.created_at
            if timedata1 >= Interval:
                embed1 = discord.Embed(title='⏫Bunp Reminder..!!!',
                description=f'Bumpされてから結構経ちましたよー。\r!d bumpをしてほしいんね。',
                color=0x0080ff)
                await channel.send(mention, embed=embed1)
            else:
                embed2 = discord.Embed(title='⏫Bunp Reminder!!!!!',
                description=f'Bumpができますよー。\r!d bumpをしてほしいんね。',
                color=0x0080ff)
                await channel.send(mention, embed=embed2)

    @bump_notice2.before_loop
    async def before_bump_notice2(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            after.channel is not None
            and (before.channel is None or before.channel != after.channel)
        ):
            embed = discord.Embed(title='ボイスチャンネル入室通知',
            description=f'{member.mention}さんが入室しました。',
            color=0x00ff00)
            await self.bot.get_channel(596668583728119809).send(embed=embed, delete_after=180)

        if (
            before.channel is not None
            and (after.channel is None or before.channel != after.channel)
        ):
            embed = discord.Embed(title='ボイスチャンネル退出通知',
            description=f'{member.mention}さんが退出しました。',
            color=0xff0000)
            await self.bot.get_channel(596668583728119809).send(embed=embed, delete_after=180)

    def add_base_image(self, icon_path):
        icon_size = 380
        mask = Image.new("L", (icon_size, icon_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, icon_size, icon_size), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(1))

        icon = Image.open(BytesIO(requests.get(icon_path).content)).convert("RGBA")
        icon = icon.resize(size=(icon_size, icon_size), resample=Image.ANTIALIAS)
        circle = Image.new("RGBA", (icon_size + 10, icon_size + 10), 0)

        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, icon_size + 10, icon_size + 10), self.accent_color)
        circle.paste(icon, (5, 5), mask)

        base_image = Image.open('./image/elegraph_welcome.png')
        base_image.paste(circle, (100, 220), circle)
        draw = ImageDraw.Draw(base_image)
        draw.line([(320,608), (1920,608)], self.accent_color, width=5)
        draw.polygon(((0, 0), (250, 0), (0, 200)), fill=self.accent_color)
        return base_image

    def add_text_to_image(self, img, text, font_path, font_size, font_color, height, width, max_length=1400):
        position = (width, height)
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(img)
        if draw.textsize(text, font=font)[0] > max_length:
            while draw.textsize(text + '…', font=font)[0] > max_length:
                text = text[:-1]
            text = text[:-3] + '… さん！'
        draw.text(position, text, font_color, font=font)
        return img

    @commands.Cog.listener()
    async def on_member_join(self, member):
        img = self.add_base_image(member.avatar_url)
        _text = []
        _text.append(["ようこそ！Welcome!", self.font_path1, 130, self.accent_color, 190, 530])
        _text.append([f"{member.name} さん！", self.font_path2, 50, (255, 255, 255), 350, 530])
        _text.append([f"ようこそ、{member.guild.name}へ！\n最初にルールをお読みください。\nあなたは{len(member.guild.members)}人目のメンバーです！", self.font_path2, 55, (255, 255, 255), 440, 530])
        for t in _text:
            img = self.add_text_to_image(img, t[0], t[1], t[2], t[3], t[4], t[5])

        arr = BytesIO()
        img.save(arr, format='png')
        arr.seek(0)
        file = discord.File(fp=arr, filename="Welcome_image.png")
        cl = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(title=f"利用規約はここから",
                              description=f"{member.guild.name}へようこそ！{member.mention}さん！\n{len(member.guild.members)}人目の参加者です！\n> 何か困ったことがあればぜひとも運営にメンションをしてください。\n> 基本一人は常駐してます。",
                              url="https://www.elegraph.cf/?page_id=24",
                              color=cl)
        embed.set_author(name=f"{member.display_name}さんが参加しました～！", icon_url=member.avatar_url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="attachment://Welcome_image.png")
        await self.bot.get_channel(596668568909643817).send(file=file, embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        img = self.add_base_image(member.avatar_url)
        _text = []
        _text.append(["さようなら｡Goodbye.", self.font_path1, 130, self.accent_color, 190, 500])
        _text.append([f"{member.name}さん", self.font_path2, 50, 'White', 370, 540])
        _text.append([f"さようなら。\n現在、{member.guild.name}には\n{len(member.guild.members)}人のメンバーがいます。", self.font_path2, 55, 'White', 445, 530])
        for t in _text:
            img = self.add_text_to_image(img, t[0], t[1], t[2], t[3], t[4], t[5])

        arr = BytesIO()
        img.save(arr, format='png')
        arr.seek(0)
        file = discord.File(fp=arr, filename="Goodbye_image.png")
        embed = discord.Embed(title=f"さようなら。",
                              description=f"{member.display_name}さん、さようなら。\n現在、このサーバーには{len(member.guild.members)}人がいます。",)
        embed.set_author(name=f"{member.display_name}さんが退出されました。", icon_url=member.avatar_url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="attachment://Goodbye_image.png")
        await self.bot.get_channel(596668568909643817).send(file=file, embed=embed)

def setup(technetium):
    technetium.add_cog(Event(technetium))
