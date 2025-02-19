import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

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

# Keeps track of current surah playing
CURRENT_SURAH = ""


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


def run_discord_bot():
    TOKEN = 'DISCORD_BOT_TOKEN'  # Replace with your bot token
    bot.run(TOKEN)

# Run the bot
run_discord_bot()
