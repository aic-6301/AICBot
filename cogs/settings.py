import discord
from discord import app_commands
from discord.ext import commands, tasks
import traceback
import json
from pathlib import Path
import os
import mariadb

class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="server_settings", description="サーバーの設定をします。", guild_only=False)

    @group.command(name="bot_role", description="自動付与されるBotロールを設定します。")
    @app_commands.describe(role="Botロールを指定します(未入力で登録解除)")
    async def role_set(self, interaction:discord.Interaction, role: discord.Role=None):
        if role:
            if role.position >= interaction.guild.me.top_role.position:
                await interaction.response.send_message(embed=discord.Embed(title="×設定失敗", description="ロールがBotのロールの位置より上です。", color=discord.Color.red()), ephemeral=True)
                return
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `bot` (guild, role) VALUES (?, ?)", (interaction.guild.id, role.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{role.mention}にロールを付与するように設定しました。", color=discord.Color.green()), ephemeral=True)
            except mariadb.Error:
                db = self.bot.db.cursor()
                db.execute("UPDATE `bot` SET `guild` = ?, `role` = ?", (interaction.guild.id, role.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🔄️設定更新", description=f"Botが入室した際、{role.mention}にロールを付与するように更新しました。", color=discord.Color.green()), ephemeral=True)
        else:
            try:
                db = self.bot.db.cursor()
                db.execute("DELETE FROM `bot` WHERE `guild` =?", (interaction.guild.id,))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"Botロールを削除しました。", color=discord.Color.green()), ephemeral=True)
            except Exception:
                traceback.print_exc()
            
    
    @group.command(name="spotify", description="Spotify再生通知を設定します。")
    @app_commands.describe(channel="Spotify再生通知を送るチャンネルを指定します(未入力で登録解除)")
    async def spotify_set(self, interaction: discord.Interaction, channel: discord.TextChannel=None):
        if channel:
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `spotify` (guild, channel) VALUES (?, ?)", (interaction.guild.id, channel.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotify再生通知を送るチャンネルを{channel.mention}に設定しました。", color=discord.Color.green()))
            except mariadb.Error:
                db = self.bot.db.cursor()
                db.execute("UPDATE `spotify` SET `guild` = ?, `channel` = ?", (interaction.guild.id, channel.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🔄️設定更新", description=f"Spotify再生通知を送るチャンネルを{channel.mention}に更新しました。", color=discord.Color.green()))
            except Exception:
                traceback.print_exc()
        else:
            try:
                db = self.bot.db.cursor()
                db.execute("DELETE FROM `spotify` WHERE `guild` =?", (interaction.guild.id,))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"Spotify再生通知を送るチャンネルを削除しました。", color=discord.Color.green()))
            except Exception:
                traceback.print_exc()
                
    @group.command(name="april", description="エイプリルフールから何日経っているかを通知します。")
    @app_commands.describe(channel="どこのチャンネルに設定するか(未入力で登録解除)")
    async def role_set(self, interaction:discord.Interaction, channel: discord.TextChannel=None):
        if channel:
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `april` (guild, channel) VALUES (?, ?)", (interaction.guild.id, channel.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"エイプリルフールの通知するチャンネルを、{channel.mention}に設定しました。"))
            except:
                db = self.bot.db.cursor()
                db.execute("UPDATE `april` SET `channel` = ? WHERE `guild` = ?", (channel.id, interaction.guild.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🔄️設定更新", description=f"エイプリルフールの通知するチャンネルを、{channel.mention}に更新しました。"))
            finally:
                traceback.print_exc()
        else:
            try:
                db = self.bot.db.cursor()
                db.execute("DELETE FROM `channel` WHERE `guild`", (channel.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"エイプリルフールの通知をオフにしました"))
            except:
                traceback.print_exc()

                    
    

async def setup(bot):
    await bot.add_cog(settings(bot))