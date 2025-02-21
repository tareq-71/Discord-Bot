import discord
import asyncio
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop_items = {
            "customrole": {"price": 10000, "description": "Gives you a custom role for 30 days."},
            "muteniz": {"price": 250, "description": "Mutes Niz for 3 mins.", "mute_target": 692408240511778876}
        }

    @commands.command()
    async def shop(self, ctx):
        """Display shop items."""
        shop_text = "```Welcome to the iizam bot shop!\n"
        for item_name, item_info in self.shop_items.items():
            shop_text += f"- {item_name.title()} : {item_info['price']} SIUBucks\n"
        shop_text += "```"
        await ctx.send(shop_text)

    @commands.command()
    async def buy(self, ctx, *, item_name: str):
        """Allows users to buy an item from the shop."""
        item_name = item_name.lower()  # Normalize input to lowercase for matching

        if item_name not in self.shop_items:
            await ctx.send("❌ Item not found! Please check `!shop` for available items.")
            return

        item_info = self.shop_items[item_name]
        price = item_info["price"]

        # Get SIUBucks system
        siubucks_cog = self.bot.get_cog("SIUBucks")
        if not siubucks_cog:
            await ctx.send("Error: SIUBucks system unavailable.")
            return

        # Fetch user's balance
        user_id = str(ctx.author.id)
        balance = siubucks_cog.members_SIUBucks.get(user_id, 0)

        if balance < price:
            await ctx.send(f"❌ You don't have enough SIUBucks! You need {price - balance} more SIUBucks.")
            return

        # Deduct the cost from user's balance
        siubucks_cog.remove_SIUBucks(ctx.author, price)
        await ctx.send(f"✅ You have successfully purchased **{item_name.title()}** for {price} SIUBucks!")

        # ✅ Handle custom role creation
        if item_name == "customrole":
            await self.create_custom_role(ctx)

        # ✅ Handle muting a specific user for 3 minutes
        elif "mute_target" in item_info:
            await self.mute_user(ctx, item_info["mute_target"])

    async def create_custom_role(self, ctx):
        """Prompts the user for a role name and color, then creates the role."""
        await ctx.send("🛠️ Please enter the name of your custom role:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            role_name_msg = await self.bot.wait_for("message", timeout=60, check=check)
            role_name = role_name_msg.content.strip()

            await ctx.send("🎨 Now enter a color for your role (in HEX format, e.g., `FF5733`):\n Use this website to get your color in HEX: https://htmlcolorcodes.com/.")

            color_msg = await self.bot.wait_for("message", timeout=100, check=check)
            color_hex = color_msg.content.strip()

            # ✅ Convert HEX to Discord Color
            try:
                if len(color_hex) != 6:
                    raise ValueError("Invalid HEX code format.")
                role_color = discord.Color(int(color_hex[0:], 16))
            except ValueError:
                await ctx.send("❌ Invalid HEX color format! Defaulting to **white**.")
                role_color = discord.Color.default()

            # ✅ Create the role with no special permissions
            role = await ctx.guild.create_role(name=role_name, color=role_color, reason="Purchased custom role")
            await ctx.author.add_roles(role)
            await ctx.send(f"🎉 Congratulations! Your **{role_name}** role has been created and assigned to you!")

        except asyncio.TimeoutError:
            await ctx.send("⏳ You took too long to respond! Custom role creation has been cancelled.")

    async def mute_user(self, ctx, target_id):
        """Mutes the specified user for 3 minutes if they are in a voice channel."""
        mute_target = ctx.guild.get_member(target_id)

        if not mute_target:
            await ctx.send("❌ The user to be muted is not in this server.")
            return

        if mute_target.voice and mute_target.voice.channel:
            try:
                await mute_target.edit(mute=True)
                await ctx.send(f"🔇 `{mute_target.display_name}` has been **voice muted** by **{ctx.author.display_name}** for 3 minutes!")
                
                # ✅ Wait 3 minutes before unmuting
                await asyncio.sleep(180)  # 180 seconds = 3 minutes
                await mute_target.edit(mute=False)
                await ctx.send(f"🔊 `{mute_target.display_name}` has been automatically **unmuted** after 3 minutes.")

            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to mute members. Please check my role permissions.")
        else:
            await ctx.send(f"⚠️ `{mute_target.display_name}` is not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Shop(bot))
