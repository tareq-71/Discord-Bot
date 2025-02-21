import discord
from discord.ext import commands

class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracked_users = {}  # Dictionary to track users and their custom messages

    def has_manage_messages():
        """Check if the user has the 'Manage Messages' permission."""
        async def predicate(ctx):
            return ctx.author.guild_permissions.manage_messages
        return commands.check(predicate)

    @commands.command(hidden=True)
    @has_manage_messages()
    async def autodelete(self, ctx, user: discord.Member, *, custom_message: str = "🚫 This user’s message was deleted."):
        """(Requires Manage Messages) Enable auto-delete for a user and replace their messages with a custom message."""
        self.tracked_users[user.id] = custom_message
        await ctx.send(f"✅ Now deleting messages from `{user.display_name}` and replacing them with: `{custom_message}`.")

    @commands.command(hidden=True)
    @has_manage_messages()
    async def stopautodelete(self, ctx, user: discord.Member):
        """(Requires Manage Messages) Disable auto-delete for a specific user."""
        if user.id in self.tracked_users:
            del self.tracked_users[user.id]
            await ctx.send(f"🛑 Stopped auto-deleting messages from `{user.display_name}`.")
        else:
            await ctx.send(f"❌ `{user.display_name}` is not being auto-deleted.")

    @commands.command(hidden=True)
    @has_manage_messages()
    async def listautodelete(self, ctx):
        """(Requires Manage Messages) Show all users who have auto-delete enabled."""
        if not self.tracked_users:
            await ctx.send("📜 No users are currently being auto-deleted.")
            return

        user_list = "\n".join(f"- <@{user_id}>: {msg}" for user_id, msg in self.tracked_users.items())
        await ctx.send(f"🔍 **Currently Auto-Deleting Messages From:**\n{user_list}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Automatically delete tracked user messages and send the custom response."""
        if message.author.id in self.tracked_users and not message.author.bot:
            custom_response = self.tracked_users[message.author.id]
            await message.delete()
            await message.channel.send(f"{custom_response}")

async def setup(bot):
    await bot.add_cog(AutoDelete(bot))
