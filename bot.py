import random
import discord
from discord.ext import commands
from discord import app_commands
import responses

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{username}" ({channel})')

    if user_message[0] == '?':
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private=False)

    await bot.process_commands(message)


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(f"{member.mention} has left the server")


@bot.command()
async def ping(ctx):
    await ctx.reply(f"Ping: {round(bot.latency * 1000)}ms")


@bot.command(aliases=['name'])
async def eightball(ctx, *, question):
    responses = ["iizam", "taco", "papi sah", "sami", "yazen", "ozmin", "kerem", "niz", "kinglightning20", "silly girl",
                 "aboody",
                 "amiin", "big clock yamin", "bigjim", "bobdi", "hadyKwiek", "korga", "laith", "mr.Mumz", "sosa",
                 "faris",
                 "zeid", "duckgang24", "abdul"]

    await ctx.send(f"**Question: ** {question}\n**Answer: **{random.choice(responses)}")


def run_discord_bot():
    TOKEN = 'ttt'
    bot.run(TOKEN)


run_discord_bot()
