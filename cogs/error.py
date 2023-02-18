import discord
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.reply(embed=discord.Embed(title="エラー - Bad Argument", description="指定された引数がエラーを起こしているため実行出来ません。", color=discord.Color.red))
        elif isinstance(commands.errors.CommandNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - Command Not Found", description="コマンドが存在しません。", color=discord.Color.red))
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.reply(embed=discord.Embed(title="クールダウン",description=f"コマンドはクールダウン中です。\n{discord.utils.format_dt(error.retry_after, style='R')}後に再度実行してください。", color=discord.Color.red))
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - Member Not Found", description="メンバーが存在しません。", color=discord.Color.red))
        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - User Not Found", description="ユーザーが存在しません", color=discord.Color.red))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(embed=discord.Embed(title="エラー - Missing Permissions", description="権限が不足しています。", color=discord.Color.red))
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed(title="エラー - Missing Required Argument", description="必要な引数が足りません。", color=discord.Color.red))
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.reply(embed=discord.Embed(title="エラー - Bot Missing Permissions", description="Botが実行するのに必要な権限が足りません。", color=discord.Color.red))
            

def setup(bot):
    bot.add_cog(Error(bot))
