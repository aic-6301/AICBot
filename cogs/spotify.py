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
        global before_activity
        if after.bot:
            return
        if before.activities is not None:
            for activity in before.activities:
                if isinstance(activity, discord.Spotify):
                    before_activity = activity
        for activities in after.activities:
            if isinstance(activities, discord.Spotify):
                    if before_activity.title is None or before_activity.title != activities.title:
                        file = Path(f"data/{after.guild.id}.json")
                        file.touch(exist_ok=True)
                        with open(file=file, mode="r+", encoding="utf-8") as data:
                            config = json.load(data)
                        if str(after.guild.id) in data.name:
                            if config["Spotify"] is True:
                                embed = discord.Embed(title=f"{after.display_name}の再生中の曲",
                                                       description=f"再生中 - {activities.title}\n 残り{discord.utils.format_dt(activities.end, style='R')}",
                                                       color=discord.Color.from_str("#0x1DB954"), url=activities.track_url)
                                # embed = discord.Embed(title=f"{after.display_name}がSpotifyで{activities.title}を再生中です!", description=f"再生中 - {activities.title}\n 残り{discord.utils.format_dt(activities.end, style='R')}", color=discord.Color.from_str(0x1DB954), url=activities.track_url)
                                embed.add_field(name="タイトル", value=activities.title, inline=True)
                                embed.add_field(name="アルバム", value=f"{activities.album}")
                                embed.add_field(name="作者", value=f"{activities.artist}")
                                if activities.album_cover_url:
                                    embed.set_thumbnail(url=activities.album_cover_url)
                                else:
                                    pass
                                title = activities.artist.replace(' ', '+')
                                view = discord.ui.View()
                                view.add_item(discord.ui.Button(label=f"{activities.artist} 検索", style=discord.ButtonStyle.url, 
                                                                url=f"https://google.com/search?q={title}"))
                                view.add_item(discord.ui.Button(label=f"聴いてみる！", style=discord.ButtonStyle.url, url=activities.track_url))
                                try:
                                    
                                    if config["Spotify_ch"] is None:
                                        await after.guild.system_channel.send(embed=embed, view=view)
                                    else:
                                        await self.bot.get_channel(config["Spotify_ch"]).send(embed=embed, view=view)
                                except:
                                    if config["Spotify_ch"] is None:
                                        await after.guild.system_channel.send(embed=embed, view=view)
                                    else:
                                        await self.bot.get_channel(config["Spotify_ch"]).send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(spotify(bot))