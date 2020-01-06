# discord.py is Sweeeeeeeeeeeeeeet!!!!!
import discord
from discord.ext import commands
import asyncio
import os # 環境変数読み込むマン。
# versionとerrorを質問したら返してくれるやさしいおじさん。
import sys
import traceback

class TECHNETIUM(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        self.command_prefix = command_prefix
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)
        # cogフォルダにある.pyファイルを読み込む。
        for cog in os.listdir("./technetium_cogs"):
            if cog.endswith('.py'):
                try:
                    self.load_extension(f'technetium_cogs.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

    async def on_ready(self): # 準備完了時に呼び出す。
        print(f'ログインしました。\n------\nBotのアカウントの概要\nユーザー名:{technetium.user.name}\nユーザーID:{technetium.user.id}\n------\nDiscord.pyのバージョン\n{discord.__version__}\n------\nPythonのバージョン\n{sys.version}\n――――――――――――――――――――――――――――――')
        await technetium.change_presence(activity=discord.Game(name=f'{self.command_prefix}￤{technetium.user.name} - by.amazakura0804'))

class AIRLINIA(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        self.command_prefix = command_prefix
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)
        # cogフォルダにある.pyファイルを読み込む。
        for cog in os.listdir("./airlinia_cogs"):
            if cog.endswith('.py'):
                try:
                    self.load_extension(f'airlinia_cogs.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

    async def on_ready(self): # 準備完了時に呼び出す。
        print(f'ログインしました。\n------\nBotのアカウントの概要\nユーザー名:{airlinia.user.name}\nユーザーID:{airlinia.user.id}\n------\nDiscord.pyのバージョン\n{discord.__version__}\n------\nPythonのバージョン\n{sys.version}\n――――――――――――――――――――――――――――――')
        await airlinia.change_presence(activity=discord.Game(name=f'{self.command_prefix}￤{airlinia.user.name} - by.amazakura0804'))

if __name__ == '__main__':
    technetium = TECHNETIUM(command_prefix='te!')
    asyncio.wait([technetium.run(os.environ['TECHNETIUM_DISCORD_TOKEN'])])

    airlinia = AIRLINIA(command_prefix='al!')
    asyncio.wait([airlinia.run(os.environ['AIRLINIA_DISCORD_TOKEN'])])
