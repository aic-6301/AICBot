import discord
from discord.ext import commands
import os
import json
import requests
from pytube import extract
import re

class link_view(discord.ui.View):
    def __init__(self, data, id):
        super().__init__()
        self.timeout = False
        self.data = data

        self.add_item(discord.ui.Button(label="動画を見る", style=discord.ButtonStyle.url, url="https://www.youtube.com/watch?v="+id))
    @discord.ui.button(label="概要欄", style=discord.ButtonStyle.secondary, emoji="📝", row=1)
    async def description(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(embed=discord.Embed(title=self.data['items'][0]['snippet']['title']+"の概要欄", description=self.data['items'][0]['snippet']['description'], color=discord.Color.from_rgb(255, 11, 0)), ephemeral=True)
        return
    @discord.ui.button(label="削除する", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def delete_emb(self, interaction: discord.Interaction, button: discord.ui.button):
        message = await interaction.channel.fetch_message(interaction.message.id)
        await message.delete()

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        r = re.match(r"(https://)?(www\.)(youtube\.com|youtu\.be)/?(watch\?v=)", message.content)
        try:
            id = extract.video_id(message.content)
            await message.add_reaction("<:search_youtube:1209789663590621254>")
            return
        except:
                id = None



    async def link_search(self, message):
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
                    view = link_view(data, id)
                else:
                    embed = discord.Embed(title=data['items'][0]['snippet']['title'], color=discord.Color.from_rgb(255, 11, 0), url="https://www.youtube.com/watch?v="+id)
                    view = link_view(data, id)
                #embed.add_field(name="アップロード日", value=f"{discord.utils.format_dt(data['items'][0]['snippet']['publishedAt'])}{discord.utils.format_dt(data['items'][0]['snippet']['publishedAt'], style='R')}")
                embed.set_author(name=data['items'][0]['snippet']['channelTitle'], url="https://youtube.com/channel/"+data['items'][0]['snippet']['channelId'])
                try:
                    embed.set_image(url=data['items'][0]['snippet']['thumbnails']['maxres']['url'])
                except:
                    embed.set_image(url=data['items'][0]['snippet']['thumbnails']['standard']['url'])
                embed.set_footer(text=f"{viewcount}回視聴")
                return embed, view
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
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await (self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id))
        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == "search_youtube":
            embed, view = await self.link_search(message)
            await message.reply(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Youtube(bot))
