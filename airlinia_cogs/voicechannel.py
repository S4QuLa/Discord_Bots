# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio

import os # .env読み込みスターズ。
import json
import pymongo

class Voice_Channel(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        mongo_connection = pymongo.MongoClient("ds161505.mlab.com", 61505, retryWrites=False)
        mongo_db = mongo_connection["heroku_stfrs35p"]
        mongo_db.authenticate("heroku_stfrs35p", os.environ['MONGODB_PASSWORD'])
        self.mongo_coll = mongo_db['voicechannel']
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})

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
                    text_channel = self.bot.get_channel(self.datas[after.channel.id]["id"])
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
                text_channel = self.bot.get_channel(self.datas[before.channel.id]["id"])
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
                    del self.datas[before.channel.id]
                    self.mongo_coll.update_one({"server": 615849898637656093}, {'$set':self.datas})

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
        self.datas["channel_data"][str(voice_channel.id)] = {}
        self.datas["channel_data"][str(voice_channel.id)]["id"] = text_channel.id
        self.datas["channel_data"][str(voice_channel.id)]["owner"] = member.id
        self.mongo_coll.update_one({"server": 615849898637656093}, {'$set':self.datas})
        embed = discord.Embed(title='ボイスチャンネル作成通知',
        description=f'{member.mention}さん、ようこそ！',
        color=0x0080ff)
        await text_channel.send(content=member.mention, embed=embed)
        await member.move_to(voice_channel)

    @commands.group()
    async def voice(self, ctx):
        if ctx.author.bot:  # ボットのメッセージをハネる
            return
        embed = discord.Embed(title='💻チャンネル編集',
        description=f'🔐チャンネルロック\n🔏チャンネル閲覧限定／解除\n🔓チャンネルロック\n✅招待\n❎キック\n🎟人数制限\n✒名前変更\n💻オーナー継承\n🚫キャンセル',
        color=0x0080ff)
        embed.set_author(name=f'{name} - 編集しちゃお！',icon_url='https://i.imgur.com/yRCJ26G.gif')
        embed_no = discord.Embed(title='💻🚫チャンネル編集をキャンセル',
        description=f'チャンネルの編集をキャンセルしたよ。',
        color=0xff0000)
        embed_no.set_author(name=f'{name} - 編集せんのかーい。',icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQLFHFV5AuInaxeSHFkAtvJV-HT3xa6Ua7M61pXgsADOC6Y0Czj',url="https://airlinia.ml")

        msg = await message.channel.send(embed=embed)
        emojis = ['🔐', '🔓', '🔏', '✅', '❎', '🎟', '✒', '💻', '🚫']
        for emoji1 in emojis:
            await msg.add_reaction(emoji1)

        try:
            def check1(r, u):
                return (
                    r.message.id == msg and u == ctx.author
                    and emojis in reaction.emoji
               )
            def check2(m):
                return m.author == ctx.author and m.channel == channel and m == msg

            react = await self.bot.wait_for('reaction_add', timeout=60.0, check=check1)
            if react[0].emoji == '🔐':
                await self.lock(ctx)
            elif react[0].emoji == '🔓':
                await self.unlock(ctx)
            elif react[0].emoji == '🔏':
                await self.view_only(ctx)
            elif react[0].emoji == '✅':
                try:
                    embed = discord.Embed(title='チャンネルへ招待✅',
                    description=f'招待する人を言ってください。\n> （ID, メンション, 名前に対応しています。）',
                    color=0x0080ff)
                    msg = await ctx.send(embed=embed)
                    react = await self.bot.wait_for('message', timeout=30.0, check=check2)
                    await self.permit(self, ctx, react[0])
                except asyncio.TimeoutError:
                    await msg.delete()
            elif react[0].emoji == '❎':
                try:
                    embed = discord.Embed(title='チャンネルからつまみ出す❎',
                    description=f'チャンネルからつまみ出す対象を言ってください。\n> （ID, メンション, 名前に対応しています。）',
                    color=0x0080ff)
                    msg = await ctx.send(embed=embed)
                    react = await self.bot.wait_for('message', timeout=30.0, check=check2)
                    await self.reject(self, ctx, react[0])
                except asyncio.TimeoutError:
                    await msg.delete()
            elif react[0].emoji == '🎟':
                try:
                    embed = discord.Embed(title='チャンネル人数制限🎟',
                    description=f'チャンネルの制限人数を言ってください。',
                    color=0x0080ff)
                    msg = await ctx.send(embed=embed)
                    react = await self.bot.wait_for('message', timeout=30.0, check=check2)
                    await self.limit(self, ctx, limit)
                except asyncio.TimeoutError:
                    await msg.delete()
            elif react[0].emoji == '✒':
                try:
                    embed = discord.Embed(title='チャンネル名変更✒',
                    description=f'チャンネルの名前を変更してください。',
                    color=0x0080ff)
                    msg = await ctx.send(embed=embed)
                    react = await self.bot.wait_for('message', timeout=30.0, check=check2)
                    await self.name(self, ctx, name)
                except asyncio.TimeoutError:
                    await msg.delete()
            elif react[0].emoji == '💻':
                await self.claim(ctx)
            elif react[0].emoji == '🚫':
                await msg.edit(embed=embed_no)
                await msg.clear_reactions()
        except asyncio.TimeoutError:
            await msg.edit(embed=embed_no)
            await msg.clear_reactions()

    @voice.command(name="lock")
    async def _lock(self, ctx):
        await self.lock(ctx)

    async def lock(self, ctx):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
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

    @voice.command(name="view_only")
    async def _view_only(self, ctx):
        await self.view_only(ctx)

    async def view_only(self, ctx):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
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

    @voice.command(name="unlock")
    async def _unlock(self, ctx):
        await self.unlock(ctx)

    async def unlock(self, ctx):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
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

    @voice.command(name="permit", aliases=["allow"])
    async def _permit(self, ctx, member):
        await self.permit(ctx, member)

    async def permit(self, ctx, member: discord.Member):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
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

    @voice.command(name="reject", aliases=["deny"])
    async def _reject(self, ctx, member):
        await self.reject(ctx, member)

    async def reject(self, ctx, member: discord.Member):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
            await channel.set_permissions(member, connect=False, speak=False, read_message_history=False, send_messages=False, read_messages=False)
            await text_channel.set_permissions(member, connect=False, speak=False, read_message_history=False, send_messages=False, read_messages=False)
            await member.move_to(self.bot.get_channel(655272738952314908))
            embed_1 = discord.Embed(title='Channel Moderate!',
            description=f'{member.name}さんをつまみ出しました。❎',
            color=0xff0000)
            embed_2 = discord.Embed(title='Your Reject.',
            description=f'{member.mention}さん、あなたはつまみ出されました。❎',
            color=0xff0000)
            await ctx.send(content=f"{ctx.author.mention}", embed=embed_1)
            await member.send(embed=embed_2)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command(name="limit")
    async def _limit(self, ctx, limit):
        await self.limit(ctx, limit)

    async def limit(self, ctx, limit):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            await channel.edit(user_limit = limit)
            embed = discord.Embed(title='Channel Moderate!',
            description=f'参加人数を{limit}人に制限しました。🎟',
            color=0xffffff)
            await ctx.send(content=f"{ctx.author.mention}", embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

    @voice.command(name="name")
    async def _name(self, ctx, *, name):
        await self.name(ctx, name)

    async def name(self, ctx, name):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            text_channel = self.bot.get_channel(self.datas["channel_data"][str(channel.id)]["id"])
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

    @voice.command(name="claim")
    async def _claim(self, ctx):
        await self.claim(ctx, ctx)

    async def claim(self, ctx):
        channel = ctx.author.voice.channel
        self.datas = self.mongo_coll.find_one(filter={"server": 615849898637656093})
        if ctx.author.id == self.datas["channel_data"][str(channel.id)]["owner"]:
            x = False
            for member in channel.members:
                if member.id == self.datas[channel.id]["owner"]:
                    await ctx.send(content=f"とっくにオーナーさんいるやないですか。")
                    x = True
            if x == False:
                self.datas[channel.id]["owner"] = ctx.author.id
                self.mongo_coll.update_one({"server": 615849898637656093}, {'$set':self.datas})
                embed = discord.Embed(title='Channel Moderate!',
                description=f'{ctx.author.mention}さん、あなたが今ここのオーナーです。💻',
                color=0x80ff00)
                await ctx.send(content=ctx.author.mention, embed=embed)
        elif channel is None:
            await ctx.send(content=f"{ctx.author.mention}さんボイチャ入ってないですやんか")
        else:
            await ctx.send(content=f"{ctx.author.mention}さん、多分そこあんたのチャンネルじゃないよ。")

def setup(airlinia):
    airlinia.add_cog(Voice_Channel(airlinia))
