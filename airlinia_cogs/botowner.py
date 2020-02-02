# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import commands
import asyncio

import textwrap
import contextlib
import traceback
import io

class Bot_Owner_Command(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send('停止しやーす！！')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())
        embed = discord.Embed(title='Eval Command!', description='コードをどうぞ。', color=0x0080ff)
        embed.set_author(name=f'{ctx.author.name} - 作成許可待ちです。',icon_url='https://i.imgur.com/yRCJ26G.gif')
        await ctx.send(embed=embed)
        message = await self.client.wait_for(
            'message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        body = self.cleanup_code(message.content)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(airlinia):
    airlinia.add_cog(Bot_Owner_Command(airlinia))
