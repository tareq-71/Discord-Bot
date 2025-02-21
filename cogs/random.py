import discord
import random
from discord.ext import commands

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
        """Sends a message to the specified text channel."""
        IIZAM = 700122491754119299
        if ctx.author.id == IIZAM:
            await channel.send(message)
            await ctx.send("Message sent")
        else:
            await ctx.send("You dont have permission to us this command.")

    @commands.command()
    async def member(self, ctx):
        """Chooses a random member from the server."""
        if ctx.guild:
            member = random.choice(ctx.guild.members)
            await ctx.send(f"🎉 Randomly selected member: {member.display_name}")
        else:
            await ctx.send("❌ This command can only be used in a server.")
    
    @commands.command()
    async def teams(self, ctx, channel_name: str):
        """Randomly divide members of a voice channel into two teams."""
        guild = ctx.guild
        channel = discord.utils.get(guild.voice_channels, name=channel_name)

        if not channel:
            await ctx.send(f"Voice channel '{channel_name}' not found.")
            return

        AMAR = 294453266274582534
        AMRIT = 987456591869673584
        IIZAM_BOT = 1078061159539802203
        YOUSEF = 772294958086488104
        members = [m for m in channel.members if m.id not in {IIZAM_BOT, AMRIT}]

        if not members:
            await ctx.send(f"No eligible members in '{channel_name}'.")
            return

        random.shuffle(members)
        mid = len(members) // 2
        team1 = ", ".join([m.name for m in members[:mid]])
        team2 = ", ".join([m.name for m in members[mid:]])

        await ctx.send(f"**Team 1:** {team1}\n**Team 2:** {team2}")

async def setup(bot):
    await bot.add_cog(Random(bot))
