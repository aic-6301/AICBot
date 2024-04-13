import discord
from discord.ext import commands
from discord import app_commands

import json
import os


class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_data(self, guild):
        db = self.bot.db.cursor()
        db.execute(f"SELECT `role` FROM `bot` WHERE `guild` = ?", (guild.id,))
        data = db.fetchone()
        return data


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            data = self.get_data(member.guild)
            if data:
                await member.add_roles(member.guild.get_role(data[0]), reason="Botであり、ロールが設定されていたため。")
                return
            else:
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(join(bot))