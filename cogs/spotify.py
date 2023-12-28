import discord
from discord.ext import commands
from discord import app_commands

from pathlib import Path
import json
import os

class spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.bot:
            return
        print(after)
        print(after.activities)
        for activities in after.activities:
            print(activities)
            if isinstance(activities, discord.Spotify):
                activities = after.activities
                file = Path(f"data/{after.guild.id}.json")
                file.touch(exist_ok=True)
                with open(file=file, mode="r+", encoding="utf-8") as data:
                    config = json.load(data)
                print(data.name)
                print(config)
                if str(after.guild.id) in data.name:
                    print("y")
                    if config["Spotify"]:
                        print("y2")
                        embed = discord.Embed(title=f"{after.display_name}がSpotifyで{activities.title}を再生中です!",description=f"再生中 - {activities.title}\n 残り{discord.utils.format_dt(activities.end, style='R')}", color=discord.Spotify.color, url=activities.track_url)
                        embed.add_field(name="タイトル", value=activities.title, inline=True)
                        embed.add_field(name="アルバム", value=f"{activities.album}")
                        embed.add_field(name="歌っている人", value=f"[{activities.artist} 検索](https://google.com/search?q={activities.artist})")
                        embed.set_image(url=activities.album_cover_url)
                        if config["Spotify_ch"] is None:
                            await after.guild.system_channel.send(embed=embed)
                        else:
                            await self.bot.get_channel(config["Spotify_ch"]).send(embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(spotify(bot))