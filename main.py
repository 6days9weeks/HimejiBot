import os
import platform
from datetime import datetime

import discord
from aiohttp import ClientSession
from colorama import Fore, Style
from discord.ext import commands

import config


class HimejiHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.random())
            await destination.send(embed=embed)


class Bot(commands.AutoShardedBot):
    """Idk"""

    def __init__(self, *args, **kwargs):
        print(Fore.GREEN, f"\rStarting the bot...")
        super().__init__(
            command_prefix=config.BOT_PREFIX,
            intents=discord.Intents.all(),
            help_command=HimejiHelpCommand(no_category="Help"),
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
            *args,
            **kwargs,
        )
        self.owner_ids = config.OWNER_IDS
        self.uptime = None
        self._session = None

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession(loop=self.loop)
        return self._session

    async def on_connect(self):
        print(Fore.GREEN, f"\rLogged in as {self.user.name}(ID: {self.user.id})")
        print(
            f"Using Python version *{platform.python_version()}* and using Discord.py version *{discord.__version__}*"
        )
        print(
            f"Running on: {platform.system()} {platform.release()} ({os.name})",
            Style.RESET_ALL,
        )
        print("-" * 15)

    async def on_ready(self):
        if bot.uptime is not None:
            return
        bot.uptime = datetime.utcnow()
        print(Fore.MAGENTA + "STARTING COG LOADING PROCESS", Style.RESET_ALL)
        loaded_cogs = 0
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                except Exception as e:
                    print(Fore.RED + f"Failed to load the cog: {cog}", Style.RESET_ALL)
                loaded_cogs += 1
                print(Fore.YELLOW + f"Loaded {cog}", Style.RESET_ALL)
        print(f"Total loaded cogs: {loaded_cogs}")
        print(Fore.MAGENTA + "DONE", Style.RESET_ALL)
        print("-" * 15)


bot = Bot()
bot.run(config.TOKEN)
