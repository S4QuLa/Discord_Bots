🌸☕import discord
import typing
import random
from discord.ext import commands
import re
import asyncio

class CategoryIndex(commands.Cog):
    def __init__(self, technetium, name=None):
        self.bot = technetium
        self.id_match = re.compile(r'ID:(\d*)')
        self.name = name if name is not None else type(self).__name__
        self.index_index = self.bot.get_channel(702026398897799209)

    @commands.command(brief='カテゴリインデックスを作ります')
    async def create_category_index(self, ctx, *args):
        async def _create_category_index(category, ctx=None):
            index_channel: discord.TextChannel = self._find_index_channel(category)
            if index_channel is None:
                if ctx is not None:
                    await ctx.send('インデックスチャンネルが見つかりませんでした。')
            else:
                await index_channel.purge(check=lambda m: m.author == self.bot.user and m.embeds)
                await self._create_category_index1(category)
                channels = sorted(
                    (c for c in category.channels if isinstance(c, discord.TextChannel) and c != index_channel),
                    key=lambda c: c.position
                )
                tasks = [self.bot.loop.create_task(self._create_category_index2(channel))
                         for channel in channels]
                await asyncio.wait(tasks)
        if not args:
            category = ctx.channel.category
            await _create_category_index(category, ctx)
        elif args[0] == 'all':
            tasks = [self.bot.loop.create_task(_create_category_index(category,)) for category in
                     ctx.guild.categories]
            await asyncio.wait(tasks)
        else:
            category = await commands.converter.CategoryChannelConverter().convert(ctx, args[0])
            await _create_category_index(category, ctx)

    # インデックスチャンネルをサーチ。なければNone
    def _find_index_channel(self, category)\
            -> typing.Union[discord.TextChannel, type(None)]:
        try:
            index_channel: discord.TextChannel = next(
                c for c in category.channels if 'Category-index' in c.topic )
        except StopIteration:
            return None
        else:
            return index_channel

    # インデックスの上のメンションのやつを作る方。
    async def _create_category_index1(self, category):
        index_channel = self._find_index_channel(category)
        if index_channel is not None:
            try:
                message = await index_channel.history(oldest_first=True) \
                                      .filter(lambda m: m.author == self.bot.user and not m.embeds) \
                                      .next()
            except discord.NoMoreItems:
                message = None
            channels = sorted((c for c in category.channels if isinstance(
                c, discord.TextChannel) and c != index_channel), key=lambda c: c.position)
            content = '\n'.join(('━' * 5, self.index_index.mention, '━' * 5, '')) \
                + '\n'.join(map(lambda c: c.mention,
                                sorted(channels, key=lambda c: c.position)))
            if message is not None:
                await message.edit(content=content)
            else:
                await index_channel.send(content=content)
            return 1

    async def _create_category_index2(self, channel):  # インデックスの下のEmbedを作る方。
        index_channel = self._find_index_channel(
            channel.category)
        if index_channel is not None:
            async for message in (index_channel.history(oldest_first=True)
                                  .filter(lambda m: m.author == self.bot.user and m.embeds)):
                match = self.id_match.search(message.embeds[0].description)
                if match and channel.id == int(match.group(1)):
                    break
            else:
                message = None
            cl = discord.Color(random.randint(0, 0xFFFFFF))
            description = channel.topic if channel.topic else 'トピックは粛清された模様。'
            embed = discord.Embed(title=channel.name,
                                  description='ID:{0}'.format(channel.id),
                                  color=cl)
            embed.add_field(name='チャンネルトピック', value=description)
            embed.set_footer(text=channel.category.name)
            if message is not None:
                await message.edit(embed=embed)
            else:
                await index_channel.send(embed=embed)
            return 1

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if (isinstance(channel, discord.TextChannel)
                and channel.category is not None):
            await self._create_category_index1(channel.category)
            await self._create_category_index2(channel)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if (isinstance(channel, discord.TextChannel)
                and channel.category is not None):
            await self._create_category_index1(channel.category)
            index_channel = self._find_index_channel(channel.category)
            if index_channel:
                async for message in (index_channel.history(oldest_first=True)
                                      .filter(lambda m: m.author == self.bot.user and m.embeds)):
                    match = self.id_match.search(message.embeds[0].description)
                    if match and channel.id == int(match.group(1)):
                        await message.delete()
                        break

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if isinstance(after, discord.TextChannel) and after.topic not in 'Category-index':
            if before.category is not None and (after.category is None or before.category != after.category):
                await self.on_guild_channel_delete(before)
            if (before.name != after.name
                    or bool(before.topic) is not bool(after.topic)
                    or before.topic != after.topic):
                await self.on_guild_channel_create(after)

def setup(technetium):
    technetium.add_cog(CategoryIndex(technetium))
