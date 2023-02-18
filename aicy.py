import discord
from discord.ext import commands, components
from motor import motor_asyncio as motor

import dotenv
import os
import datetime
import traceback

dotenv.load_dotenv()
token = os.environ.get('token')




class AicyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="a!",
            intents=discord.Intents.all(),
            
            )
        self.start_time = datetime.datetime.now()
    async def on_ready(self):
        await self.change_presence(status="Offline") # なんとなく
        """self.dbclient = motor.AsyncIOMotorClient("localhost:27017")
        self.db = self.dbclient["AicyBot"]
        self.guild_set = self.db.guild_set"""
        for file in os.listdir('./cogs'):
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
        try:
            await self.load_extension("discord.ext.components") # Load jishaku
            print("Loaded extension: dpy-components")
        except Exception:
            traceback.print_exc()
        await self.tree.sync() # Slash command automatic sync
        await self.change_presence(activity=discord.Game(name="あいしぃーのためのぼっと"), status="Online")
        print(f"Startup Program finished!\nLogging in {self.user.name}")



if __name__ == "__main__":
    print("Program starting...")
    bot=AicyBot()
    try:
        bot.run(token)
    except Exception:
        print("Program Crashed!\n")
        traceback.print_exc()
