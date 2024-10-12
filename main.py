import discord
from discord.ext import commands
import random
import time
import os
import json
from gamelogic import run_mathgame, run_numgame, run_blackjack


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

server_members = []
game_lock = False
members_SIUBucks = {}

# File to store SIUBucks
SIUBUCKS_FILE = "siubucks_data.json"


# On Ready #
@bot.event
async def on_ready():
    global server_members
    # Load SIUBucks data when the bot starts
    load_SIUBucks()

    for guild in bot.guilds:
        # Store all members except bots in the global list
        server_members = [member for member in guild.members if not member.bot]

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="Thick of it! By: KSI"))
    print(f'{bot.user} is now running!')

# Random Commands
@bot.command()
async def say(ctx, channel: discord.TextChannel, *, message: str):
    await channel.send(message)

@bot.command()
async def member(ctx):
    await ctx.send(random.choice(server_members))

# END of Random Commands

# SIUBucks Functions #

# Load SIUBucks from a JSON file
def load_SIUBucks():
    global members_SIUBucks
    try:
        with open(SIUBUCKS_FILE, "r") as f:
            members_SIUBucks = json.load(f)
    except FileNotFoundError:
        members_SIUBucks = {}

# Save SIUBucks to a JSON file
def save_SIUBucks():
    global members_SIUBucks
    with open(SIUBUCKS_FILE, "w") as f:
        json.dump(members_SIUBucks, f)

def award_SIUBucks(user, amount):
    global members_SIUBucks
    user_id = str(user.id)  # Use the user's ID as the key in the dictionary
    if user_id not in members_SIUBucks:
        members_SIUBucks[user_id] = amount
    else:
        new_amount = members_SIUBucks.get(user_id) + amount
        members_SIUBucks.update({user_id: new_amount})

    save_SIUBucks()  # Save the updated data after modifying it

def remove_SIUBucks(user, amount):
    global members_SIUBucks
    user_id = str(user.id)  # Use the user's ID as the key in the dictionary
    if user_id not in members_SIUBucks:
        members_SIUBucks[user_id] = amount * -1
    else:
        new_amount = members_SIUBucks.get(user_id) - amount
        members_SIUBucks.update({user_id: new_amount})

    save_SIUBucks()  # Save the updated data after modifying it

@bot.command()
async def give(ctx, user: discord.Member, amount: int):
    if ctx.author.id == 700122491754119299:
        award_SIUBucks(user, amount)
        await ctx.send(f"{user} has been given {amount} SIUBucks!")  
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def remove(ctx, user: discord.Member, amount: int):
    if ctx.author.id == 700122491754119299:
        remove_SIUBucks(user, amount)
        await ctx.send(f"{user} has lost {amount} SIUBucks!")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def SIUBucks(ctx):
    global members_SIUBucks
    user_id = str(ctx.author.id)

    amount = members_SIUBucks.get(user_id, 0)

    await ctx.send(f"You have {amount} SIUBucks")

# iizam bot Shop
@bot.command()
async def shop(ctx):
    await ctx.send("Welcome to iizam bot shop!")
    await ctx.send("```\nThis is the first line.\nThis is the second line.\nThis is the third line.\n```")

# END of SIUBucks Functions #


# Command functions for mini games

@bot.command()
async def mathgame(ctx):
    global game_lock

    if game_lock:
        await ctx.send("Sorry, a game is already in progress. Please wait your turn.")
        return

    game_lock = True

    award_amount = await run_mathgame(ctx, bot)

    award_SIUBucks(ctx.author, award_amount)
    await ctx.send(f"You gained {award_amount} SIUBucks")

    game_lock = False

@bot.command()
async def numgame(ctx):
    global game_lock
    if game_lock:
        await ctx.send("Sorry, a game is already in progress. Please wait your turn.")
        return

    game_lock = True

    award_amount = await run_numgame(ctx, bot)
    
    award_SIUBucks(ctx.author, award_amount)
    
    game_lock = False


@bot.command()
async def blackjack(ctx):
    global members_SIUBucks
    global game_lock
    user_id = str(ctx.author.id)
    amount = 0

    if user_id in members_SIUBucks.keys(): 
        amount = members_SIUBucks.get(user_id)
    else:
        await ctx.send("You dont have enough SIUBucks to play")
        return

    if amount < 1:
        await ctx.send("You dont have enough SIUBucks to play")
        return

    game_lock = True
    await ctx.send(f"You currently have {amount} SIUBucks")
    await ctx.send(f"How much would you like to bet?")

    response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit())
    bet_amount = int(response.content)

    while bet_amount < 1 or bet_amount > amount:
        await ctx.send("Invalid bet amount, try again.")
        response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit())
        bet_amount = int(response.content)
    
    winner = await run_blackjack(ctx, bot)
    if winner == 1:
        await ctx.send(f"You lost {bet_amount} SIUBucks")
        remove_SIUBucks(ctx.author, bet_amount)
    elif winner == 2:
        await ctx.send(f"You won {bet_amount} SIUBucks")
        award_SIUBucks(ctx.author, bet_amount)
    elif winner == 3:
        await ctx.send("You won 0 SIUBucks")
    
    game_lock = False


# Commands for photo functions #
@bot.command()
async def sami(ctx):
    folder_path = "E:\sami"
    # Get all files in the folder (no extension filtering)
    all_files = os.listdir(folder_path)
    
    if not all_files:
        await ctx.send("No files found in the folder.")
        return

    # Randomly choose one file from the folder
    random_file = random.choice(all_files)
    
    # Create the full file path
    file_path = os.path.join(folder_path, random_file)

    # Check if the file is an image and send it as an embedded image
    if random_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await ctx.send(file=discord.File(file_path))
    else:
        # Send other file types as an attachment link
        await ctx.send(f"Here is a file: {random_file}", file=discord.File(file_path))

@bot.command()
async def japan(ctx):
    folder_path = "E:\japan"
    # Get all files in the folder (no extension filtering)
    all_files = os.listdir(folder_path)
    
    if not all_files:
        await ctx.send("No files found in the folder.")
        return

    # Randomly choose one file from the folder
    random_file = random.choice(all_files)
    
    # Create the full file path
    file_path = os.path.join(folder_path, random_file)

    # Check if the file is an image and send it as an embedded image
    if random_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await ctx.send(file=discord.File(file_path))
    else:
        # Send other file types as an attachment link
        await ctx.send(f"Here is a file: {random_file}", file=discord.File(file_path))

# END of photo functions #





def run_discord_bot():
    TOKEN = 'TOKEN'
    bot.run(TOKEN)

# Run the bot
run_discord_bot()
