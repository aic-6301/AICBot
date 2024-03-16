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
        print(back)
        if back is not False:
            await ctx.reply(f"{back}です！ ({input})")
        else:
            await ctx.reply(back)
            


async def setup(bot: commands.Bot):
    await bot.add_cog(dicebot(bot))