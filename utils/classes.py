from datetime import datetime
import os
import platform
import traceback

from aiohttp import ClientSession
from colorama import Back, Fore, Style
from discord.ext import commands, menus
import discord

from utils.funcs import can_execute_action
import config

embed_color = config.OK_COLOR.replace("#", "0x")


class EmbedListMenu(menus.ListPageSource):
    """
    Paginated embed menu.
    """

    def __init__(self, data):
        """
        Initializes the EmbedListMenu.
        """
        super().__init__(data, per_page=1)

    async def format_page(self, menu, embeds):
        """
        Formats the page.
        """
        return embeds


class HimejiHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=int(embed_color, base=16))
            await destination.send(embed=embed)


class HimejiBot(commands.AutoShardedBot):
    """Idk"""

    def __init__(self, *args, **kwargs):
        print(Fore.GREEN, f"\rStarting the bot...")
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.BOT_PREFIX),
            intents=discord.Intents.all(),
            help_command=HimejiHelpCommand(no_category="Help"),
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
            *args,
            **kwargs,
        )
        self.owner_ids = config.OWNER_IDS
        self.ok_color = int(str(f"0x{config.OK_COLOR}").replace("#", ""), base=16)
        self.error_color = int(str(f"0x{config.ERROR_COLOR}").replace("#", ""), base=16)
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
        unloaded_cogs = 0
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                    print(Fore.YELLOW + f"Loaded {cog}", Style.RESET_ALL)
                    loaded_cogs += 1
                except Exception as e:
                    unloaded_cogs += 1
                    print(
                        Fore.RED + f"Failed to load the cog: {cog}",
                        Style.RESET_ALL,
                    )
                    print(Back.RED, Fore.WHITE, f"\r{e}", Style.RESET_ALL)
        print(Fore.MAGENTA, "\rDONE", Style.RESET_ALL)
        print(Fore.GREEN, f"\rTotal loaded cogs: {loaded_cogs}", Style.RESET_ALL)
        print(Fore.RED, f"\rTotal unloaded cogs: {unloaded_cogs}", Style.RESET_ALL)
        print("-" * 15)

    async def on_shard_connect(self, shard_id):
        print(Fore.GREEN, f"\rShard {shard_id} Logged Into Discord.", Style.RESET_ALL)
        print("-" * 15)

    async def on_shard_disconnect(self, shard_id):
        print(
            Fore.RED,
            f"\rSHARD {shard_id} IS NOW IN A DISCONNECTED STATE FROM DISCORD",
            Style.RESET_ALL,
        )
        print("-" * 15)

    async def close(self):
        """Logs out of Discord and closes all connections."""
        await super().close()
        if self._session:
            await self._session.close()


bot = HimejiBot()
