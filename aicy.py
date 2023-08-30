import discord
from discord.ext import commands
import pymongo
import dotenv
import os
import datetime
import traceback

dotenv.load_dotenv()
token = os.getenv('token')


class AicyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="a!",
            intents=discord.Intents.all(),
            
            )
        self.start_time = datetime.datetime.now()
        self.dbclient = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.dbclient['AicyBot']
        self.server_set = self.db['server_settings']
    async def on_ready(self):
        for file in os.listdir(os.getenv("COG_FOLDER")):
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
        await self.tree.sync() # Slash command automatic sync
        await self.change_presence(activity=discord.Game(name="あいしぃーのためのぼっと"), status="Online")
        await bot.get_channel(1058005805426814976).send(embed=discord.Embed(title="Startup Program finished!", description=f"Logging in {self.user.name}\nStart time: {discord.utils.format_dt(self.start_time)}"))
        print(f"Startup Program finished!\nLogging in {self.user.name}")



if __name__ == "__main__":
    print("Program starting...")
    bot=AicyBot()
    try:
        bot.run(token)
    except Exception:
        print("Program Crashed!\n")
        traceback.print_exc()
