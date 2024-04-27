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
        
    def get_data(self, mode, interaction):
        db = self.bot.db.cursor()
        db.execute(f"SELECT * FROM `{mode}` WHERE `guild` = ?", (interaction.guild.id))
        data = db.fetchone()
        return data

    group = app_commands.Group(name="settings", description="サーバーの設定をします。", guild_only=False)

    @group.command(name="bot_role", description="自動付与されるBotロールを設定します。")
    @app_commands.describe(mode="Trueで有効化 / Falseで無効化", role="Botロールを指定します")
    async def role_set(self, interaction:discord.Interaction, mode: bool, role: discord.Role=None):
        if role:
            if role.position >= interaction.guild.me.top_role.position:
                await interaction.response.send_message(embed=discord.Embed(title="×設定失敗", description="ロールがBotのロールの位置より上です。", color=discord.Color.red()), ephemeral=True)
                return
        if role is None and mode:
            await interaction.response.send_message(embed=discord.Embed(title="×設定失敗", description="モードがオンの時は、ロールの指定が必要です。", color=discord.Color.red()), ephemeral=True)
        if mode and role:
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `bot` (guild, role) VALUES (?, ?)", (interaction.guild.id, role.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{role.mention}にロールを付与するように設定しました。", color=discord.Color.green()), ephemeral=True)
            except mariadb.Error:
                db = self.bot.db.cursor()
                db.execute("UPDATE `bot` SET `role` = ? WHERE `guild` = ?", (interaction.guild.id, role.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="🔄️設定更新", description=f"Botが入室した際、{role.mention}にロールを付与するように更新しました。", color=discord.Color.green()), ephemeral=True)
        else:
            try:
                if self.get_data(mode="bot", interaction=interaction):
                    db = self.bot.db.cursor()
                    db.execute("DELETE FROM `bot` WHERE `guild` =?", (interaction.guild.id,))
                    self.bot.db.commit()
                    await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"Botロール付与を無効にしました。", color=discord.Color.green()), ephemeral=True)
                else:
                        await interaction.response.send_message(embed=discord.Embed(title="エラー", description=f"すでに無効です。", color=discord.Color.red()))
            except Exception:
                traceback.print_exc()
            
    
    @group.command(name="spotify", description="Spotify再生通知を設定します。")
    @app_commands.describe(mode="Trueで有効化 / Falseで無効化", channel="Spotify再生通知を送るチャンネルを指定します")
    async def spotify_set(self, interaction: discord.Interaction, mode:bool, channel: discord.TextChannel=None):
        if channel:
            ch = channel
        else:
            ch = interaction.channel
        if mode:
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `spotify` (guild, channel) VALUES (?, ?)", (interaction.guild.id, ch.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotify再生通知を送るチャンネルを{ch.mention}に設定しました。", color=discord.Color.green()))
            except mariadb.Error:
                db = self.bot.db.cursor()
                db.execute("UPDATE `spotify` SET `guild` = ?, `channel` = ?", (interaction.guild.id, ch.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotify再生通知を送るチャンネルを{ch.mention}に更新しました。", color=discord.Color.green()))
            except Exception:
                traceback.print_exc()
        else:
            try:
                if self.get_data(mode="spotify", interaction=interaction):
                    db = self.bot.db.cursor()
                    db.execute("DELETE FROM `spotify` WHERE `guild` =?", (interaction.guild.id,))
                    self.bot.db.commit()
                    await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"Spotify再生通知を無効にしました。", color=discord.Color.green()))
                else:
                    await interaction.response.send_message(embed=discord.Embed(title="エラー", description=f"すでに無効です。", color=discord.Color.red()))
            except Exception:
                traceback.print_exc()
                
    @group.command(name="april", description="エイプリルフールから何日経っているかを通知します。")
    @app_commands.describe(mode="Trueで有効化 / Falseで無効化", channel="どこのチャンネルに設定するか")
    async def role_set(self, interaction:discord.Interaction, mode: bool, channel: discord.TextChannel=None):
        if channel:
            ch = channel
        else:
            ch = interaction.channel
        if mode:
            try:
                db = self.bot.db.cursor()
                db.execute("INSERT INTO `april` (guild, channel) VALUES (?, ?)", (interaction.guild.id, ch.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"エイプリルフールの通知するチャンネルを、{ch.mention}に設定しました。", color=discord.Color.green()))
            except:
                db = self.bot.db.cursor()
                db.execute("UPDATE `april` SET `channel` = ? WHERE `guild` = ?", (ch.id, interaction.guild.id))
                self.bot.db.commit()
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"エイプリルフールの通知するチャンネルを、{ch.mention}に更新しました。", color=discord.Color.green()))
            finally:
                traceback.print_exc()
        else:
            try:
                if self.get_data(mode="april", interaction=interaction):
                    db = self.bot.db.cursor()
                    db.execute("DELETE FROM `april` WHERE `guild` =?", (interaction.guild.id,))
                    self.bot.db.commit()
                    await interaction.response.send_message(embed=discord.Embed(title="🗑️設定削除", description=f"エイプリルフールの通知を無効にしました", color=discord.Color.green()))
                else:
                    await interaction.response.send_message(embed=discord.Embed(title="エラー", description=f"すでに無効です。", color=discord.Color.red()))
            except:
                traceback.print_exc()

                    
    

async def setup(bot):
    await bot.add_cog(settings(bot))