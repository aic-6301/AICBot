import discord
from discord.ext import commands, tasks
from discord import app_commands, Webhook

from datetime import datetime, time, timedelta
import pytz
import requests
import json



class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.ranking.start()
        self.embed = None
        self.data = {}
    
    async def sender(self, message:str, ):
        await self.bot.get_channel(1180147591338537090).send(message)

    async def geter(self, message):
        async for msg in self.bot.get_channel(1180147591338537090).history(limit=None):
            if msg.created_at == datetime.today():
                self.data["content"] = {msg.content}
            if message.author.id in self.data:
                self.data = {}
                return 1
            else:
                self.data = {}
                return None



    def is_time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.channel == self.bot.get_channel(1180334698703106181):
            if message.author.bot:
                return
            result = await self.geter(message)
            if result is not None:
                print("added")
                return
            msg_time = message.created_at + timedelta(hours=9)
            if self.is_time_in_range(time(11, 54), time(11, 55), msg_time.time()):
                self.messages[message.author.id] = (message.author.id, (message.created_at + timedelta(hours=9)).strftime('%H%M%S%f'))
                await self.bot.get_channel(1180147591338537090).send(message.author.id)
            else:
                print("not time")

    @tasks.loop(seconds=15)
    async def ranking(self):
        channel = self.bot.get_channel(1180334698703106181)
        now = datetime.now()
        if now.strftime("%H:%M") == "11:55":
            if self.embed is None:
                print(self.messages)
                sorted_messages = sorted(self.messages.items(), key=lambda x: abs(int(x[1][1]) - 24000000))
                rank_message = "Ranking:\n"
                for i, msg in enumerate(sorted_messages):
                    rank_message += f"{i+1}位. <@{msg[1][0]}> 送信時間:{msg[1][1][:2]}:{msg[1][1][2:4]}:{msg[1][1][4:6]}.{msg[1][1][7:]}\n"
                self.embed = await channel.send(embed=discord.Embed(title="一コメランキング", description=rank_message))
            else:
                pass
        elif now.strftime("%H%M") == "11:49":
            if self.embed is None:
                self.embed = await channel.send(embed=discord.Embed(title="一コメランキング", description=f"計測中...結果は重複回避のため{discord.utils.format_dt((now+timedelta(days=1)).replace(hour=0, minute=5, second=0, microsecond=0))}に送信されます。"))
            else:
                pass
        else:
            print("not time (tasks)")
            self.embed = None
            print(self.embed)


    async def cog_unload(self):
        self.ranking.stop()
        

async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot))