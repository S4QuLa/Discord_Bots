# discord.py is Sweeeeeeeeeeeeeeet!!!!!
import discord
from discord.ext import commands
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
                    self.load_extension(f'cogs.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

    async def on_ready(self): # 準備完了時に呼び出す。
        print(f'ログインしました。\n------\nBotのアカウントの概要\nユーザー名:{bot.user.name}\nユーザーID:{bot.user.id}\n------\nDiscord.pyのバージョン\n{discord.__version__}\n------\nPythonのバージョン\n{sys.version}\n――――――――――――――――――――――――――――――')
        await bot.change_presence(activity=discord.Game(name=f'{self.command_prefix}￤{bot.user.name} - by.amazakura0804'))

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
                    self.load_extension(f'cogs.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

    async def on_ready(self): # 準備完了時に呼び出す。
        print(f'ログインしました。\n------\nBotのアカウントの概要\nユーザー名:{bot.user.name}\nユーザーID:{bot.user.id}\n------\nDiscord.pyのバージョン\n{discord.__version__}\n------\nPythonのバージョン\n{sys.version}\n――――――――――――――――――――――――――――――')
        await bot.change_presence(activity=discord.Game(name=f'{self.command_prefix}￤{bot.user.name} - by.amazakura0804'))

if __name__ == '__main__':
    technetium = TECHNETIUM(command_prefix='te!')
    technetium.run(os.environ['TECHNETIUM_DISCORD_TOKEN'])

    airlinia = AIRLINIA(command_prefix='al!')
    airlinia.run(os.environ['AIRLINIA_DISCORD_TOKEN'])
