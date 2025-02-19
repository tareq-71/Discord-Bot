import discord
import json
import os
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a user from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked for: {reason}")

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a user from the server."""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} has been banned for: {reason}")

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_id: int):
        """Unban a user from the server by user ID."""
        banned_users = await ctx.guild.bans()
        user = discord.Object(id=user_id)

        for ban_entry in banned_users:
            if ban_entry.user.id == user_id:
                await ctx.guild.unban(user)
                await ctx.send(f"✅ Unbanned user ID: {user_id}")
                return

        await ctx.send("User not found in ban list.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
