import discord
from discord import app_commands
from discord.ext import commands

from .dice import dice


# * 自作

class dicebot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx, input):
        back = dice.dice(self, input)
        if back is not False:
            await ctx.reply(f"{back}です！ ({input})")
        else:
            await ctx.reply(embed=discord.Embed(title="エラー", description="引数が不正です", color=discord.Color.red()))
            


async def setup(bot: commands.Bot):
    await bot.add_cog(dicebot(bot))