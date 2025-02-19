import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handles unknown commands and other errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Unknown command. Use `!help` to see available commands.")
        else:
            raise error  # ✅ Let other errors be handled normally

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
