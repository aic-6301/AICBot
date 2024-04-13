import discord
from discord.ext import commands
from discord import app_commands

from pathlib import Path
import json
import os

class spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.before_activity = {}
    
    
    def get_data(self, guild):
        db = self.bot.db.cursor()
        db.execute(f"SELECT `channel` FROM `spotify` WHERE `guild` = ?", (guild.id,))
        data = db.fetchone()
        return data

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.bot:
            return
        if before.activities is not None:
            for activity in before.activities:
                if isinstance(activity, discord.Spotify):
                    self.before_activity[before.id] = activity
        for activities in after.activities:
            if isinstance(activities, discord.Spotify):
                if before is None or self.before_activity[before.id].title != activities.title:
                    data = self.get_data(after.guild)
                    print(data)
                    if data is not None:
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
                        await self.bot.get_channel(data[0]).send(embed=embed, view=view)
                        return
        self.before_activity[before.id] = None
        return

    @app_commands.command(name="spotify")
    async def spotify(self, interaction: discord.Interaction, user: discord.Member):
        if user is None:
            user = interaction.user
        for activities in user.activities:
            if isinstance(activities, discord.activity.Spotify):
                embed = discord.Embed(title=f"{interaction.user.display_name}の再生中の曲",
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
                await interaction.response.send_message(embed=embed, view=view)
                return
        await interaction.response.send_message(embed=discord.Embed(title=f"{interaction.user.display_name}の再生中の曲はありません", color=discord.Color.from_str("#0x1DB954")), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(spotify(bot))