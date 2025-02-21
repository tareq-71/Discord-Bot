import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

# ✅ Use only one logging setup (Remove extra logging)
discord.utils.setup_logging()  # Handles both Discord and bot logs

# ✅ Define logging format for cleaner output (No duplicate handlers)
logger = logging.getLogger("discord")  # Use Discord's logger
logger.setLevel(logging.INFO)  # Change to DEBUG for more details

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name="Brawl Stars"))
    logger.info(f'{bot.user} is now running!')

# ✅ Log every command usage
@bot.event
async def on_command(ctx):
    logging.info(f"📢 Command used: {ctx.command} by {ctx.author} in {ctx.guild.name if ctx.guild else 'DM'}")

# ✅ Log command errors
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"⚠️ Error with command '{ctx.command}': {error}")

@bot.event
async def on_member_remove(member):
    logging.info(f"{member} has left the server.")
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"😢 {member.mention} has left the server.")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel = discord.utils.get(member.guild.text_channels, name="bot-testing")
        if channel:
            await channel.send(f"{member} has joing the voice channels.")


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = f'cogs.{filename[:-3]}'
            try:
                if extension in bot.extensions:
                    logger.info(f"⚠️ {extension} is already loaded. Skipping...")
                else:
                    await bot.load_extension(extension)
                    logger.info(f"✅ Loaded {extension}")
            except Exception as e:
                logger.error(f"⚠️ Failed to load {extension}: {e}")

async def main():
    async with bot:
        load_dotenv()  # Load environment variables
        await load_cogs()  # Load cogs BEFORE starting the bot
        DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
        await bot.start(DISCORD_BOT_TOKEN)

import asyncio
asyncio.run(main())
