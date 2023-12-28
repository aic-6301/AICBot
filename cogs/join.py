import discord
from discord.ext import commands
from discord import app_commands

import json
import os


class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        with open(f"data/{guild.id}.json", mode="w", encoding="utf-8") as file:
            data = {"bot_role_id": None, "Spotify": False, "Spotify_ch": None}
            file.write(data)
            return
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        os.remove(f"data/{guild.id}.json")
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(join(bot))