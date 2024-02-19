import discord
from discord.ext import commands
import pymongo
import dotenv
import os
import datetime
import traceback
import json

dotenv.load_dotenv()
token = os.getenv('token')


class AicyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="a!",
            intents=discord.Intents.all(),
            
            )
        self.start_time = datetime.datetime.now()
    async def on_ready(self):
        for file in os.listdir("./cogs"):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f"Loaded cogs: cogs.{file[:-3]}")
                except Exception as e:
                    print(f"cogs.{file[:-3]} failed to load", e)
                    traceback.print_exc()
        try:
            await self.load_extension("jishaku") # Load jishaku
            print("Loaded extension: Jishaku")
        except Exception:
            traceback.print_exc()            
        sync = await self.tree.sync() # Slash command automatic sync
        await self.change_presence(activity=discord.Game(name="あいしぃーによるぼっと"), status="Online")
        await bot.get_channel(1058005805426814976).send(embed=discord.Embed(title="Startup Program finished!", description=f"Logging in {self.user.name}\n起動時間: {discord.utils.format_dt(self.start_time)}"))
        # await bot.get_channel(1145593830998016070).send(embed=discord.Embed(title="サーバーが起動しました！", description=f"サーバーが起動した時間:{discord.utils.format_dt(self.start_time)}"))
        print(f"起動完了!\nLogging in {self.user.name} ({self.user.id})\n 同期済みコマンド：{len(sync)}")



if __name__ == "__main__":
    print("Program starting...")
    bot=AicyBot()
    try:
        bot.run(token)
    except Exception:
        print("Program Crashed!\n")
        traceback.print_exc()
