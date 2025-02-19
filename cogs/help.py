import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"])
    async def help_command(self, ctx, command_name: str = None):
        """
        Displays all commands with descriptions or provides details on a specific command.
        """
        if command_name:
            # Get details on a specific command
            command = self.bot.get_command(command_name)
            if command and not command.hidden:  # ✅ Exclude hidden commands
                # 🎨 Different color for individual command details
                embed = discord.Embed(title=f"📌 Command: `{command.name}`", color=discord.Color.orange())
                embed.add_field(name="Description", value=command.help or "No description available.", inline=False)
                embed.add_field(name="Usage", value=f"!{command.name}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Command `{command_name}` not found or is hidden.")
            return

        # ✅ Display only non-hidden commands grouped by cogs
        embed = discord.Embed(title="📜 Available Commands", color=discord.Color.blue())  # ✅ Main Help Color
        embed.set_footer(text="Use !help <command> to get more details.")

        for cog_name, cog in self.bot.cogs.items():
            commands_list = [cmd for cmd in cog.get_commands() if not cmd.hidden]  # ✅ Exclude hidden commands

            if commands_list:
                # 🎨 Different color per category (optional)
                category_color = discord.Color.green() if "Mod" in cog_name else discord.Color.teal()
                
                embed.add_field(
                    name=f"{cog_name} Commands:",
                    value="\n".join([f"**!{cmd.name}** - {cmd.help}" for cmd in commands_list if cmd.help]),
                    inline=False
                )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
