import discord
from discord.ext import commands, tasks
import traceback
import json
from pathlib import Path
import os


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
            file = Path(f"data/{ctx.guild.id}.json")
            file.touch(exist_ok=True)
            with open(file=file, mode="r+", encoding="utf-8") as data:
                config = json.load(data)
            config["bot_role_id"] = bot_id.id
            with open(f"data/{ctx.guild.id}.json", "w+", encoding="utf-8") as file:
                json.dump(config, file, indent=1)
            await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{bot_id.mention}にロールを付与するように設定しました。"))
        except:
            traceback.print_exc()
    
    @server_settings.group(name="spotify")
    async def _spotify(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("使用方法が違うよ！")
    
    @_spotify.command(name="set")
    async def spotify_set(self, ctx, mode: bool, channel: discord.TextChannel):
        if mode:
            try:
                file = Path(f"data/{ctx.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                config["Spotify"] = True
                config["Spotify_ch"] = channel.id
                with open(f"data/{ctx.guild.id}.json", "w+", encoding="utf-8") as file:
                    json.dump(config, file)
                await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Spotifyの再生の通知を有効に設定しました。"))
            except:
                traceback.print_exc()
        else:
            try:
                file = Path(f"data/{ctx.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                config["Spotify"] = mode
                config["Spotify_ch"] = None
                with open(f"data/{ctx.guild.id}.json", "w+", encoding="utf-8") as file:
                    json.dump(config, file, indent=2)
                await ctx.send(embed=discord.Embed(title="✅設定完了", description=f"Spotifyの再生の通知を無効に設定しました。"))
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