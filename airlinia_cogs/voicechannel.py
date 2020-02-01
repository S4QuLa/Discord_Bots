# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json

def reaction(message, author, bot):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user or author != user:
            return False
        if reaction.emoji == '✅' or reaction.emoji == '❎':
            return True
    return check

class Voice_Channel(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。🔐🔏🔓✅❌🎟✒
        # -----------
        with open('./date/voicechannel.json', 'r') as f:
            self.dates = json.load(f)

    @property
    def category(self):
        return self.bot.get_channel(655274860708364288)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            after.channel is not None
            and (before.channel is None or before.channel != after.channel)
        ):
            if after.channel.id == 655274902600941579:
                await self._channel_create(member)
            else:
                try:
                    text_channel = self.bot.get_channel(self.dates[after.channel.id]["id"])
                except KeyError:
                    pass
                else:
                    embed = discord.Embed(title='ボイスチャンネル入室通知',
                    description=f'{member.mention}さんが入室しました。',
                    color=0x00ff00)
                    await text_channel.send(embed=embed, delete_after=180)

        if (
            before.channel is not None
            and (after.channel is None or before.channel != after.channel)
        ):
            try:
                text_channel = self.bot.get_channel(self.dates[before.channel.id]["id"])
            except KeyError:
                pass
            else:
                embed = discord.Embed(title='ボイスチャンネル退出通知',
                description=f'{member.mention}さんが退出しました。',
                color=0xff0000)
                await text_channel.send(embed=embed, delete_after=180)
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    await text_channel.delete()
                    del self.dates[before.channel.id]
                    with open("./date/voicechannel.json", "w") as f:
                        json.dump(self.dates, f, indent=4)

 # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

    async def _channel_create(self, member):
        category = self.category
        guild = member.guild
        position = self.bot.get_channel(670473107269746718).position - 1
        overwrites = {
            self.bot.user:
                discord.PermissionOverwrite.from_pair(discord.Permissions.all(), discord.Permissions.none()),
            category.guild.default_role:
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            category.guild.get_role(635149066795483137): #ミュート。
                discord.PermissionOverwrite.from_pair(discord.Permissions.none(), discord.Permissions.all()),
            category.guild.get_role(617017694306435073): #閲覧できる役職
                discord.PermissionOverwrite.from_pair(
                    discord.Permissions(37080128), discord.Permissions(2 ** 53 - 37080129)),
        }
        text_channel = await guild.create_text_channel(member.display_name, overwrites=overwrites, category=category, position=position)
        voice_channel = await guild.create_voice_channel(member.display_name, overwrites=overwrites, category=category)
        self.dates[voice_channel.id] = {}
        self.dates[voice_channel.id]["id"] = text_channel.id
        self.dates[voice_channel.id]["owner"] = member.id
        with open("./date/voicechannel.json", "w") as f:
            json.dump(self.dates, f, indent=4)
        embed = discord.Embed(title='ボイスチャンネル作成通知',
        description=f'{member.mention}さん、ようこそ！',
        color=0x0080ff)
        await text_channel.send(content=member.mention, embed=embed)
        await member.move_to(voice_channel)

 # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

    @commands.group()
    async def voice(self, ctx):
        if message.author.bot:  # ボットのメッセージをハネる
            return
        embed = discord.Embed(title='🗃️チャンネルを作成しますか？',
        description=f'チャンネル名:{name}\n\n✅：チャンネルを作成します。\n❎：チャンネルの作成をキャンセルします。\n（15秒反応がない場合、自動的にキャンセルします。）',
        color=0x0080ff)
        embed.set_author(name=f'{name} - 作成許可待ちです。',icon_url='https://i.imgur.com/yRCJ26G.gif')
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')
        try:
            react = await self.bot.wait_for('reaction_add', timeout=15, check=reaction(msg, message.author, self.bot))
            if react[0].emoji == '✅':
                channel = await self._free_channel_create(message, message.content, VC=False)
                if channel is not None:
                    nowtime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d %H:%M:%S')
                    embed_ok = discord.Embed(title='🗃️チャンネルを作成しました！',
                    description=f'チャンネル名:{name}\nチャンネル作成先：{channel.mention}\n現在時刻：{nowtime}\n残りチャンネル作成可能数：{50 - len(channel.category.channels)}',
                    color=0x00ff00)
                    embed_ok.set_author(name=f'{name} - 作成しました。',icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSkiyk4R_ppUp-6qcfobj3OI9eEEdwxFTQocIy6aZ0jQ27zhMhq',url="https://airlinia.ml")
                    await msg.edit(embed=embed_ok)
                    await msg.clear_reactions()
            elif react[0].emoji == '❎':
                await msg.edit(embed=embed_no)
                await msg.clear_reactions()
        except asyncio.TimeoutError:
            await msg.edit(embed=embed_no)
            await msg.clear_reactions()

    @voice.command()
    async def lock(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            role = ctx.guild.get_role(617017694306435073)
            await channel.set_permissions(role, connect=False, speak=False, send_messages=False, read_message_history=False, read_messages=False)
            await text_channel.set_permissions(role, connect=False, speak=False, send_messages=False, read_message_history=False, read_messages=False)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'{ctx.author.mention}さん、チャンネルをロックしました！🔐',
            color=0xffff00)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command()
    async def view_only(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            role = ctx.guild.get_role(617017694306435073)
            await channel.set_permissions(role, connect=True, speak=False, read_message_history=True, read_messages=True, send_messages=False)
            await text_channel.set_permissions(role, connect=True, speak=False, read_message_history=True, read_messages=True, send_messages=False)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'{ctx.author.mention}さん、チャンネルを閲覧限定にしました！🔏',
            color=0xffff00)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command()
    async def unlock(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            role = ctx.guild.get_role(617017694306435073)
            await channel.set_permissions(role, connect=True, speak=True, read_message_history=True, read_messages=True, send_messages=True)
            await text_channel.set_permissions(role, connect=True, speak=True, read_message_history=True, read_messages=True, send_messages=True)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'{ctx.author.mention}さん、チャンネルをアンロックしました！🔓',
            color=0xffff00)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command(aliases=["allow"])
    async def permit(self, ctx, member : discord.Member):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            await channel.set_permissions(member, connect=True, speak=True, read_message_history=True, read_messages=True, send_messages=True)
            await text_channel.set_permissions(member, connect=True, speak=True, read_message_history=True, read_messages=True, send_messages=True)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'{member.mention}さん、ようこそ。✅',
            color=0x00ff00)
            await ctx.send(content=f"{ctx.author.mention}、{member.mention}", embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command(aliases=["deny"])
    async def reject(self, ctx, member : discord.Member):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            await channel.set_permissions(member, connect=False, speak=False, read_message_history=False, send_messages=False, read_messages=False)
            await text_channel.set_permissions(member, connect=False, speak=False, read_message_history=False, send_messages=False, read_messages=False)
            await member.move_to(self.bot.get_channel(655272738952314908))
            embed_1 = discord.Embed(title='Channel Moderate!',
            description=f'{member.name}さんをつまみ出しました。❌',
            color=0xff0000)
            embed_2 = discord.Embed(title='Your Reject.',
            description=f'{member.mention}さん、あなたはつまみ出されました。❌',
            color=0xff0000)
            await ctx.send(content=f"{ctx.author.mention}", embed=embed_1)
            await member.send(embed=embed_2)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command()
    async def limit(self, ctx, limit):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            await channel.edit(user_limit = limit)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'参加人数を{limit}人に制限しました。🎟',
            color=0xffffff)
            await ctx.send(content=f"{ctx.author.mention}", embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command()
    async def name(self, ctx, *, name):
        channel = ctx.author.voice.channel
        if ctx.author.id == self.dates[channel.id]["owner"]:
            text_channel = self.bot.get_channel(self.dates[channel.id]["id"])
            await channel.edit(name = name)
            await text_channel.edit(name = name)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'チャンネル名を{name}に変更しました！✒',
            color=0xffffff)
            await ctx.send(content=f"{ctx.author.mention}", embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command()
    async def claim(self, ctx):
        channel = ctx.author.voice.channel
        if self.dates[channel.id] is not None:
            owner = ctx.guild.get_member(self.dates[channel.id]["id"])
            x = False
            for member in channel.members:
                if member.id == self.dates[channel.id]["owner"]:
                    await ctx.send(content=f"とっくにオーナーさんいるやないですか。")
                    x = True
            if x == False:
                self.dates[channel.id]["owner"] = ctx.author.id
                with open("./date/voicechannel.json", "w") as f:
                    json.dump(self.dates, f, indent=4)
                embed = discord.Embed(title='Channel Moderate!',
                description=f'{ctx.author.mention}さん、あなたが今ここのオーナーです。',
                color=0x80ff00)
                await ctx.send(content=ctx.author.mention, embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

def setup(airlinia):
    airlinia.add_cog(Voice_Channel(airlinia))
