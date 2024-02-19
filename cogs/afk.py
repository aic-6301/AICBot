import discord
from discord.ext import commands
import json
import asyncio


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.array = []

    async def afk_add(self, ctx, reason):
        dic = {}
        dic.update({"user_id": str(ctx.author.id)})
        dic.update({"reason": str(reason)})
        data = json.dumps(dic, ensure_ascii=False)
        msg = await self.bot.get_channel(1094512811557797969).send(data)
        return "Done"

    async def afk_del(self, msgid:int):
        try:
            msg = await self.bot.get_channel(1094512811557797969).fetch_message(msgid)
            await msg.delete()
            return "ok"
        except:
            return "bad"

    async def afk_get_mention(self, message):
        mention = str(message.mentions[0].id)
        messages = self.bot.get_channel(1094512811557797969).history(limit=None)
        async for msg in messages:
            if mention in msg.content:
                data = json.loads(msg.content)
                if data['reason'] == "None":
                    reason="なし"
                else:
                    reason = data['reason']
                user=await self.bot.fetch_user(data['user_id'])
                await message.reply(embed=discord.Embed(title=f"{user.name}はAFKです。",
                                                         description=f"理由：{str(reason)}", color=discord.Color.from_rgb(237, 175, 65)
                                                         ).set_footer(text="このメッセージは5秒後に削除されます。"), delete_after=5)

    async def afk_get(self, message):
        messages = self.bot.get_channel(1094512811557797969).history(limit=None)
        id = str(message.author.id)
        async for msg in messages:
            if id in msg.content:
                return msg.id
            else:
                return None

    @commands.command(name="afk")
    async def afk(self, ctx, reason=None):
        await asyncio.sleep(2)
        back = await self.afk_add(ctx, reason)
        if back == "Done":
            await ctx.reply("AFKに設定しました。")
        else:
            await ctx.reply("失敗")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        back = await self.afk_get(message)
        if back is None:
            if not message.mentions:
                return
            else:
                await self.afk_get_mention(message)
                return
        else:
            ba = await self.afk_del(msgid=back)
            if ba == "ok":
                await message.reply(embed=discord.Embed(title="AFKを解除しました", color=discord.Color.green()
                                                        ).set_footer(text="このメッセージは5秒後に削除されます"), delete_after=5)
            else:
                await message.reply("失敗")


async def setup(bot):
    await bot.add_cog(Afk(bot))
