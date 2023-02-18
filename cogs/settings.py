import discord
from discord.ext import commands
import traceback


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def server_settings(self, ctx ):
        if ctx.invoked_subcommand is None:
            await ctx.send("使用方法が違うよ！")
    @server_settings.command()
    async def _bot_role(self, ctx, bot_id):
        try:
            """await self.guild_set.replace_one({
                "guild_id": ctx.guild.id,
                "bot_id": bot_id})"""
            await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、<@&{bot_id}>にロールを付与するように設定しました。"))
        except:
            try:
                """await self.guild_set.replace_one({
                "guild_id": ctx.guild.id,
                "bot_id": bot_id})"""
                await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、<@&{bot_id}>にロールを付与するように設定しました。"))
            except:
                traceback.print_exc()

async def setup(bot):
    await bot.add_cog(settings(bot))
