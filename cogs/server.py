import discord
from discord.ext import commands, tasks
from datetime import datetime
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import traceback


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_today = self.bot. db['today']

    async def set_ch(self, guildid, channelid):
        ch_check = await self.db_today.find_one({"channel_id": channelid})
        if ch_check is None:
            await self.db_today.insert_one(
                {
                "_id": False,
                "Guild_id": guildid
                },
                {
                "channel_id": channelid}
                )
        else:
            raise KeyError("既に設定されています。")

    async def get_ch(self, guildid: int =None) -> list:
        target={"_id": False}
        if guildid is not None:
            target["Guild_id"] = guildid
        return [row async for row in self.db_today.find(target)
                if row
                 ]




    async def get_today(self) -> discord.Embed:
        # 今日はなんの日をyahooから持ってくる。
        async with ClientSession() as session:
            async with session.get(
                "https://kids.yahoo.co.jp/today"
            ) as r:
                day = BeautifulSoup(
                    await r.read(), "html.parser"
                ).find("dl")

                embed = discord.Embed(
                    title=day.find("span").text,
                    description=day.find("dd").text,
                    color=0xee373e
                )
                embed.set_footer(
                    text="Yahoo きっず",
                    icon_url="http://www.google.com/s2/favicons?domain=www.yahoo.co.jp"
                )
            return embed

    @tasks.loop(seconds=30)
    async def today_notification(self):
        if datetime.now().strftime("%H:%M") == "07:00":
            embed = await self.get_today()
            for row in await self.get_ch:
                channel = self.bot.get_channel(row[1])
                if channel:
                    try:
                        channel.send(embed=embed)
                    except (discord.Forbidden, discord.HTTPException):
                        pass
                else:
                    await self.delete_ch(row[0], row[1])
    @commands.group()
    async def today(self, ctx, set: bool=None):
        if set is None:
            embed = await self.get_today()
            try:
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)
        elif ctx.author.guild_permissions.manage_channels:
            try:
                await self.set_ch(ctx.guild.id, ctx.channel.id)
                if len(await self.get_ch(ctx.guild.id)) == 3:
                    raise OverflowError
            except (KeyError, OverflowError) as e:
                if isinstance(e, OverflowError):
                    return await ctx.reply("一つのサーバーに3つまで設定できます")
            await ctx.reply(embed=discord.Embed(title="✅設定完了", description=f"Botが入室した際、{ctx.channel.mention}にロールを付与するように設定しました。"))

async def setup(bot):
    await bot.add_cog(Server(bot))
