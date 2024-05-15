import discord
from discord.ext import commands, tasks
from discord import app_commands

from datetime import datetime, timedelta
import random


class april(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot
        self.april.start()
        self.message = None
        
    def get_data(self):
        db = self.bot.db.cursor()
        db.execute(f"SELECT `channel` FROM `april`", ())
        columns = [column[0] for column in db.description] # 列名を取得
        data = [dict(zip(columns, row)) for row in db.fetchall()] # 結果を辞書に変
        return data
    
    @tasks.loop(seconds=15)
    async def april(self):
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            if now.month == 4 and now.day == 1:
                if self.message is None:
                    channels = self.get_data()
                    for ch in channels:
                        print(ch['channel'])
                        with open("data/uso800.txt", "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            random_line_number = random.randint(0, len(lines) - 1)
                            txt = lines[random_line_number].strip()
                        channel = self.bot.get_channel(int(ch['channel']))
                        self.message = await channel.send(embed=discord.Embed(title="今日はエイプリルフールだよ！！", description=f"{txt}", color=discord.Color.pink()))
            else:
                if self.message is None:
                    channels = self.get_data()
                    today = (now - datetime(now.year, 4, 1)).days
                    if now < datetime(now.year, 4, 1):
                        today += 365
                    for ch in channels:
                        with open("data/uso800.txt", "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            random_line_number = random.randint(0, len(lines) - 1)
                            txt = lines[random_line_number].strip()
                        channel = self.bot.get_channel(int(ch['channel']))
                        self.message = await channel.send(embed=discord.Embed(title="エイプリルフール通知", description=f"今日はエイプリルフール{today}日目です。\n{txt}", color=discord.Color.pink()).set_footer(text="Generated by Gemini",icon_url="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png"))
        else:
            self.message = None
    @app_commands.command(name="next_april", description="次のエイプリルフール")
    async def next_april(self, interaction:discord.Interaction):
        now = datetime.now()
        year = now.year
        print(now)
        if now.month == 4 and now.day == 1:
            await interaction.response.send_message(embed=discord.Embed(title="エイプリルフールまで何日？", description=f"今日がエイプリルフールだよ！！！",color=discord.Color.pink()))
        if now > datetime(year, 4, 1):
            year += 1
        time = datetime(year, 4, 1)
        await interaction.response.send_message(embed=discord.Embed(title="エイプリルフールまで何日？", description=f"次のエイプリルフールまで残り{discord.utils.format_dt(time, style='R')} ({discord.utils.format_dt(time, style='f')})です。", color=discord.Color.pink()))
        
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(april(bot))