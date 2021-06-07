import asyncio

import discord
from discord.ext import tasks, commands


class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status_handler.start()

    @tasks.loop()
    async def status_handler(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.competing, name="your love"
            )
        )
        await asyncio.sleep(60)
        await self.bot.change_presence(activity=discord.Game("with you :D"))
        await asyncio.sleep(60)
        await self.bot.change_presence(activity=discord.Game("with Tylerr#6979!"))
        await asyncio.sleep(60)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"you do {config.prefix}help"
            )
        )
        await asyncio.sleep(60)
        await self.bot.change_presence(
            activity=discord.Game(f"with {len(self.bot.users)} humans!")
        )
        await asyncio.sleep(60)
        await self.bot.change_presence(
            activity=discord.Game(f"in {len(self.bot.guilds)} guilds")
        )
        await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(Tasks(bot))
