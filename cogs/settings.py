import discord
from discord import app_commands
from discord.ext import commands, tasks
import traceback
import json
from pathlib import Path
import os


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="server_settings", description="サーバーの設定をします。", guild_only=False)

    @group.command(name="bot_role")
    @app_commands.describe(bot_id="Botロールを指定します")
    async def role_set(self, interaction:discord.Interaction, bot_id: discord.Role):
        try:
            file = Path(f"data/{interaction.guild.id}.json")
            file.touch(exist_ok=True)
            with open(file=file, mode="r+", encoding="utf-8") as data:
                config = json.load(data)
            config["bot_role_id"] = bot_id.id
            with open(f"data/{interaction.guild.id}.json", "w+", encoding="utf-8") as file:
                json.dump(config, file)
            await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{bot_id.mention}にロールを付与するように設定しました。"))
        except:
            traceback.print_exc()
    
    @group.command(name="spotify")
    async def spotify_set(self, interaction: discord.Interaction, mode: bool, channel: discord.TextChannel=None):
        if mode or channel:
            try:
                file = Path(f"data/{interaction.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                config["Spotify"] = True
                config["Spotify_ch"] = channel.id
                with open(f"data/{interaction.guild.id}.json", "w+", encoding="utf-8") as file:
                    json.dump(config, file)
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotifyの再生の通知を有効に設定しました。"))
            except:
                traceback.print_exc()
        elif mode and channel is None:
            try:
                file = Path(f"data/{interaction.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                config["Spotify"] = True
                config["Spotify_ch"] = interaction.channel.id
                with open(f"data/{interaction.guild.id}.json", "w+", encoding="utf-8") as file:
                    json.dump(config, file)
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotifyの再生の通知を有効に設定しました。"))
            except:
                traceback.print_exc()
        else:
            try:
                file = Path(f"data/{interaction.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                config["Spotify"] = mode
                config["Spotify_ch"] = None
                with open(f"data/{interaction.guild.id}.json", "w+", encoding="utf-8") as file:
                    json.dump(config, file, indent=2)
                await interaction.response.send_message(embed=discord.Embed(title="✅設定完了", description=f"Spotifyの再生の通知を無効に設定しました。"))
            except:
                traceback.print_exc()
    
    @tasks.loop(seconds=10.0)
    async def check_config(self):
        for file in os.listdir():
            if file.endswith(".json"):
                files = open(f"data/{file}", "w+", encoding="utf-8")
                if files == "":
                    files.write("{}")
                    files.close()
                    
    

async def setup(bot):
    await bot.add_cog(settings(bot))