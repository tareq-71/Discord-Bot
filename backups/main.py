import discord
from discord.ext import commands
import random
import time
import os
import json
from backups.gamelogic import run_mathgame, run_numgame, run_blackjack, run_guessgame
from gtts import gTTS


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

server_members = []
game_locks = {}
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
        activity=discord.Activity(type=discord.ActivityType.playing, name="boof"))
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

@bot.command()
async def serverbucks(ctx):
    global members_SIUBucks
    await ctx.send(members_SIUBucks.values())
    await ctx.send(members_SIUBucks.keys())

@bot.command()
async def teams(ctx, channel_name: str):
    # Find the guild (server) from the context
    guild = ctx.guild

    # Look for the specified voice channel
    channel = discord.utils.get(guild.voice_channels, name=channel_name)

    if not channel:
        await ctx.send(f"Voice channel '{channel_name}' not found.")
        return

    # Get all members in the channel
    members = channel.members
    if not members:
        await ctx.send(f"No members in the voice channel '{channel_name}'.")
        return

    AMAR = 294453266274582534
    AMRIT = 987456591869673584
    IIZAM_BOT = 1078061159539802203
    YOUSEF = 772294958086488104
    # Define the IDs of members to exclude
    excluded_ids = [AMAR, AMRIT, YOUSEF, IIZAM_BOT]  # Replace with actual member IDs

    # Filter out the excluded members
    filtered_members = [member for member in members if member.id not in excluded_ids]

    if not filtered_members:
        await ctx.send(f"All members in the voice channel '{channel_name}' are excluded.")
        return

    # Shuffle the filtered members list randomly
    random.shuffle(filtered_members)

    # Split the filtered members into two teams
    mid_index = len(filtered_members) // 2
    team1 = filtered_members[:mid_index]
    team2 = filtered_members[mid_index:]

    # Create a formatted message
    team1_names = ", ".join([member.name for member in team1])
    team2_names = ", ".join([member.name for member in team2])

    response = f"Team 1: {team1_names}\n" f"Team 2: {team2_names}"

    await ctx.send(response)
    
# iizam bot Shop
@bot.command()
async def shop(ctx):
    await ctx.send("Welcome to iizam bot shop!")
    await ctx.send("```\nThis is the first line.\nThis is the second line.\nThis is the third line.\n```")

# END of SIUBucks Functions #

# VOICE CHANNEL COMMANDS
# Map user-friendly surah names to file paths
QURAN_LIBRARY = {
    "fatiha": "Quran_surahs/001.mp3",   # Al-Fatiha
    "baqara": "Quran_surahs/002.mp3",  # Al-Baqara
    "imran": "Quran_surahs/003.mp3",   # Al-Imran
    "nisa": "Quran_surahs/004.mp3",    # An-Nisa
    "maidah": "Quran_surahs/005.mp3",  # Al-Ma'idah
    "anam": "Quran_surahs/006.mp3",    # Al-An'am
    "araf": "Quran_surahs/007.mp3",    # Al-A'raf
    "anfal": "Quran_surahs/008.mp3",   # Al-Anfal
    "tawba": "Quran_surahs/009.mp3",   # At-Tawba
    "yunus": "Quran_surahs/010.mp3",   # Yunus
    "hud": "Quran_surahs/011.mp3",     # Hud
    "yusuf": "Quran_surahs/012.mp3",   # Yusuf
    "rad": "Quran_surahs/013.mp3",     # Ar-Ra'd
    "ibrahim": "Quran_surahs/014.mp3", # Ibrahim
    "hijr": "Quran_surahs/015.mp3",    # Al-Hijr
    "nahl": "Quran_surahs/016.mp3",    # An-Nahl
    "isra": "Quran_surahs/017.mp3",    # Al-Isra
    "kahf": "Quran_surahs/018.mp3",    # Al-Kahf
    "maryam": "Quran_surahs/019.mp3",  # Maryam
    "taha": "Quran_surahs/020.mp3",    # Ta-Ha
    "anbiya": "Quran_surahs/021.mp3",  # Al-Anbiya
    "hajj": "Quran_surahs/022.mp3",    # Al-Hajj
    "muminun": "Quran_surahs/023.mp3", # Al-Mu'minun
    "nur": "Quran_surahs/024.mp3",     # An-Nur
    "furqan": "Quran_surahs/025.mp3",  # Al-Furqan
    "shuara": "Quran_surahs/026.mp3",  # Ash-Shu'ara
    "naml": "Quran_surahs/027.mp3",    # An-Naml
    "qasas": "Quran_surahs/028.mp3",   # Al-Qasas
    "ankabut": "Quran_surahs/029.mp3", # Al-Ankabut
    "rum": "Quran_surahs/030.mp3",     # Ar-Rum
    "luqman": "Quran_surahs/031.mp3",  # Luqman
    "sajda": "Quran_surahs/032.mp3",   # As-Sajda
    "ahzab": "Quran_surahs/033.mp3",   # Al-Ahzab
    "saba": "Quran_surahs/034.mp3",    # Saba
    "fatir": "Quran_surahs/035.mp3",   # Fatir
    "yaseen": "Quran_surahs/036.mp3",  # Ya-Sin
    "saffat": "Quran_surahs/037.mp3",  # As-Saffat
    "sad": "Quran_surahs/038.mp3",     # Sad
    "zumar": "Quran_surahs/039.mp3",   # Az-Zumar
    "ghafir": "Quran_surahs/040.mp3",  # Ghafir
    "fussilat": "Quran_surahs/041.mp3",# Fussilat
    "shura": "Quran_surahs/042.mp3",   # Ash-Shura
    "zukhruf": "Quran_surahs/043.mp3", # Az-Zukhruf
    "dukhan": "Quran_surahs/044.mp3",  # Ad-Dukhan
    "jathiya": "Quran_surahs/045.mp3", # Al-Jathiya
    "ahqaf": "Quran_surahs/046.mp3",   # Al-Ahqaf
    "muhammad": "Quran_surahs/047.mp3",# Muhammad
    "fath": "Quran_surahs/048.mp3",    # Al-Fath
    "hujurat": "Quran_surahs/049.mp3", # Al-Hujurat
    "qaf": "Quran_surahs/050.mp3",     # Qaf
    "dhariyat": "Quran_surahs/051.mp3",# Adh-Dhariyat
    "tur": "Quran_surahs/052.mp3",     # At-Tur
    "najm": "Quran_surahs/053.mp3",    # An-Najm
    "qamar": "Quran_surahs/054.mp3",   # Al-Qamar
    "rahman": "Quran_surahs/055.mp3",  # Ar-Rahman
    "waqia": "Quran_surahs/056.mp3",   # Al-Waqia
    "hadid": "Quran_surahs/057.mp3",   # Al-Hadid
    "mujadila": "Quran_surahs/058.mp3",# Al-Mujadila
    "hashr": "Quran_surahs/059.mp3",   # Al-Hashr
    "mumtahina": "Quran_surahs/060.mp3",# Al-Mumtahina
    "saff": "Quran_surahs/061.mp3",    # As-Saff
    "jumuah": "Quran_surahs/062.mp3",  # Al-Jumuah
    "munafiqun": "Quran_surahs/063.mp3",# Al-Munafiqun
    "taghabun": "Quran_surahs/064.mp3",# At-Taghabun
    "talaq": "Quran_surahs/065.mp3",   # At-Talaq
    "tahrim": "Quran_surahs/066.mp3",  # At-Tahrim
    "mulk": "Quran_surahs/067.mp3",    # Al-Mulk
    "qalam": "Quran_surahs/068.mp3",   # Al-Qalam
    "haqqa": "Quran_surahs/069.mp3",   # Al-Haqqa
    "maarij": "Quran_surahs/070.mp3",  # Al-Maarij
    "nuh": "Quran_surahs/071.mp3",     # Nuh
    "jinn": "Quran_surahs/072.mp3",    # Al-Jinn
    "muzammil": "Quran_surahs/073.mp3",# Al-Muzammil
    "mudathir": "Quran_surahs/074.mp3",# Al-Mudathir
    "qiyama": "Quran_surahs/075.mp3",  # Al-Qiyama
    "insan": "Quran_surahs/076.mp3",   # Al-Insan
    "mursalat": "Quran_surahs/077.mp3",# Al-Mursalat
    "naba": "Quran_surahs/078.mp3",    # An-Naba
    "naziat": "Quran_surahs/079.mp3",  # An-Naziat
    "abasa": "Quran_surahs/080.mp3",   # Abasa
    "takwir": "Quran_surahs/081.mp3",  # At-Takwir
    "infitar": "Quran_surahs/082.mp3", # Al-Infitar
    "mutaffifin": "Quran_surahs/083.mp3",# Al-Mutaffifin
    "inshiqaq": "Quran_surahs/084.mp3",# Al-Inshiqaq
    "burooj": "Quran_surahs/085.mp3",  # Al-Burooj
    "tariq": "Quran_surahs/086.mp3",   # At-Tariq
    "ala": "Quran_surahs/087.mp3",     # Al-Ala
    "ghashiya": "Quran_surahs/088.mp3",# Al-Ghashiya
    "fajr": "Quran_surahs/089.mp3",    # Al-Fajr
    "balad": "Quran_surahs/090.mp3",   # Al-Balad
    "shams": "Quran_surahs/091.mp3",   # Ash-Shams
    "layl": "Quran_surahs/092.mp3",    # Al-Layl
    "duha": "Quran_surahs/093.mp3",    # Ad-Duha
    "sharh": "Quran_surahs/094.mp3",   # Al-Inshirah (Ash-Sharh)
    "tin": "Quran_surahs/095.mp3",     # At-Tin
    "alaq": "Quran_surahs/096.mp3",    # Al-Alaq
    "qadr": "Quran_surahs/097.mp3",    # Al-Qadr
    "bayyina": "Quran_surahs/098.mp3", # Al-Bayyina
    "zilzal": "Quran_surahs/099.mp3",  # Az-Zalzala
    "adiyat": "Quran_surahs/100.mp3",  # Al-Adiyat
    "qariah": "Quran_surahs/101.mp3",  # Al-Qaria
    "takathur": "Quran_surahs/102.mp3",# At-Takathur
    "asr": "Quran_surahs/103.mp3",     # Al-Asr
    "humazah": "Quran_surahs/104.mp3", # Al-Humazah
    "fil": "Quran_surahs/105.mp3",     # Al-Fil
    "quraish": "Quran_surahs/106.mp3", # Quraysh
    "maun": "Quran_surahs/107.mp3",    # Al-Ma'un
    "kawthar": "Quran_surahs/108.mp3", # Al-Kawthar
    "kafirun": "Quran_surahs/109.mp3", # Al-Kafirun
    "nasr": "Quran_surahs/110.mp3",    # An-Nasr
    "masad": "Quran_surahs/111.mp3",   # Al-Masad
    "ikhlas": "Quran_surahs/112.mp3",  # Al-Ikhlas
    "falaq": "Quran_surahs/113.mp3",   # Al-Falaq
    "nas": "Quran_surahs/114.mp3"      # An-Nas
}

# Map short names to full names
SURAH_NAMES = {
    "fatiha": "Al-Fatiha",
    "baqara": "Al-Baqara",
    "imran": "Al-Imran",
    "nisa": "An-Nisa",
    "maidah": "Al-Ma'idah",
    "anam": "Al-An'am",
    "araf": "Al-A'raf",
    "anfal": "Al-Anfal",
    "tawba": "At-Tawba",
    "yunus": "Yunus",
    "hud": "Hud",
    "yusuf": "Yusuf",
    "rad": "Ar-Ra'd",
    "ibrahim": "Ibrahim",
    "hijr": "Al-Hijr",
    "nahl": "An-Nahl",
    "isra": "Al-Isra",
    "kahf": "Al-Kahf",
    "maryam": "Maryam",
    "taha": "Ta-Ha",
    "anbiya": "Al-Anbiya",
    "hajj": "Al-Hajj",
    "muminun": "Al-Mu'minun",
    "nur": "An-Nur",
    "furqan": "Al-Furqan",
    "shuara": "Ash-Shu'ara",
    "naml": "An-Naml",
    "qasas": "Al-Qasas",
    "ankabut": "Al-Ankabut",
    "rum": "Ar-Rum",
    "luqman": "Luqman",
    "sajda": "As-Sajda",
    "ahzab": "Al-Ahzab",
    "saba": "Saba",
    "fatir": "Fatir",
    "yaseen": "Ya-Sin",
    "saffat": "As-Saffat",
    "sad": "Sad",
    "zumar": "Az-Zumar",
    "ghafir": "Ghafir",
    "fussilat": "Fussilat",
    "shura": "Ash-Shura",
    "zukhruf": "Az-Zukhruf",
    "dukhan": "Ad-Dukhan",
    "jathiya": "Al-Jathiya",
    "ahqaf": "Al-Ahqaf",
    "muhammad": "Muhammad",
    "fath": "Al-Fath",
    "hujurat": "Al-Hujurat",
    "qaf": "Qaf",
    "dhariyat": "Adh-Dhariyat",
    "tur": "At-Tur",
    "najm": "An-Najm",
    "qamar": "Al-Qamar",
    "rahman": "Ar-Rahman",
    "waqia": "Al-Waqia",
    "hadid": "Al-Hadid",
    "mujadila": "Al-Mujadila",
    "hashr": "Al-Hashr",
    "mumtahina": "Al-Mumtahina",
    "saff": "As-Saff",
    "jumuah": "Al-Jumuah",
    "munafiqun": "Al-Munafiqun",
    "taghabun": "At-Taghabun",
    "talaq": "At-Talaq",
    "tahrim": "At-Tahrim",
    "mulk": "Al-Mulk",
    "qalam": "Al-Qalam",
    "haqqa": "Al-Haqqa",
    "maarij": "Al-Maarij",
    "nuh": "Nuh",
    "jinn": "Al-Jinn",
    "muzammil": "Al-Muzammil",
    "mudathir": "Al-Mudathir",
    "qiyama": "Al-Qiyama",
    "insan": "Al-Insan",
    "mursalat": "Al-Mursalat",
    "naba": "An-Naba",
    "naziat": "An-Naziat",
    "abasa": "Abasa",
    "takwir": "At-Takwir",
    "infitar": "Al-Infitar",
    "mutaffifin": "Al-Mutaffifin",
    "inshiqaq": "Al-Inshiqaq",
    "burooj": "Al-Burooj",
    "tariq": "At-Tariq",
    "ala": "Al-Ala",
    "ghashiya": "Al-Ghashiya",
    "fajr": "Al-Fajr",
    "balad": "Al-Balad",
    "shams": "Ash-Shams",
    "layl": "Al-Layl",
    "duha": "Ad-Duha",
    "sharh": "Al-Inshirah",
    "tin": "At-Tin",
    "alaq": "Al-Alaq",
    "qadr": "Al-Qadr",
    "bayyina": "Al-Bayyina",
    "zilzal": "Az-Zalzala",
    "adiyat": "Al-Adiyat",
    "qariah": "Al-Qaria",
    "takathur": "At-Takathur",
    "asr": "Al-Asr",
    "humazah": "Al-Humazah",
    "fil": "Al-Fil",
    "quraish": "Quraysh",
    "maun": "Al-Ma'un",
    "kawthar": "Al-Kawthar",
    "kafirun": "Al-Kafirun",
    "nasr": "An-Nasr",
    "masad": "Al-Masad",
    "ikhlas": "Al-Ikhlas",
    "falaq": "Al-Falaq",
    "nas": "An-Nas",
}

CURRENT_SURAH = ""

# Mapping of user IDs (or usernames) to audio file paths
user_audio_files = {
    692408240511778876: "members_audios/niz.mp3",
    700122491754119299: "members_audios/iizam.mp3",
    751468568960303206: "members_audios/amer.mp3",
    1194421350887079946: "members_audios/yazen.mp3",
    730973534150459454: "members_audios/zane.mp3",
    549710097681481742: "members_audios/jamal.mp3",
    1013461708238508222: "members_audios/laith.mp3",
    672650948610490378: "members_audios/sigma.mp3",
}

# Default volume level (1.0 = original, 0.5 = 50%, 2.0 = 200%)
DEFAULT_VOLUME = 1.0

@bot.command()
async def set_volume(ctx, volume: float):
    """
    Sets the playback volume (e.g., 0.5 for 50%, 1.0 for 100%, 2.0 for 200%).
    """
    global DEFAULT_VOLUME
    if 0.0 < volume <= 2.0:  # Ensure volume is within a reasonable range
        DEFAULT_VOLUME = volume
        await ctx.send(f"Volume set to {volume * 100:.0f}%.")
    else:
        await ctx.send("Volume must be between 0.1 and 2.0.")

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Plays a specific audio file with adjustable volume depending on the user who joins the voice channel.
    """
    if member.bot:
        return  # Ignore bots

    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    if voice_client and voice_client.channel == after.channel and before.channel != after.channel:
        user_audio_file = user_audio_files.get(member.id)  # Get the audio file for this user
        if user_audio_file and os.path.exists(user_audio_file):
            # Use FFmpeg with volume adjustment
            ffmpeg_options = f"-filter:a 'volume={DEFAULT_VOLUME}'"
            source = discord.FFmpegPCMAudio(user_audio_file, options=ffmpeg_options)
            if not voice_client.is_playing():
                voice_client.play(source)
        elif user_audio_file:
            print(f"Audio file '{user_audio_file}' for user '{member}' not found.")
        else:
            print(f"No specific audio file assigned for user '{member}'.")

@bot.command()
async def join(ctx, *, channel_name: str = None):
    """
    Joins the specified voice channel by name, or the user's current channel if no name is provided.
    """
    guild = ctx.guild
    if channel_name:
        channel = discord.utils.get(guild.voice_channels, name=channel_name)
        if channel:
            await channel.connect()
            await ctx.send(f"Joined the voice channel: {channel_name}")
        else:
            await ctx.send(f"Voice channel '{channel_name}' not found.")
    elif ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined your voice channel: {channel.name}")
    else:
        await ctx.send("You need to specify a channel name or be in a voice channel yourself.")

async def play_next_in_order(ctx, voice_client):
    """
    Plays the next surah in the order of QURAN_LIBRARY.
    """
    global CURRENT_SURAH
    global surah_file_path
    global surah_name_path

    # Check if there is another surah to play
    if not surah_name_path:
        return  # No more surahs to play

    # Pop the next surah to play
    next_name = surah_name_path.pop(0)
    next_path = surah_file_path.pop(0)

    if os.path.exists(next_path):
        CURRENT_SURAH = next_name
        # Stop any audio currently playing
        if voice_client.is_playing():
            voice_client.stop()

        # Start playing the new surah
        voice_client.play(
            discord.FFmpegPCMAudio(next_path),
            after=lambda error: play_next_in_order(ctx, voice_client)
        )

@bot.command()
async def surah(ctx, surah_name: str):
    """
    Stops the current playback (if any) and starts playing the specified surah,
    then continues with the next surah in order.
    """

    global CURRENT_SURAH
    global surah_file_path
    global surah_name_path

    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.send("I am not in a voice channel. Use !join <vc name> to add me.")
        return


    surah_name = surah_name.lower()
    if surah_name not in QURAN_LIBRARY:
        await ctx.send(f"'{surah_name}' is not available in the library.")
        return
    
    if voice_client.is_playing():
        voice_client.stop()

    await ctx.send(f"Now playing: {SURAH_NAMES[surah_name]}")
    # Reset iterator starting from the given surah
    keys = list(QURAN_LIBRARY.keys())
    start_index = keys.index(surah_name)
    surah_file_path = list(QURAN_LIBRARY.values())[start_index:]
    surah_name_path = list(QURAN_LIBRARY.keys())[start_index:]

    await play_next_in_order(ctx, voice_client)


@bot.command()
async def surahs(ctx):
    # Create a neat list of surah names, joined by newline characters
    surah_list = "\n".join(f"{index + 1}. {value}" for index, value in enumerate(SURAH_NAMES.values()))
    
    # Send the list as a single message
    await ctx.send(f"List of Surahs:\n{surah_list}")

@bot.command()
async def currentsurah(ctx):
    if ctx.voice_client.is_playing():
        await ctx.send(f"Current Surah: {SURAH_NAMES[CURRENT_SURAH]}.")
    else:
        await ctx.send("No current surah is playing.")

@bot.command()
async def pause(ctx):
    """
    Pauses the currently playing audio.
    """
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Audio paused.")
    else:
        await ctx.send("No audio is currently playing.")

@bot.command()
async def resume(ctx):
    """
    Resumes the currently paused audio.
    """
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Audio resumed.")
    else:
        await ctx.send("No audio is currently paused.")

@bot.command()
async def sayV(ctx, *, text: str):
    if ctx.voice_client:
        # Generate TTS audio file from text input
        tts = gTTS(text=text, lang='en')
        tts.save("tts_output.mp3")

        # Play the mp3 audio in the voice channel
        voice_client = ctx.voice_client
        voice_client.play(discord.FFmpegPCMAudio("tts_output.mp3"), after=lambda e: os.remove("tts_output.mp3"))
    else:
        await ctx.send("I'm not in a voice channel. Use `!joinV` to invite me to one.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

# END OF VOICE CHANNEL


# Command functions for mini games

@bot.command()
async def mathgame(ctx):
    global game_locks
    user_id = ctx.author.id

    if game_locks.get(user_id, False):
        await ctx.send("You already have a game in progress. Both running games stopped.")
        return
    
    game_locks[user_id] = True

    try:
        award_amount = await run_mathgame(ctx, bot)
        award_SIUBucks(ctx.author, award_amount)
        await ctx.send(f"You gained {award_amount} SIUBucks")
    except Exception as e:
        await ctx.send("You took to long to respond or an error occurred during the game. Please try again.")
        print(f"Error: {e}")  # Optional: log the error for debugging
    finally:
        game_locks[user_id] = False

@bot.command()
async def numgame(ctx):
    global game_locks
    user_id = ctx.author.id

    if game_locks.get(user_id, False):
        await ctx.send("You already have a game in progress. Both running games stopped.")
        return
    
    game_locks[user_id] = True

    try:
        award_amount = await run_numgame(ctx, bot)
        award_SIUBucks(ctx.author, award_amount)
    except Exception as e:
        await ctx.send("You took to long to respond or an error occurred during the game. Please try again.")
        print(f"Error: {e}")  # Optional: log the error for debugging
    finally:
        game_locks[user_id] = False

@bot.command()
async def blackjack(ctx):
    global members_SIUBucks
    global game_locks
    user_id = ctx.author.id
    amount = 0

    if game_locks.get(user_id, False):
        await ctx.send("You already have a game in progress. Both running games stopped.")
        return
    
    game_locks[user_id] = True  # Lock this user



    if user_id in members_SIUBucks.keys(): 
        amount = members_SIUBucks.get(str(user_id))
    else:
        await ctx.send("You dont have enough SIUBucks to play")
        return

    if amount < 1:
        await ctx.send("You dont have enough SIUBucks to play")
        return

    
    await ctx.send(f"You currently have {amount} SIUBucks")
    await ctx.send(f"How much would you like to bet?")

    try:

        response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit(), timeout=30)
        bet_amount = int(response.content)

        while bet_amount < 1 or bet_amount > amount:
            await ctx.send("Invalid bet amount, try again.")
            response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit(), timeout=30)
            bet_amount = int(response.content)
        
        winner = await run_blackjack(ctx, bot)
    except Exception as e:
        await ctx.send("You took to long to respond or an error occurred during the game. Please try again.")
        print(f"Error: {e}")  # Optional: log the error for debugging
    finally:
        if winner == 1:
            await ctx.send(f"You lost {bet_amount} SIUBucks")
            remove_SIUBucks(ctx.author, bet_amount)
        elif winner == 2:
            await ctx.send(f"You won {bet_amount} SIUBucks")
            award_SIUBucks(ctx.author, bet_amount)
        elif winner == 3:
            await ctx.send("You won 0 SIUBucks")
        
        game_locks[user_id] = False

@bot.command()
async def guessgame(ctx):
    global game_locks
    user_id = ctx.author.id

    if game_locks.get(user_id, False):
        await ctx.send("You already have a game in progress. Please finish it before starting a new one.")
        return
    
    game_locks[user_id] = True  # Lock this user

    try:
        await run_guessgame(ctx, bot)

        award_SIUBucks(ctx.author, 2)
        await ctx.send("You get 2 SIUBucks")
    except Exception as e:
        await ctx.send("You took to long to respond or an error occurred during the game. Please try again.")
        print(f"Error: {e}")  # Optional: log the error for debugging
    finally:
        game_locks[user_id] = False

# END of command functions

# Commands for photo functions #
@bot.command()
async def sami(ctx):
    folder_path = "sami"
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
    folder_path = "japan"
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
    TOKEN = 'DISCORD_BOT_TOKEN'
    bot.run(TOKEN)

# Run the bot
run_discord_bot()
 