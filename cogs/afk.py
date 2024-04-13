import discord
from discord import app_commands
from discord.ext import commands
import json
import asyncio
import requests
import os
from datetime import time, datetime

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.array = []

    async def afk_add(self, ctx, reason) -> requests.Response:
        """
        Add a user to the AFK list.

        Args:
            ctx (commands.Context): The context of the command.
            reason (str): The reason for the AFK status.

        Returns:
            str: A message indicating success or failure.
        """
        if await self.afk_get(ctx):
            return False
        dic = {}
        dic.update({"id": str(ctx.user.id)})
        dic.update({"reason": reason if reason else "None"})
        data = json.dumps(dic, ensure_ascii=False)
        await self.bot.get_channel(1094512811557797969).send(data)
        header = {"Authorization": f"{os.getenv('api_token')}"}
        res = requests.post("https://api.munesky.net/v1/afk", data=data, headers=header)
        return res

    async def afk_del(self, id:int, msg:discord.Message) -> requests.Response:
        """
        Delete an AFK message from the channel.

        Args:
            id (int): The ID of the message to delete.

        Returns:
            str: A status indicating success or failure.
        """

        header = {"Authorization": f"{os.getenv('api_token')}"}
        res = requests.delete(f"https://api.munesky.net/v1/afk/{id}", headers=header)
        await msg.delete()
        return res
        
    async def afk_get_api(self, id:int) -> requests.Response:
        header = {"Authorization": f"{os.getenv('api_token')}"}
        res = requests.get(f"https://api.munesky.net/v1/afk/{id}", headers=header)
        return res.json()["data"]

    async def afk_get_mention(self, message):
        mention = str(message.mentions[0].id)
        messages = self.bot.get_channel(1094512811557797969).history(limit=None)
        async for msg in messages:
            if mention in msg.content:
                data = await self.afk_get_api(mention)
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
        id = str(message)
        async for msg in messages:
            if id in msg.content:
                return msg
            else:
                return None

    @app_commands.command(name="afk")
    async def afk(self, interaction: discord.Interaction, reason:str=None):
        back = await self.afk_add(ctx = interaction, reason=reason)
        if back is False:
            await interaction.response.send_message("登録済みです。", ephemeral=True)
        if back.status_code == 200:
            await interaction.response.send_message("AFKに設定しました。", ephemeral=True)
        else:
            await interaction.response.send_message(f"失敗\nエラー：{back.json()['message'] or back.json()['detail']}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot:
            return
        back = await self.afk_get(message.author.id)
        if back is None:
            if not message.mentions:
                return
            else:
                await self.afk_get_mention(message)
                return
        else:
            ba:requests.Response = await self.afk_del(id=message.author.id, msg=back)
            print(ba.json())
            if ba.status_code == 200:
                time = datetime.strptime(ba.json()['data']['time'], '%Y-%m-%d %H:%M:%S')
                await message.reply(embed=discord.Embed(title="AFKを解除しました",description=f"また会いましたね！{discord.utils.format_dt(time, style='f')}ぶりです！", color=discord.Color.green()
                                                        ).set_footer(text="このメッセージは5秒後に削除されます"), delete_after=5)
            else:
                await message.reply(f"失敗, Error:{ba.json()['message']}", mention_author=False)


async def setup(bot):
    await bot.add_cog(Afk(bot))
