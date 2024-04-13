import discord
from discord import app_commands
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.reply(embed=discord.Embed(title="エラー - Bad Argument", description="指定された引数がエラーを起こしているため実行出来ません。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - Command Not Found", description="コマンドが存在しません。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.reply(embed=discord.Embed(title="クールダウン",description=f"コマンドはクールダウン中です。\n{discord.utils.format_dt(error.retry_after, style='R')}後に再度実行してください。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - Member Not Found", description="メンバーが存在しません。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.reply(embed=discord.Embed(title="エラー - User Not Found", description="ユーザーが存在しません", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(embed=discord.Embed(title="エラー - Missing Permissions", description="権限が不足しています。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed(title="エラー - Missing Required Argument", description="必要な引数が足りません。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.reply(embed=discord.Embed(title="エラー - Bot Missing Permissions", description="Botが実行するのに必要な権限が足りません。", color=discord.Color.red(), timestamp=ctx.message.created_at))
        else:
            await ctx.reply(embed=discord.Embed(title="エラー - Unknown Error", description=f"エラーが発生しました。\nエラー内容：{error} \nエラーID:{ctx.message.id}", color=discord.Color.red(), timestamp=ctx.message.created_at).set_footer(text="エラーIDをコピーして、お問い合わせサーバーまでお問い合わせください。"))
        embed = discord.Embed(title="Error Info", description="", color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.add_field(name="エラー内容", value=error, inline=False)
        embed.add_field(name="エラーID", value=ctx.message.id, inline=False)
        embed.add_field(name="実行ユーザー", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
        embed.add_field(name="実行サーバー", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
        await self.bot.get_channel(1033496616130334784).send(embed=embed)
    
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction:discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                embed=discord.Embed(title="エラー - Bot Missing Permissions", 
                                    description="Botが実行するのに必要な権限が足りません。", 
                                    color=discord.Color.red(), 
                                    timestamp=interaction.message.created_at
                                    ))
        elif isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                embed=discord.Embed(title="クールダウン",
                                    description=f"コマンドはクールダウン中です。\n{discord.utils.format_dt(error.retry_after, style='R')}後に再度実行してください。",
                                    color=discord.Color.red(),
                                    timestamp=interaction.message.created_at
                                    ))
        else:
            await interaction.response.send_message(
                embed=discord.Embed(title="エラー - Unknown Error",
                                    description=f"エラーが発生しました。\nエラー内容：{error} \nエラーID:{interaction.message.id}",
                                    color=discord.Color.red(),
                                    timestamp=interaction.message.created_at
                                    ).set_footer(text="エラーIDをコピーして、お問い合わせサーバーまでお問い合わせください。")
                )
        embed = discord.Embed(title="Error Info", description="", color=discord.Color.red(), timestamp=interaction.message.created_at)
        embed.add_field(name="エラー内容", value=error, inline=False)
        embed.add_field(name="エラーID", value=interaction.message.id, inline=False)
        embed.add_field(name="実行ユーザー", value=f"{interaction.user.name} ({interaction.user.id})", inline=False)
        embed.add_field(name="実行サーバー", value=f"{interaction.guild.name} ({interaction.guild.id})", inline=False)
        await self.bot.get_channel(1033496616130334784).send(embed=embed)
            


async def setup(bot):
    await bot.add_cog(Error(bot))
