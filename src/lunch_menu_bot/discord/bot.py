import discord
from discord.ext import commands
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


RATE_LIMIT_SECONDS = 60  # Rate limit in seconds
MESSAGE_SPLIT_LENGTH = 2000  # Maximum length of a message


# Set up intents
bot_intents = discord.Intents.default()
bot_intents.message_content = True  # Enable message content intent if needed


class LunchMenuCog(commands.Cog):
    def __init__(self, bot, func_get_menu):
        self.bot = bot
        self.func_get_menu = func_get_menu

    @commands.cooldown(1, RATE_LIMIT_SECONDS, commands.BucketType.guild)
    @commands.command()
    async def menu(self, ctx):
        ret = self.func_get_menu()

        message = None
        embed = None
        if isinstance(ret, str):
            message = ret
        if isinstance(ret, discord.Embed):
            embed = ret
        if isinstance(ret, tuple):
            message = ret[0]
            embed = ret[1]

        logger.info(f"Sending message: {message} and embed: {embed}")

        # Split the message if it's too long
        messages = [
            message[i : i + MESSAGE_SPLIT_LENGTH]
            for i in range(0, len(message), MESSAGE_SPLIT_LENGTH)
        ]

        n_messages = len(messages)
        for i, msg in enumerate(messages):
            # Send the message (and embed if it's the last message)
            logger.info(f"Send {i+1}/{n_messages}: {msg}")
            await ctx.send(
                msg,
                embed=embed if i == n_messages - 1 else None,
                silent=True,
            )


class LunchMenuBot(commands.Bot):
    def __init__(self, func_get_menu, *args, **kwargs):
        super().__init__(command_prefix="!", intents=bot_intents, *args, **kwargs)
        self.func_get_menu = func_get_menu

    async def setup_hook(self):
        # Add the cog during the setup phase
        await self.add_cog(LunchMenuCog(self, self.func_get_menu))

    # Override on_message to be able to handle commands in the middle of a message
    async def on_message(self, message):
        # Prevent the bot from responding to its own messages
        if message.author.id == self.user.id:
            logger.info("Ignoring message from myself")
            return

        # Convert the message content to lowercase for case-insensitive matching
        content_lower = message.content.lower()

        command_found = False  # Initialize the command_found variable
        for command in ["!menu"]:
            if command in content_lower:
                message.content = (
                    command + " " + message.content
                )  # prepend the command to the message
                ctx = await self.get_context(message)
                await self.invoke(ctx)
                command_found = True
                break

        # Process other commands only if no custom command was invoked
        if not command_found:
            await self.process_commands(message)
