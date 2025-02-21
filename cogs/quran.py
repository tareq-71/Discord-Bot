import discord
import os
from discord.ext import commands

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


class Quran(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_surah = None

    async def play_audio(self, ctx, surah_name, manual_call=True):
        """Stops current playback (if any) and plays the requested Surah, then auto-plays the next one."""
        file_path = QURAN_LIBRARY.get(surah_name)

        if not file_path or not os.path.exists(file_path):
            if manual_call:  # Only send a message if it was a manual request
                await ctx.send(f"Audio file not found for {SURAH_NAMES.get(surah_name, surah_name)}.")
            return

        # Stop current playback before updating self.current_surah
        if ctx.voice_client and ctx.voice_client.is_playing():
            self.manual_override = True  # Indicate that playback was manually changed
            ctx.voice_client.stop()

        # Set current_surah **before** playing to prevent mismatched messages
        self.current_surah = surah_name  

        # Send "Now playing" message only if it's a manual call
        if manual_call:
            await ctx.send(f"Now playing: {SURAH_NAMES[surah_name]}")

        def after_playback(error):
            if not self.manual_override:  # Only auto-play next if not manually overridden
                self.bot.loop.create_task(self.auto_next(ctx))
            else:
                self.manual_override = False  # Reset flag after manual playback switch

        ctx.voice_client.play(
            discord.FFmpegPCMAudio(file_path),
            after=after_playback
        )

    async def auto_next(self, ctx):
        """Automatically plays the next Surah when the current one ends, without sending a message."""
        next_surah = self.get_next_surah(self.current_surah)
        if next_surah:
            await self.play_audio(ctx, next_surah, manual_call=False)  # Auto transition, no message

    def get_next_surah(self, current_surah):
        """Finds the next Surah in the order from SURAH_NAMES, looping back at the end."""
        surah_list = list(SURAH_NAMES.keys())  # Get a list of Surahs in order
        if current_surah in surah_list:
            index = surah_list.index(current_surah)
            next_index = (index + 1) % len(surah_list)  # Loops back to 0 when reaching the end
            return surah_list[next_index]
        return None

    @commands.command()
    async def surah(self, ctx, surah_name: str):
        """Plays the specified Surah and stops any currently playing one."""
        surah_name = surah_name.lower()

        if surah_name not in QURAN_LIBRARY:
            await ctx.send(f"'{surah_name}' is not available in the library.")
            return

        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.send("I am not in a voice channel. Use `!join` first.")
            return

        await self.play_audio(ctx, surah_name, manual_call=True)  # Manual play, sends message

    @commands.command()
    async def currentsurah(self, ctx):
        """Displays the currently playing Surah."""
        if self.current_surah:
            await ctx.send(f"Currently playing: {SURAH_NAMES[self.current_surah]}")
        else:
            await ctx.send("No Surah is currently playing.")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the currently playing Surah."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Playback paused.")
        else:
            await ctx.send("No Surah is currently playing.")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the paused Surah."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("No Surah is currently paused.")

    @commands.command()
    async def next(self, ctx):
        """Skips the current Surah and plays the next one in order."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            self.manual_override = True  # Prevent auto_next() from interfering
            ctx.voice_client.stop()
            next_surah = self.get_next_surah(self.current_surah)
            if next_surah:
                await ctx.send("Surah skipped.")
                await self.play_audio(ctx, next_surah, manual_call=True)  # Make skip behave like !surah
            else:
                await ctx.send("No next Surah found.")  # Should never happen due to looping
        else:
            await ctx.send("No Surah is currently playing.")

    @commands.command()
    async def surahs(self, ctx):
        """Lists all available Surahs."""
        surah_list = "\n".join(f"- {value}" for value in SURAH_NAMES.values())
        await ctx.send(f"Available Surahs:\n```{surah_list}```")


async def setup(bot):
    await bot.add_cog(Quran(bot))