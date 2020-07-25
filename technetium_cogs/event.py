# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random

class Event(commands.Cog):
    def __init__(self, technetium):
        self.bot = technetium #botを受け取る。
        self.accent_color = (255, 210, 0)
        self.font_path = "./fonts/Harenosora.otf"
        self.bump_notice2.start()

    def cog_unload(self):
        self.bump_notice2.cancel()

    @tasks.loop(reconnect=True)
    async def bump_notice2(self):
        disboard_bot = self.bot.get_user(302050872383242240)
        channel = self.bot.get_channel(617960149067366410)
        mention = '<@&596668500916043796>'
        Interval = datetime.timedelta(hours=2)
        def check1(m):
            return m.author == disboard_bot and ':thumbsup:' in m.embeds[0].description
        mes = await channel.history().filter(check1).next()
        if mes is not None and "Bump canceled" not in channel.topic:
            timedata1 = datetime.datetime.utcnow() - mes.created_at
            if timedata1 >= Interval:
                embed1 = discord.Embed(title='⏫Bunp Reminder..!!!',
                description=f'Bumpされてから結構経ちましたよー。\r!d bumpをしてほしいんね。',
                color=0x0080ff)
                await channel.send(mention, embed=embed1)
            else:
                try:
                    # クライアントクローズか2時間経過するのを待つ
                    await asyncio.wait_for(
                        self.asyncio.Event(loop=self.bot.loop).wait(),
                        (Interval - timedata1).total_seconds()
                    )
                except asyncio.TimeoutError:
                    # 2時間経過
                    embed2 = discord.Embed(title='⏫Bunp Reminder!!!!!',
                    description=f'Bumpができますよー。\r!d bumpをしてほしいんね。',
                    color=0x0080ff)
                    await channel.send(mention, embed=embed2)
                else:
                    # クライアントクローズ
                    pass

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

    def add_base_image(self, icon_path, member_name, text2):
        icon_size = 160
        icon = Image.new("RGBA", ((icon_size + 30)*3, (icon_size + 30)*3), 0) #icon
        draw1 = ImageDraw.Draw(icon)
        draw1.ellipse((9*3, 9*3, (icon_size + 21)*3, (icon_size + 21)*3), fill="White") #縁取り
        draw1.ellipse((0, 0, (icon_size + 30)*3, (icon_size + 30)*3), width=3*3, outline="White") #周りの白抜きされた丸
        icon = icon.resize((icon_size + 30, icon_size + 30), Image.ANTIALIAS) #エイリアス

        mask = Image.new("L", (icon_size*3, icon_size*3), 0)
        draw2 = ImageDraw.Draw(mask)
        draw2.ellipse((0, 0, icon_size*3, icon_size*3), fill=255) #マスク用
        mask = mask.resize((icon_size, icon_size), Image.ANTIALIAS) #エイリアス

        icon_img = Image.open(BytesIO(requests.get(icon_path).content)).convert("RGBA").resize(size=(icon_size, icon_size), resample=Image.ANTIALIAS) #サイズ変更
        icon.paste(icon_img, ((icon.size[0]-icon_size)//2, (icon.size[0]-icon_size)//2), mask) #下地へ合成

        image = Image.open('./images/discord_cafe_welcome.png')
        image.paste(icon, ((image.size[0]-icon.size[0])//2, 200), icon) #背景と合成

        draw3 = ImageDraw.Draw(image)
        max_length = 550
        font1 = ImageFont.truetype(self.font_path, 30)
        font2 = ImageFont.truetype(self.font_path, 23)
        text1 = f"{member_name}さん"
        height = 430

        if draw3.textsize(text1, font=font1)[0] > max_length:
            while draw3.textsize(text1 + '…', font=font1)[0] > max_length:
                text1 = text1[:-1]
            text1 = text1[:-3] + '…さん'
        draw3.text(((image.size[0]-draw3.textsize(text1, font=font1))//2, 400), text1, "White", font=font1)
        for text in text2:
            draw3.text(((image.size[0]-draw3.textsize(text2, font=font2))//2, height), text, "White", font=font2)
            height += 24
        return image

    @commands.Cog.listener()
    async def on_member_join(self, member):
        image = self.add_base_image(member.avatar_url, member.name, [f"Welcome! #{len(member.guild.members)}"])
        arr = BytesIO()
        image.save(arr, format='png')
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
        image = self.add_base_image(member.avatar_url, member.name, [f"Goodbye. #{len(member.guild.members)}"])
        arr = BytesIO()
        image.save(arr, format='png')
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
