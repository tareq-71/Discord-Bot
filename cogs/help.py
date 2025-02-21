import discord
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"])
    async def help_command(self, ctx, command_name: str = None):
        """Displays all commands with descriptions or details on a specific command."""
        
        mee6_id = 159985870458322944  # MEE6's Bot ID

        # ✅ Wait for MEE6 to send a message before deleting
        await asyncio.sleep(1.5)  # Give MEE6 time to respond

        async for message in ctx.channel.history(limit=5):
            if message.author.id == mee6_id:
                await message.delete()
                break  # Stop after deleting the first MEE6 message

        # ✅ If a specific command is requested, show its details
        if command_name:
            command = self.bot.get_command(command_name)
            if command and not command.hidden:
                embed = discord.Embed(title=f"📌 Command: `{command.name}`", color=discord.Color.blue())
                embed.add_field(name="🔹 Description", value=command.help or "No description available.", inline=False)
                embed.add_field(name="🛠️ Usage", value=f"`!{command.name}`", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Command `{command_name}` not found or is hidden.")
            return

        # ✅ Display only non-hidden commands grouped by cogs (Categories)
        embed = discord.Embed(title="📜 iizam Bot Help Menu", color=discord.Color.blurple())
        embed.set_footer(text="Use !help <command> to get details on a specific command.")

        for cog_name, cog in self.bot.cogs.items():
            commands_list = [cmd for cmd in cog.get_commands() if not cmd.hidden]

            if commands_list:
                command_info = "\n".join([f"🔹 `!{cmd.name}` - {cmd.help}" for cmd in commands_list if cmd.help])
                embed.add_field(name=f"**{cog_name} Commands**", value=command_info, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
