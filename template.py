import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


def run_discord_bot():
    TOKEN = 'BOT TOKEN'  # Replace with your bot token
    bot.run(TOKEN)

# Run the bot
run_discord_bot()
