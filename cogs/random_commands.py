import discord
import random
from discord.ext import commands

class RandomCommands(commands.Cog):
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

async def setup(bot):
    await bot.add_cog(RandomCommands(bot))
