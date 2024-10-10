import random
import discord
from discord.ext import commands
from discord import app_commands
import responses
import requests
import asyncio
import datetime
import time
import sqlite3


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
TARGET_CHANNEL_ID = 708432115984891984

#---Bots online status---#
async def setup(bot):
    activity = discord.Activity(type=discord.ActivityType.playing, name="!mathgame")
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    await bot.change_presence(
        #status=discord.Status.dnd,
        activity=discord.Game('!mathgame'))
    print(f'{bot.user} is now running!')

#---Random events or commands---------------------------------------------------------------#
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

@bot.command()
async def define(ctx, term):
    response = requests.get(f"https://api.urbandictionary.com/v0/define?term={term}")
    data = response.json()
    if len(data['list']) > 0:
        definition = data['list'][0]['definition']
        example = data['list'][0]['example']
        await ctx.send(f"**{term}:**\n\nDefinition: {definition}\n\nExample: {example}")
    else:
        await ctx.send("No definition found.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def timeout(ctx, member: discord.Member, duration: float, *, reason=None):
    # Replace 'Muted' with the name you want for the muted role
    role = discord.utils.get(ctx.guild.roles, name='Muted')

    # If the 'Muted' role doesn't exist, create it
    if role is None:
        role = await ctx.guild.create_role(name='Muted')

        # Configure the permissions for the 'Muted' role (Optional)
        # You can modify this based on your server's specific requirements
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, send_messages=False)

    # Convert the duration from hours to seconds
    duration_seconds = duration * 3600

    await member.add_roles(role, reason=reason)
    
    # Get the target channel where the messages will be sent
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)

    if target_channel:
        await target_channel.send(f'{member.mention} has been put in timeout for {duration} hour(s) due to {reason}.')
    else:
        await ctx.send("The target channel doesn't exist or the bot can't access it.")

    await ctx.send(f'{member.mention} has been muted for {duration} hour(s).')

    # Wait for the duration, then remove the mute role
    await asyncio.sleep(duration_seconds)

    # Check if the user is still in the server and the role still exists
    if member in ctx.guild.members and role in member.roles:
        await member.remove_roles(role)
        await target_channel.send(f'{member.mention} has been unmuted.')

@timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid arguments. Please use the command as follows: `!timeout @user duration_in_hours [reason]`")

@bot.command()
async def remindme(ctx, duration, *, reminder):
    time_units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400
    }

    duration_value = int(duration[:-1])
    duration_unit = duration[-1]

    if duration_unit not in time_units:
        await ctx.send("Invalid duration unit. Use s, m, h, or d.")
        return

    total_seconds = duration_value * time_units[duration_unit]
    await ctx.send(f"Reminder set for {duration}.")

    await asyncio.sleep(total_seconds)
    await ctx.send(f"Reminder: {reminder} ({duration} ago)")

@bot.command()
async def insult(ctx, user: discord.Member):
    response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
    data = response.json()
    insult = data["insult"]
    await ctx.send(f"{user.mention}, {insult}")


#---------Code for random member generator and yes/no answers---# 
@bot.command(aliases=['name', 'question'])
async def eightball(ctx, *, question):
    if ctx.invoked_with in ['name']:
        responses = ["iizam", "taco", "papi sah", "sami", "yazen", "ozmin", "kerem", "niz", "kinglightning20", "silly girl",
                 "aboody",
                 "amiin", "big clock yamin", "bigjim", "bobdi", "hadyKwiek", "korga", "laith", "mr.Mumz", "sosa",
                 "faris",
                 "zeid", "duckgang24", "abdul"]
        
    elif ctx.invoked_with in ['question']:
        responses = ['yes', 'no']

    await ctx.send(f"**Question: ** {question}\n**Answer: **{random.choice(responses)}")


#-------Code for scheduling message entries --------------------------------------------------------------------------#
@bot.command()
async def schedule(ctx, date_str: str, time_str: str, am_pm: str, channel: discord.TextChannel, *, message: str):
    try:
        datetime_format = "%Y-%m-%d %I:%M %p"  # Using 12-hour format with AM/PM
        scheduled_time = datetime.datetime.strptime(f"{date_str} {time_str} {am_pm}", datetime_format)

        # Calculate the timezone offset for Eastern Time (Columbus, Ohio)
        current_time = datetime.datetime.now()
        scheduled_time = scheduled_time.replace(tzinfo=current_time.tzinfo)  # Use the current timezone

        if scheduled_time <= current_time:
            await ctx.send("Please provide a valid future time.")
            return

        time_difference = (scheduled_time - current_time).total_seconds()

        await ctx.send(f"Message scheduled to be sent in {time_difference:.2f} seconds.")

        await asyncio.sleep(time_difference)
        await channel.send(f"{message}")

    except ValueError:
        await ctx.send("Dont use this command")


#-------Code for sending message entires-------------------------------#
@bot.command()
async def say(ctx, channel: discord.TextChannel, *, message: str):
    await channel.send(message)



#-----------Code for guessgame---------#
game_in_progress = False

@bot.command()
async def guessgame(ctx):
    global game_in_progress

    if game_in_progress:
        await ctx.send(
            "Sorry, a game is already in progress. Please wait for the current game to finish."
        )
        return

    try:

        game_lock = asyncio.Lock()
        # Acquire the lock to start the game
        async with game_lock:
            game_in_progress = True

        question1 = "Is your person bad at soccer for there age?"
        question2 = "Is your person an OSU student?"
        question3 = "Is your person Stupid?"
        question4 = "Is your person in highschool/middleschool?"
        question5 = "Did your person go on the japan trip?"
        question6 = "Does your person have a little brother?"
        question7 = "Is your person an Anime fan?"
        question8 = "Can your person bench a 185+?"
        question9 = "Is your person fat or have previously been fat?"
        question10 = "Is your person bad at video games?"
        question11 = "Is your person short?"
        question12 = "Is your person from Palestine?"
        question13 = "Is your person bad at basketball?"

        players = [
            "Tareq",
            "Amar",
            "Aymen",
            "Ozmin",
            "Sami",
            "Shareef",
            "Niz",
            "Abdulla",
            "Jamal",
            "Kerem",
            "Laith",
            "Amer",
            "Zeid",
            "Hady",
        ]

        player_scores = {
            "Tareq": 0,
            "Amar": 0,
            "Aymen": 0,
            "Ozmin": 0,
            "Sami": 0,
            "Shareef": 0,
            "Niz": 0,
            "Abdulla": 0,
            "Jamal": 0,
            "Kerem": 0,
            "Amer": 0,
            "Zeid": 0,
            "Laith": 0,
            "Hady": 0,
        }

        questions = [
            question1,
            question2,
            question3,
            question4,
            question5,
            question6,
            question7,
            question8,
            question9,
            question10,
            question11,
            question12,
            question13,
        ]

        await ctx.send(
            "Welcome to SIU guessing game, I will ask you questions and try to guess who you are thinking of."
        )

        while (
            len(players) > 1
        ):  # Keep the game loop running as long as there is more than one player left
            random_question = random.choice(questions)
            await ctx.send(random_question)

            game_completed = (
                False  # Flag to track if the game was successfully completed
            )

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                response = await bot.wait_for(
                    "message", check=check, timeout=30
                )  # Wait for 30 seconds for a response
                userInput = response.content.lower()

                while userInput not in ["yes", "no"]:
                    await ctx.send("Invalid response, enter 'yes' or 'no'.")
                    try:
                        response = await bot.wait_for(
                            "message", check=check, timeout=30
                        )
                        userInput = response.content.lower()
                    except asyncio.TimeoutError:
                        await ctx.send(
                            "You took too long to respond. The game has ended."
                        )
                        return

                if random_question == question1:
                    if userInput == "yes":
                        player_scores["Niz"] += 1
                        player_scores["Jamal"] += 1
                        player_scores["Ozmin"] += 1
                        player_scores["Kerem"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                    else:
                        if "Niz" in players:
                            players.remove("Niz")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question2:
                    if userInput == "yes":
                        player_scores["Tareq"] += 1
                        player_scores["Amar"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Ozmin"] += 1
                        player_scores["Niz"] += 1
                        player_scores["Shareef"] += 1

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                    else:
                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Niz" in players:
                            players.remove("Niz")

                elif random_question == question3:
                    if userInput == "yes":
                        player_scores["Niz"] += 1
                        player_scores["Jamal"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Aymen"] += 1
                        player_scores["Kerem"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                    else:
                        if "Niz" in players:
                            players.remove("Niz")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question4:
                    if userInput == "yes":
                        player_scores["Amer"] += 1
                        player_scores["Hady"] += 1
                        player_scores["Zeid"] += 1
                        player_scores["Niz"] += 1
                        player_scores["Laith"] += 1

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Shareef" in players:
                            players.remove("Shareef")

                    else:
                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                        if "Niz" in players:
                            players.remove("Niz")

                elif random_question == question5:
                    if userInput == "yes":
                        player_scores["Tareq"] += 1
                        player_scores["Amar"] += 1
                        player_scores["Aymen"] += 1
                        player_scores["Ozmin"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Kerem"] += 1

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                    else:
                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                elif random_question == question6:
                    if userInput == "yes":
                        player_scores["Amar"] += 1
                        player_scores["Jamal"] += 1
                        player_scores["Ozmin"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Shareef"] += 1

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                    else:
                        if "Sami" in players:
                            players.remove("Sami")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question7:
                    if userInput == "yes":
                        player_scores["Tareq"] += 1
                        player_scores["Amar"] += 1
                        player_scores["Aymen"] += 1
                        player_scores["Niz"] += 1
                        player_scores["Jamal"] += 1

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Hady" in players:
                            players.remove("Hady")

                    else:
                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                elif random_question == question8:
                    if userInput == "yes":
                        player_scores["Ozmin"] += 1
                        player_scores["Abdulla"] += 1
                        player_scores["Amar"] += 1
                        player_scores["Aymen"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                    else:
                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                elif random_question == question9:
                    if userInput == "yes":
                        player_scores["Ozmin"] += 1
                        player_scores["Jamal"] += 1
                        player_scores["Niz"] += 1
                        player_scores["Shareef"] += 1
                        player_scores["Abdulla"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                    else:
                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                elif random_question == question10:
                    if userInput == "yes":
                        player_scores["Ozmin"] += 1
                        player_scores["Shareef"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Abdulla"] += 1
                        player_scores["Kerem"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                    else:
                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question11:
                    if userInput == "yes":
                        player_scores["Ozmin"] += 1
                        player_scores["Kerem"] += 1
                        player_scores["Aymen"] += 1
                        player_scores["Abdulla"] += 1
                        player_scores["Niz"] += 1

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Zeid" in players:
                            players.remove("Zeid")

                    else:
                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question12:
                    if userInput == "yes":
                        player_scores["Tareq"] += 1
                        player_scores["Amar"] += 1
                        player_scores["Jamal"] += 1
                        player_scores["Sami"] += 1
                        player_scores["Abdulla"] += 1

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Shareef" in players:
                            players.remove("Shareef")

                    else:
                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Laith" in players:
                            players.remove("Laith")

                        if "Zeid" in players:
                            players.remove("Zeid")

                        if "Hady" in players:
                            players.remove("Hady")

                elif random_question == question13:
                    if userInput == "yes":
                        if "Jamal" in players:
                            players.remove("Jamal")

                        if "Tareq" in players:
                            players.remove("Tareq")

                        if "Amar" in players:
                            players.remove("Amar")

                        if "Abdulla" in players:
                            players.remove("Abdulla")

                        if "Shareef" in players:
                            players.remove("Shareef")

                        if "Amer" in players:
                            players.remove("Amer")

                        if "Zeid" in players:
                            players.remove("Zeid")

                    else:
                        if "Laith" in players:
                            players.remove("Laith")

                        if "Hady" in players:
                            players.remove("Hady")

                        if "Niz" in players:
                            players.remove("Niz")

                        if "Aymen" in players:
                            players.remove("Aymen")

                        if "Sami" in players:
                            players.remove("Sami")

                        if "Kerem" in players:
                            players.remove("Kerem")

                        if "Ozmin" in players:
                            players.remove("Ozmin")

                questions.remove(
                    random_question
                )  # Remove the selected question from the list

                game_completed = (
                    True  # Set the flag to indicate the game was completed successfully
                )

            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. The game has ended.")
                break

            if not game_completed:
                break

    finally:
        game_in_progress = False

    if len(players) == 1:
        await ctx.send("I have guessed your person! It's " + players[0] + "!")
    else:
        await ctx.send("I couldn't guess your person.")


#---------Code for mathgame--------------------------------------------#

# Create a connection to the SQLite database
connection = sqlite3.connect("leaderboard.db")
cursor = connection.cursor()

# Create a table to store user scores if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS leaderboard (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        score INTEGER,
        high_score INTEGER DEFAULT 0
    )
"""
)
connection.commit()

# Create a lock to prevent multiple users from playing concurrently
game_lock = False


def generate_problem():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operator = random.choice(["+", "-", "*", "/"])
    problem = f"{num1} {operator} {num2}"
    correct_answer = eval(problem)
    
    if operator == "/":
        return problem, correct_answer, 3
    elif operator == "*":
        return problem, correct_answer, 2
    else:
        return problem, correct_answer, 1



@bot.command()
async def mathgame(ctx):
    global game_lock

    if game_lock:
        await ctx.send("Sorry, a game is already in progress. Please wait your turn.")
        return

    game_lock = True

    await ctx.send("Welcome to the Math Problem Solver Game!")
    await ctx.send("You have 60 seconds to solve as many math problems as you can.")
    await ctx.send("Type your answer as a number round your answer to two decimal places when required.")
    await ctx.send("Division worth: 3 points, Multiplication worth: 2 points, Addition/Subtraction worth: 1 points and -1 for incorrect answer.")
    await ctx.send("DO NOT CHEAT OR USE CALCULATOR")

    score = 0
    start_time = time.time()
    end_time = start_time + 60

    while time.time() < end_time:
        problem, correct_answer, points = generate_problem()
        await ctx.send(f"Problem: {problem}")

        try:
            msg = await bot.wait_for(
                "message", check=lambda message: message.author == ctx.author
            )
            player_answer = float(msg.content)
            if round(player_answer, 2) == round(correct_answer, 2):
                score += points
                await ctx.send(f"Correct! You earned {points} point(s).\n")
            else:
                await ctx.send("Incorrect. You lose 1 point.\n")
                score = score - 1
        except ValueError:
            await ctx.send("Invalid input. You lose 1 point.\n")
            score = score - 1

    await ctx.send("Time's up!")
    await ctx.send(f"Your final score: {score}")

    cursor.execute(
        "SELECT high_score FROM leaderboard WHERE user_id = ?", (ctx.author.id,)
    )
    existing_high_score = cursor.fetchone()

    if existing_high_score is None or score > existing_high_score[0]:
        cursor.execute(
            "INSERT OR REPLACE INTO leaderboard (user_id, username, score, high_score) VALUES (?, ?, ?, ?)",
            (ctx.author.id, ctx.author.name, score, score),
        )
        connection.commit()

    game_lock = False


@bot.command()
async def leaderboard(ctx):
    cursor.execute(
        "SELECT username, high_score FROM leaderboard ORDER BY high_score DESC"
    )
    rows = cursor.fetchall()

    if not rows:
        await ctx.send("No scores available.")
    else:
        leaderboard_text = "Leaderboard:\n"
        for rank, (username, high_score) in enumerate(rows, start=1):
            leaderboard_text += f"{rank}. {username} - {high_score} points\n"
        await ctx.send(leaderboard_text)


@bot.command()
async def resetleaderboard(ctx):
    cursor.execute("DELETE FROM leaderboard")
    connection.commit()
    await ctx.send("Leaderboard has been reset.")

def run_discord_bot():
    TOKEN = 'TOKEN'
    bot.run(TOKEN)

run_discord_bot()
