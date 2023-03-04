import discord
from discord.ext import commands
import os
import json
import requests
from pytube import extract

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        permission = message.channel.permissions_for(message.author)
        if permission.embed_links is True:
            return
        if message.content in "youtube.com/watch?v=" or  "youtu.be/":
            try:
                id = extract.video_id(message.content)
            except Exception as e:
                id = None
            if id is None:
                return
            else:
                url=requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={id}&key={os.environ['youtube_api_key']}&part=snippet,statistics")
                text=url.text
                data=json.loads(text)
                viewcount = "{:,}".format(int(data['items'][0]['statistics']['viewCount']))
                if len(data['items'][0]['snippet']['description']) <= 500:
                    embed = discord.Embed(title=data['items'][0]['snippet']['title'], description=data['items'][0]['snippet']['description'], color=discord.Color.from_rgb(255, 11, 0), url="https://www.youtube.com/watch?v="+id)
                else:
                    embed = discord.Embed(title=data['items'][0]['snippet']['title'], color=discord.Color.from_rgb(255, 11, 0), url="https://www.youtube.com/watch?v="+id)
                #embed.add_field(name="アップロード日", value=f"{discord.utils.format_dt(data['items'][0]['snippet']['publishedAt'])}{discord.utils.format_dt(data['items'][0]['snippet']['publishedAt'], style='R')}")
                embed.set_author(name=data['items'][0]['snippet']['channelTitle'], url="https://youtube.com/channel/"+data['items'][0]['snippet']['channelId'])
                embed.set_image(url=data['items'][0]['snippet']['thumbnails']['maxres']['url'])
                embed.set_footer(text=f"{viewcount}回視聴")
                await message.reply(embed=embed, mention_author=False)
    @commands.group()
    async def search(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("使い方が違うよ！")
    @search.command()
    async def youtube(self, ctx, q):
        url = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={os.environ['youtube_api_key']}&q={q}&part=snippet&type=video")
        text=url.text
        data=json.loads(text)
        embed=discord.Embed(title=f"{q}での検索結果", description="", color=discord.Color.from_rgb(255, 11, 0)).set_author(name="Youtube", icon_url="https://1.bp.blogspot.com/-qdRfUNOtjkM/XeI_00z9pzI/AAAAAAAAF4E/FeD2SvVFnKUjPAKQ_cNM6-D2ahjKb0HkQCLcBGAsYHQ/s1600/Youtube-Icon-square-2340x2340-2.png")
        embed.add_field(name=data['items'][0]['snippet']['channelTitle'], value=f"[{data['items'][0]['snippet']['title']}](https://www.youtube.com/watch?v={data['items'][0]['id']['videoId']})", inline=False)
        embed.add_field(name=data['items'][1]['snippet']['channelTitle'], value=f"[{data['items'][1]['snippet']['title']}](https://www.youtube.com/watch?v={data['items'][1]['id']['videoId']})", inline=False)
        embed.add_field(name=data['items'][2]['snippet']['channelTitle'], value=f"[{data['items'][2]['snippet']['title']}](https://www.youtube.com/watch?v={data['items'][2]['id']['videoId']})", inline=False)
        embed.add_field(name=data['items'][3]['snippet']['channelTitle'], value=f"[{data['items'][3]['snippet']['title']}](https://www.youtube.com/watch?v={data['items'][3]['id']['videoId']})", inline=False)
        embed.add_field(name=data['items'][4]['snippet']['channelTitle'], value=f"[{data['items'][4]['snippet']['title']}](https://www.youtube.com/watch?v={data['items'][4]['id']['videoId']})", inline=False)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Youtube(bot))
