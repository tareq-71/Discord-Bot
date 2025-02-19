import discord
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        """Display shop items."""
        shop_text = "```Welcome to the iizam bot shop!\n1. Item A - 10 SIUBucks\n2. Item B - 20 SIUBucks\n3. Item C - 30 SIUBucks```"
        await ctx.send(shop_text)

async def setup(bot):
    await bot.add_cog(Shop(bot))
