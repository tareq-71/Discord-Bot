import discord
from discord.ext import commands

class ModHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help_mods", hidden=True)
    @commands.has_permissions(manage_messages=True)  # ✅ Only mods/admins can use this
    async def help_mods(self, ctx):
        """Shows a list of all hidden commands (moderator/admin commands)."""
        embed = discord.Embed(title="🛠 Moderator Commands", color=discord.Color.red())

        mod_commands = []

        # ✅ Loop through all cogs and commands, filter only hidden ones
        for cog in self.bot.cogs.values():
            for cmd in cog.get_commands():
                if cmd.hidden:  # ✅ Only include hidden commands
                    mod_commands.append(f"`{cmd.name}` - {cmd.help or 'No description available.'}")

        if mod_commands:
            embed.description = "\n".join(mod_commands)
        else:
            embed.description = "No hidden/moderator commands found."

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ModHelp(bot))
