import discord
from discord.ext import commands
import traceback


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['ss'])
    async def server_settings(self, ctx ):
        if ctx.invoked_subcommand is None:
            await ctx.send("使用方法が違うよ！")
    @server_settings.group(name="bot_role")
    async def _bot_role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("使用方法が違うよ！")
    @_bot_role.command(name="set")
    async def role_set(self, ctx, bot_id: discord.Role):
        try:
            self.bot.server_set.replace_one(
                {
                "_id": False,
                "guild_id": ctx.guild.id},
                {"guild_id": ctx.guild.id,
                "bot_id": bot_id.id}, upsert=True)
            await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{bot_id.mention}にロールを付与するように設定しました。"))
        except:
            traceback.print_exc()

async def setup(bot):
    await bot.add_cog(settings(bot))