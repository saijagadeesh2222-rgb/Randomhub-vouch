import discord
from discord import app_commands
from discord.ext import commands
import random
import string
import asyncio
import os

VOUCH_CHANNEL_ID = 1479868238396653578

# Starting numbers
VOUCH_COUNT = 436
ORDER_NUMBER = 436

PRODUCTS = {
    "Duel Script": ("USD", 5, 7),
    "Trade Machine Script": ("USD", 7, 10),
    "Auto Accept Script": ("USD", 7, 10),
    "Force Add Script": ("USD", 5, 7)
}

REVIEWS = [
    "legit and fast 🔥",
    "works perfectly tysm",
    "vouch!! instant delivery",
    "best script fr",
    "support was fast and helpful",
    "10/10 recommend",
    "W service",
    "no issues works great",
    "super fast delivery",
    "actually works lol",
    "ty for fast delivery"
]

intents = discord.Intents.default()
intents.members = True


class RandomHubBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.running = False
        self.vouch_task = None

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Bot online as {self.user}")

    async def send_vouch(self):

        global VOUCH_COUNT
        global ORDER_NUMBER

        channel = self.get_channel(VOUCH_CHANNEL_ID)
        if not channel:
            return

        members = [m for m in channel.guild.members if not m.bot]
        if not members:
            return

        player = random.choice(members)

        product = random.choice(list(PRODUCTS.keys()))
        currency, min_price, max_price = PRODUCTS[product]

        price = round(random.uniform(min_price, max_price), 2)
        stars = round(random.uniform(3.5, 5.0), 1)

        price_text = f"${price}"
        payment = "LTC"

        ORDER_NUMBER += 1
        VOUCH_COUNT += 1

        vouch_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        embed = discord.Embed(
            title="⭐ Customer Purchase Review",
            description=f"> {random.choice(REVIEWS)}",
            color=random.randint(0, 0xffffff)
        )

        embed.add_field(
            name="👤 Customer",
            value=player.mention,
            inline=True
        )

        embed.add_field(
            name="📦 Product",
            value=f"`{product}`",
            inline=True
        )

        embed.add_field(
            name="⭐ Rating",
            value=f"{stars}/5",
            inline=True
        )

        embed.add_field(
            name="💰 Price",
            value=price_text,
            inline=True
        )

        embed.add_field(
            name="💳 Payment",
            value=payment,
            inline=True
        )

        embed.add_field(
            name="🧾 Order Info",
            value=f"Order #: **{ORDER_NUMBER}**\nTransaction ID: **{vouch_id}**",
            inline=False
        )

        embed.add_field(
            name="📊 Total Vouches",
            value=f"{VOUCH_COUNT}+",
            inline=False
        )

        embed.set_author(
            name="Random Hub • Verified Purchase",
            icon_url=channel.guild.icon.url if channel.guild.icon else None
        )

        embed.set_footer(text="Random Hub • Instant Delivery Marketplace")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)

    async def auto_vouch_loop(self):

        while self.running:

            wait_hours = random.uniform(4, 5)
            print(f"Next vouch in {wait_hours:.2f} hours")

            await asyncio.sleep(wait_hours * 3600)

            if self.running:
                await self.send_vouch()


bot = RandomHubBot()


@bot.tree.command(name="start", description="Start auto vouch system")
async def start(interaction: discord.Interaction):

    if bot.running:
        await interaction.response.send_message("Already running.", ephemeral=True)
        return

    bot.running = True

    await interaction.response.send_message("✅ Auto vouch system started.")

    # Send 10 vouches instantly
    for _ in range(10):
        await bot.send_vouch()
        await asyncio.sleep(random.uniform(1, 3))

    bot.vouch_task = asyncio.create_task(bot.auto_vouch_loop())


@bot.tree.command(name="stop", description="Stop auto vouch system")
async def stop(interaction: discord.Interaction):

    if not bot.running:
        await interaction.response.send_message("Already stopped.", ephemeral=True)
        return

    bot.running = False

    if bot.vouch_task:
        bot.vouch_task.cancel()

    await interaction.response.send_message("⛔ Auto vouch system stopped.")


bot.run(os.getenv("TOKEN"))
