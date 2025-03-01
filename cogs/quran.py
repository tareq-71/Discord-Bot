import discord
import os
import asyncio
from discord.ext import commands

RECITERS = {
    "dosari": "Yasser Al-Dosari",
    "afasy": "Mishari Rashid Al-Afasy",
    "hazza": "Hazza Al-Balushi",
    "idrees": "Idrees Abkar"
}

DEFAULT_RECITER = "dosari"

# Mapping Surah Names to Numbers
SURAH_TO_NUMBER = {
    "fatiha": "001",
    "baqara": "002",
    "imran": "003",
    "nisa": "004",
    "maidah": "005",
    "anam": "006",
    "araf": "007",
    "anfal": "008",
    "tawba": "009",
    "yunus": "010",
    "hud": "011",
    "yusuf": "012",
    "rad": "013",
    "ibrahim": "014",
    "hijr": "015",
    "nahl": "016",
    "isra": "017",
    "kahf": "018",
    "maryam": "019",
    "taha": "020",
    "anbiya": "021",
    "hajj": "022",
    "muminun": "023",
    "nur": "024",
    "furqan": "025",
    "shuara": "026",
    "naml": "027",
    "qasas": "028",
    "ankabut": "029",
    "rum": "030",
    "luqman": "031",
    "sajda": "032",
    "ahzab": "033",
    "saba": "034",
    "fatir": "035",
    "yaseen": "036",
    "saffat": "037",
    "sad": "038",
    "zumar": "039",
    "ghafir": "040",
    "fussilat": "041",
    "shura": "042",
    "zukhruf": "043",
    "dukhan": "044",
    "jathiya": "045",
    "ahqaf": "046",
    "muhammad": "047",
    "fath": "048",
    "hujurat": "049",
    "qaf": "050",
    "dhariyat": "051",
    "tur": "052",
    "najm": "053",
    "qamar": "054",
    "rahman": "055",
    "waqia": "056",
    "hadid": "057",
    "mujadila": "058",
    "hashr": "059",
    "mumtahina": "060",
    "saff": "061",
    "jumuah": "062",
    "munafiqun": "063",
    "taghabun": "064",
    "talaq": "065",
    "tahrim": "066",
    "mulk": "067",
    "qalam": "068",
    "haqqa": "069",
    "maarij": "070",
    "nuh": "071",
    "jinn": "072",
    "muzammil": "073",
    "mudathir": "074",
    "qiyama": "075",
    "insan": "076",
    "mursalat": "077",
    "naba": "078",
    "naziat": "079",
    "abasa": "080",
    "takwir": "081",
    "infitar": "082",
    "mutaffifin": "083",
    "inshiqaq": "084",
    "burooj": "085",
    "tariq": "086",
    "ala": "087",
    "ghashiya": "088",
    "fajr": "089",
    "balad": "090",
    "shams": "091",
    "layl": "092",
    "duha": "093",
    "sharh": "094",
    "tin": "095",
    "alaq": "096",
    "qadr": "097",
    "bayyina": "098",
    "zilzal": "099",
    "adiyat": "100",
    "qariah": "101",
    "takathur": "102",
    "asr": "103",
    "humazah": "104",
    "fil": "105",
    "quraish": "106",
    "maun": "107",
    "kawthar": "108",
    "kafirun": "109",
    "nasr": "110",
    "masad": "111",
    "ikhlas": "112",
    "falaq": "113",
    "nas": "114"
}

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

# Quran File Paths
QURAN_LIBRARY = {
    reciter: {SURAH_TO_NUMBER[key]: f"Quran_surahs/{reciter}/{SURAH_TO_NUMBER[key]}.mp3" for key in SURAH_TO_NUMBER}
    for reciter in RECITERS.keys()
}


class PaginatedSurahSelect(discord.ui.View):
    def __init__(self, bot, ctx, reciter, page=0):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.reciter = reciter
        self.page = page
        self.per_page = 25  # Max items per page

        # ✅ Ensure Surahs are actually available for this reciter
        self.available_surahs = [
            key for key, num in SURAH_TO_NUMBER.items()
            if num in QURAN_LIBRARY.get(reciter, {}) and os.path.exists(QURAN_LIBRARY[reciter][num])
        ]

        # ✅ Prevent division by zero
        self.total_pages = max((len(self.available_surahs) // self.per_page) + (1 if len(self.available_surahs) % self.per_page > 0 else 0), 1)

        self.add_dropdown()
        self.add_buttons()

    def add_dropdown(self):
        """Creates a dropdown menu with only available Surahs."""
        start_idx = self.page * self.per_page
        end_idx = start_idx + self.per_page

        options = [
            discord.SelectOption(label=SURAH_NAMES[key], value=key)
            for key in self.available_surahs[start_idx:end_idx]
        ]

        # ✅ Handle case where no Surahs are available
        if not options:
            options.append(discord.SelectOption(label="No available Surahs", value="none", description="Try a different reciter", default=True))

        select = discord.ui.Select(
            placeholder=f"Select a Surah (Page {self.page+1}/{self.total_pages})",
            min_values=1,
            max_values=1,
            options=options
        )

        async def select_callback(interaction: discord.Interaction):
            surah = select.values[0]

            if surah == "none":
                await interaction.response.send_message("❌ No available Surahs for this reciter.", ephemeral=True)
                return

            self.ctx.bot.get_cog("Quran").auto_playing = False
            await interaction.response.defer()
            await self.ctx.bot.get_cog("Quran").play_audio(self.ctx, surah, self.reciter, manual_call=True)

        select.callback = select_callback
        self.add_item(select)

    def add_buttons(self):
        """Adds navigation buttons for paginated Surah selection."""
        if self.page > 0:
            self.add_item(PreviousPageButton(self.bot, self.ctx, self.reciter, self.page))
        if self.page < self.total_pages - 1:
            self.add_item(NextPageButton(self.bot, self.ctx, self.reciter, self.page))


class PreviousPageButton(discord.ui.Button):
    def __init__(self, bot, ctx, reciter, page):
        super().__init__(label="◀ Previous", style=discord.ButtonStyle.secondary)
        self.bot = bot
        self.ctx = ctx
        self.reciter = reciter
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=PaginatedSurahSelect(self.bot, self.ctx, self.reciter, self.page - 1))


class NextPageButton(discord.ui.Button):
    def __init__(self, bot, ctx, reciter, page):
        super().__init__(label="Next ▶", style=discord.ButtonStyle.secondary)
        self.bot = bot
        self.ctx = ctx
        self.reciter = reciter
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=PaginatedSurahSelect(self.bot, self.ctx, self.reciter, self.page + 1))

class PlaybackControlView(discord.ui.View):
    """Persistent playback control buttons with working skip."""
    def __init__(self, bot, ctx):
        super().__init__(timeout=None)  # Keep buttons active
        self.bot = bot
        self.ctx = ctx

    @discord.ui.button(label="⏸ Pause", style=discord.ButtonStyle.secondary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Pause playback and update 'Now Playing' message instead of sending a private message."""
        quran_cog = self.bot.get_cog("Quran")
        voice_client = interaction.guild.voice_client

        if voice_client and voice_client.is_playing():
            voice_client.pause()
            
            # ✅ Convert numeric Surah key ('002') back to text ('baqara')
            surah_key = next((key for key, num in SURAH_TO_NUMBER.items() if num == quran_cog.current_surah), None)

            if surah_key:
                now_playing_text = f"```\nNow Playing: {SURAH_NAMES[surah_key]}\nReciter: {RECITERS[quran_cog.current_reciter]}\n⏸️ Paused\n```"

                # ✅ Update "Now Playing" box with pause status
                if hasattr(quran_cog, "now_playing_message") and quran_cog.now_playing_message:
                    try:
                        await quran_cog.now_playing_message.edit(content=now_playing_text)
                    except discord.NotFound:
                        pass  # If the message was deleted, ignore error

            await interaction.response.defer()
        else:
            await interaction.response.send_message("❌ No Surah is currently playing.", ephemeral=True)



    @discord.ui.button(label="▶ Resume", style=discord.ButtonStyle.success)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Resume playback and update 'Now Playing' message instead of sending a private message."""
        quran_cog = self.bot.get_cog("Quran")
        voice_client = interaction.guild.voice_client

        if voice_client and voice_client.is_paused():
            voice_client.resume()
            
            # ✅ Convert numeric Surah key ('002') back to text ('baqara')
            surah_key = next((key for key, num in SURAH_TO_NUMBER.items() if num == quran_cog.current_surah), None)

            if surah_key:
                now_playing_text = f"```\nNow Playing: {SURAH_NAMES[surah_key]}\nReciter: {RECITERS[quran_cog.current_reciter]}\n```"

                # ✅ Update "Now Playing" box to remove "Paused" text
                if hasattr(quran_cog, "now_playing_message") and quran_cog.now_playing_message:
                    try:
                        await quran_cog.now_playing_message.edit(content=now_playing_text)
                    except discord.NotFound:
                        pass  # If the message was deleted, ignore error

            await interaction.response.defer()
        else:
            await interaction.response.send_message("❌ No Surah is currently paused.", ephemeral=True)


    @discord.ui.button(label="⏭ Skip", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Skips to the next available Surah without crashing if one is missing."""
        quran_cog = self.bot.get_cog("Quran")
        voice_client = interaction.guild.voice_client

        if quran_cog.auto_playing:
            quran_cog.auto_playing = False  # Prevent extra skipping

        if voice_client and voice_client.is_playing():
            voice_client.stop()

        next_surah = quran_cog.get_next_surah()

        if next_surah:
            await interaction.response.defer()  # ✅ Prevents unnecessary reply
            await quran_cog.play_audio(interaction, next_surah, quran_cog.current_reciter, manual_call=False)
        else:
            await interaction.response.send_message("❌ No more Surahs available for this reciter.", ephemeral=True)  # ✅ Handle missing Surahs gracefully


class ReciterSelect(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__()
        self.bot = bot
        self.ctx = ctx

        select = discord.ui.Select(
            placeholder="Select a Reciter",
            min_values=1,
            max_values=1,
            options=self.get_reciter_options()
        )

        async def select_callback(interaction: discord.Interaction):
            reciter = select.values[0]
            await interaction.response.edit_message(
                content=f"✅ **Reciter: {RECITERS[reciter]}**\nSelect a Surah:",
                view=PaginatedSurahSelect(self.bot, self.ctx, reciter)
            )

        select.callback = select_callback
        self.add_item(select)

    def get_reciter_options(self):
        """Generates reciter options, marking those missing some Surahs."""
        options = []
        for reciter in RECITERS.keys():
            # Check if the reciter is missing any Surahs
            if self.is_incomplete_reciter(reciter):
                label = f"{RECITERS[reciter]} (Missing Some Surahs)"
            else:
                label = RECITERS[reciter]
            
            options.append(discord.SelectOption(label=label, value=reciter))

        return options


    def is_incomplete_reciter(self, reciter):
        """Checks if a reciter is missing any Surah files."""
        available_surahs = sum(
            1 for surah_num, file_path in QURAN_LIBRARY.get(reciter, {}).items()
            if os.path.exists(file_path)  # ✅ Only count if the file actually exists
        )

        total_surahs = len(SURAH_TO_NUMBER)  # 114 total Surahs

        #print(f"Reciter: {reciter}, Available: {available_surahs}, Total: {total_surahs}")  # Debugging print

        return available_surahs != total_surahs  # ✅ Return True if any Surah is missing

class Quran(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_surah = None
        self.current_reciter = DEFAULT_RECITER
        self.auto_playing = False
        self.playback_control_message = None  # Initialize control message tracking
        self.now_playing_message = None       # Initialize now playing message tracking


    async def join_voice_channel(self, ctx):
        """Joins the user's voice channel if not already connected."""
        if ctx.author.voice is None:
            await ctx.send("❌ You need to be in a voice channel.")
            return False
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        return True

    async def play_audio(self, ctx_or_interaction, surah, reciter, manual_call=True):
        """Plays the requested Surah and ensures auto-play works like before."""
        ctx = ctx_or_interaction if isinstance(ctx_or_interaction, commands.Context) else None
        interaction = ctx_or_interaction if isinstance(ctx_or_interaction, discord.Interaction) else None

        voice_client = ctx.voice_client if ctx else (interaction.guild.voice_client if interaction else None)

        if not voice_client:
            joined = await self.join_voice_channel(ctx_or_interaction)
            if not joined:
                return
            voice_client = ctx.voice_client if ctx else (interaction.guild.voice_client if interaction else None)

        surah_number = SURAH_TO_NUMBER.get(surah)
        if not surah_number:
            return

        file_path = QURAN_LIBRARY.get(reciter, {}).get(surah_number)

        # ✅ Check if the Surah exists before playing
        if not file_path or not os.path.exists(file_path):
            error_message = f"❌ Surah {SURAH_NAMES.get(surah, surah)} is not available for {RECITERS[reciter]}."
            if ctx:
                await ctx.send(error_message)
            elif interaction:
                await interaction.response.send_message(error_message, ephemeral=True)
            return  # ✅ Prevents freezing

        if voice_client.is_playing():
            voice_client.stop()
            await asyncio.sleep(1)

        if manual_call:
            self.auto_playing = True  # ✅ Ensure auto-play is enabled if started manually

        self.current_surah = surah_number
        self.current_reciter = reciter

        surah_key = next((key for key, num in SURAH_TO_NUMBER.items() if num == self.current_surah), None)
        now_playing_text = f"```\nNow Playing: {SURAH_NAMES[surah_key]}\nReciter: {RECITERS[reciter]}\n```" if surah_key else "Now Playing: Unknown"

        view = PlaybackControlView(self.bot, ctx_or_interaction)

        try:
            if manual_call:
                if self.playback_control_message:
                    await self.playback_control_message.delete()
                if self.now_playing_message:
                    await self.now_playing_message.delete()

                if ctx:
                    self.playback_control_message = await ctx.send("**Playback Controls:**", view=view)
                    self.now_playing_message = await ctx.send(now_playing_text)
                elif interaction:
                    await interaction.response.defer()
                    self.playback_control_message = await interaction.followup.send("**Playback Controls:**", view=view)
                    self.now_playing_message = await interaction.followup.send(now_playing_text)
            else:
                if self.now_playing_message:
                    await self.now_playing_message.edit(content=now_playing_text)
        except discord.NotFound:
            pass  

        # ✅ Improved `after_playback()` function
        def after_playback(error):
            if error:
                print(f"Playback error: {error}")
            if self.auto_playing:  # ✅ Ensure auto-play continues
                self.bot.loop.create_task(self.auto_next(ctx_or_interaction))

        voice_client.play(discord.FFmpegPCMAudio(file_path), after=after_playback)


    def get_next_surah(self):
        """Finds the next available Surah for the current reciter, looping back to the beginning."""
        if not self.current_surah:
            return None

        # ✅ Get a sorted list of available Surahs for this reciter
        available_surahs = sorted([
            key for key, num in SURAH_TO_NUMBER.items()
            if num in QURAN_LIBRARY.get(self.current_reciter, {}) and os.path.exists(QURAN_LIBRARY[self.current_reciter][num])
        ], key=lambda surah: int(SURAH_TO_NUMBER[surah]))  # Sort by Surah number

        if not available_surahs:
            return None  # No available Surahs for this reciter

        # ✅ Find the index of the current Surah
        current_surah_name = next((key for key, num in SURAH_TO_NUMBER.items() if num == self.current_surah), None)

        if current_surah_name not in available_surahs:
            return None  # If current Surah isn't in available Surahs, return None

        current_index = available_surahs.index(current_surah_name)

        # ✅ Loop back to the first Surah if we're at the last one
        if current_index + 1 < len(available_surahs):
            return available_surahs[current_index + 1]
        else:
            return available_surahs[0]  # Restart from the first Surah



    async def auto_next(self, ctx):
        """Automatically plays the next available Surah when the current one finishes."""
        if not self.auto_playing:
            return

        next_surah = self.get_next_surah()

        if next_surah:
            await self.play_audio(ctx, next_surah, self.current_reciter, manual_call=False)
        else:
            self.auto_playing = False  # ✅ Stop auto-play if no more Surahs exist
            if ctx:
                await ctx.send("✅ Auto-play stopped: No more Surahs available for this reciter.")

    @commands.command()
    async def surah(self, ctx):
        """Displays a menu to select a Surah and Reciter."""
        await ctx.send("(To select new reciter recall '!surah'.)")
        await ctx.send("**Select a Reciter:**", view=ReciterSelect(self.bot, ctx))


async def setup(bot):
    await bot.add_cog(Quran(bot))
