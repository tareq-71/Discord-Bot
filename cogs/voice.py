import discord
import os
import random
from discord.ext import commands
from gtts import gTTS

DEFAULT_VOLUME = 1.0  # Default volume level

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
        async def join(self, ctx, *, channel_name: str = None):
            """
            Joins the specified voice channel by name, or the user's current channel if no name is provided.
            """
            guild = ctx.guild
            voice_client = ctx.voice_client  # Get current voice connection

            if voice_client and voice_client.is_connected():
                await ctx.send("❌ I'm already connected to a voice channel!")
                return

            if channel_name:
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                if channel:
                    await channel.connect()
                    await ctx.send(f"✅ Joined voice channel: **{channel_name}**")
                else:
                    await ctx.send(f"❌ Voice channel **'{channel_name}'** not found.")
            elif ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send(f"✅ Joined **your** voice channel: **{channel.name}**")
            else:
                await ctx.send("❌ You need to specify a channel name or be in a voice channel yours")


    @commands.command(hidden=True)
    async def leave(self, ctx):
        """Disconnects the bot from the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")

    @commands.command(hidden=True)
    async def sayV(self, ctx, *, text: str):
        """Converts text to speech and plays it in the voice channel."""
        if ctx.voice_client:
            # Generate TTS audio file
            tts = gTTS(text=text, lang='en')
            tts.save("tts_output.mp3")

            # Play the audio
            ctx.voice_client.play(
                discord.FFmpegPCMAudio("tts_output.mp3"),
                after=lambda e: os.remove("tts_output.mp3")  # Delete after playing
            )
        else:
            await ctx.send("I'm not in a voice channel. Use `!join` to invite me.")

    @commands.command(hidden=True)
    async def set_volume(self, ctx, volume: float):
        """Sets playback volume (e.g., 0.5 for 50%, 1.0 for 100%, 2.0 for 200%)."""
        global DEFAULT_VOLUME
        if 0.0 < volume <= 2.0:  # Ensure valid range
            DEFAULT_VOLUME = volume
            await ctx.send(f"Volume set to {volume * 100:.0f}%.")
        else:
            await ctx.send("Volume must be between 0.1 and 2.0.")

async def setup(bot):
    await bot.add_cog(Voice(bot))
