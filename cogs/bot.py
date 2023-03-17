import discord
from discord.ext import commands


class invitebutton(discord.ui.View):
    def __init__(self, select_bot):
        super().__init__()
        self.timeout = None
        self.add_item(discord.ui.Button(label="管理者権限で招待",emoji="👑",style=discord.ButtonStyle.url, url=f"https://discord.com/api/oauth2/authorize?client_id={select_bot.id}&permissions=8&scope=bot%20applications.commands"))
        self.add_item(discord.ui.Button(label="権限を選択して招待",emoji="🔢",style=discord.ButtonStyle.url, url=f"https://discord.com/api/oauth2/authorize?client_id={select_bot.id}&permissions=1194000908287&scope=bot%20applications.commands"))
        self.add_item(discord.ui.Button(label="権限無しで招待",emoji="❌",style=discord.ButtonStyle.url, url=f"https://discord.com/api/oauth2/authorize?client_id={select_bot.id}&scope=bot%20applications.commands"))


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx, bot: discord.User =None):
        if bot == None:
            select_bot = self.bot.user
        if bot is not None:
            search_bot = await self.bot.fetch_user(bot.id)
            select_bot = search_bot
        if select_bot.bot is False:
            await ctx.send("Botを選択してください。")
        else:
            await ctx.send(embed=discord.Embed(title=f"{select_bot.name}の招待リンク", 
            description=f"",
            color=select_bot.color), view=invitebutton(select_bot)
            )
    @commands.command()
    async def about(self, ctx):
        await ctx.send(embed=discord.Embed(
                                        title="このBotについて",
                                        description="あいしぃーによるあいしぃーのためのぼっとです。いろいろやってます", color=discord.Colour.from_rgb(160, 106, 84))
                                        .add_field(name="作成者", value="あいしぃー([@AIC_6301](https://twitter.com/AIC_6301))\n[Link-Tree](https://linktr.ee/aic_6301/)")
                                        .add_field(name="Botのソース", value="[Github](https://github.com/AIC-6301/AICBot)")
                                        .add_field(name="ライブラリ",value=f"`Python 3.10`, `discord.py {discord.__version__}`")
                                        .add_field(name="サーバー数", value=f"{len(self.bot.guilds)}")
                                        .add_field(name="メンバー数", value=f"{len(self.bot.users)}")
                                        )
async def setup(bot):
    await bot.add_cog(Bot(bot))
