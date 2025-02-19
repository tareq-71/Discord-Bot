import discord
import os
import random
from discord.ext import commands

class Photos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_random_file(self, ctx, folder_name):
        folder_path = folder_name
        
        # Get all files from the folder
        all_files = os.listdir(folder_path) if os.path.exists(folder_path) else []
        
        if not all_files:
            await ctx.send(f"No files found in `{folder_name}` folder.")
            return

        # Choose a random file
        random_file = random.choice(all_files)
        file_path = os.path.join(folder_path, random_file)

        # Send as a file attachment
        await ctx.send(file=discord.File(file_path))

    @commands.command()
    async def sami(self, ctx):
        """Send a random image/file from the 'sami' folder"""
        await self.send_random_file(ctx, "sami")

    @commands.command()
    async def japan(self, ctx):
        """Send a random image/file from the 'japan' folder"""
        await self.send_random_file(ctx, "japan")

async def setup(bot):
    await bot.add_cog(Photos(bot))


