import discord, argparse

from dotenv import load_dotenv
from discord.ext import commands

import models
from database import engine

parser = argparse.ArgumentParser(description='Discord bot for auto moderation of challenge "Secret Server"')
parser.add_argument('--test-platform', dest="test_platform", action='store_true', default=False)
parser.add_argument('--test-env', dest="test_env", action='store_true', default=False)

args = parser.parse_args()

load_dotenv(".env.test" if args.test_env else ".env")

models.Base.metadata.create_all(bind=engine)

from cogs import *
from logs import *
from modals import *
from vars import *

class DiscordBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        if args.test_env:
            logger.info("Running on test environment")
        if args.test_platform:
            logger.info("Running using test platform")

        logger.info(f'Logged on as {self.user}!')
        await self.add_cog(SafetyCog(self))
        await self.add_cog(VerificationCog(self))
        message = await bot.get_channel(VERIFY_CHANNEL_ID).fetch_message(VERIFY_MESSAGE_ID)
        await message.add_reaction("✅")

    async def on_message(self, message: discord.Message):
        if message.guild is not None and message.guild.id == SERVER_ID:
            logger.info(f"User {message.author.name} sent message {message.content}")

    async def setup_hook(self):
        app_commands = await self.tree.sync()
        logger.info(app_commands)
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=discord.Object(id=SERVER_ID))
        await self.tree.sync(guild=discord.Object(id=SERVER_ID))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = DiscordBot(intents=intents)
@bot.tree.command(
    name="request",
    description="Verify your identity with a flag submission platform (24.cuhkctf.org) access token"
)
async def request(interaction: discord.Interaction):
    model = GetTokenModal(url="https://test.cuhkctf.org" if args.test_platform else "https://24.cuhkctf.org")
    await interaction.response.send_modal(model)

bot.run(DISCORD_TOKEN)