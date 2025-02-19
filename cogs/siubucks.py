import discord
import json
import os
from discord.ext import commands

SIUBUCKS_FILE = "siubucks.json"

class SIUBucks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_SIUBucks()

    def load_SIUBucks(self):
        """Load SIUBucks balances from a JSON file."""
        if os.path.exists(SIUBUCKS_FILE):
            with open(SIUBUCKS_FILE, "r") as f:
                self.members_SIUBucks = json.load(f)
        else:
            self.members_SIUBucks = {}

    def save_SIUBucks(self):
        """Save SIUBucks balances to a JSON file."""
        with open(SIUBUCKS_FILE, "w") as f:
            json.dump(self.members_SIUBucks, f, indent=4)

    def award_SIUBucks(self, user, amount):
        """Give SIUBucks to a user."""
        user_id = str(user.id)
        self.members_SIUBucks[user_id] = self.members_SIUBucks.get(user_id, 0) + amount
        self.save_SIUBucks()

    def remove_SIUBucks(self, user, amount):
        """Remove SIUBucks from a user."""
        user_id = str(user.id)
        self.members_SIUBucks[user_id] = self.members_SIUBucks.get(user_id, 0) - amount
        self.save_SIUBucks()

    @commands.command(hidden=True)
    async def give(self, ctx, user: discord.Member, amount: int):
        """Give SIUBucks (Admin Only)."""
        if ctx.author.id == 700122491754119299:
            self.award_SIUBucks(user, amount)
            await ctx.send(f"{user} has been given {amount} SIUBucks!")  
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command(hidden=True)
    async def remove(self, ctx, user: discord.Member, amount: int):
        """Remove SIUBucks (Admin Only)."""
        if ctx.author.id == 700122491754119299:
            self.remove_SIUBucks(user, amount)
            await ctx.send(f"{user} has lost {amount} SIUBucks!")
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command()
    async def balance(self, ctx):
        """Check your SIUBucks balance."""
        user_id = str(ctx.author.id)
        amount = self.members_SIUBucks.get(user_id, 0)
        await ctx.send(f"You have {amount} SIUBucks.")

    @commands.command()
    async def serverbucks(self, ctx):
        """Show all SIUBucks balances (Debug)."""
        await ctx.send(str(self.members_SIUBucks))

async def setup(bot):
    await bot.add_cog(SIUBucks(bot))
