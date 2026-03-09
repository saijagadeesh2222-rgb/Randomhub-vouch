import discord
from discord.ext import commands
from discord import app_commands
import random
import string
import asyncio
import os

TOKEN = os.getenv("TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

VOUCH_CHANNEL_ID = 1479868238396653578

VOUCH_COUNT = 436
ORDER_NUMBER = 436

SELLERS = [
1435466065990652044,
1243922588133228626,
1272254946288336917,
1471106657193820250,
1435160292739776554,
828149658789609492
]

PRODUCTS = {
"Trade Machine Script": (7,10),
"Auto Accept Script": (7,10),
"Force Add Script": (5,7),
"Duel Script": (5,7)
}

PAYMENTS = [
"LTC",
"BTC",
"PayPal",
"USDT",
"ETH"
]

REVIEWS = [
"legit and fast",
"works perfectly tysm",
"delivery was instant",
"really smooth purchase",
"support replied fast",
"script works great",
"10/10 recommend",
"seller is legit",
"super fast delivery",
"no issues works great",
"actually works lol",
"best script fr",
"fast service",
"works as expected",
"worth the price",
"highly recommend",
"setup was easy",
"great product",
"perfect service",
"trusted seller",
"instant delivery",
"clean script",
"works flawlessly",
"very good support",
"top tier service",
"good communication",
"great experience",
"product delivered fast",
"everything works",
"very smooth transaction",
"excellent seller"
]

intents = discord.Intents.default()
intents.members = True


class VouchBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.running = False

    async def setup_hook(self):
        await self.tree.sync()

    async def get_random_member(self, guild):

        members = []

        async for member in guild.fetch_members(limit=None):

            if member.bot:
                continue

            if member.guild_permissions.administrator:
                continue

            members.append(member)

        return random.choice(members)

    async def send_vouch(self):

        global VOUCH_COUNT
        global ORDER_NUMBER

        vouch_channel = self.get_channel(VOUCH_CHANNEL_ID)
        log_channel = self.get_channel(LOG_CHANNEL_ID)

        if vouch_channel is None:
            return

        guild = vouch_channel.guild

        member = await self.get_random_member(guild)

        product = random.choice(list(PRODUCTS.keys()))
        min_price,max_price = PRODUCTS[product]

        price = round(random.uniform(min_price,max_price),2)
        rating = round(random.uniform(4.2,5.0),1)

        payment = random.choice(PAYMENTS)

        seller_id = random.choice(SELLERS)

        ORDER_NUMBER += 1
        VOUCH_COUNT += 1

        transaction = ''.join(random.choices(string.ascii_uppercase + string.digits,k=8))

        embed = discord.Embed(
            title="⭐ Customer Purchase Review",
            description=f"> {random.choice(REVIEWS)}",
            color=random.randint(0,16777215)
        )

        embed.add_field(name="👤 Customer",value=member.mention,inline=True)
        embed.add_field(name="🧑‍💼 Seller",value=f"<@{seller_id}>",inline=True)
        embed.add_field(name="📦 Product",value=product,inline=True)

        embed.add_field(name="⭐ Rating",value=f"{rating}/5",inline=True)
        embed.add_field(name="💰 Price",value=f"${price}",inline=True)
        embed.add_field(name="💳 Payment",value=payment,inline=True)

        embed.add_field(
        name="🧾 Order Info",
        value=f"Order #: **{ORDER_NUMBER}**\nTransaction ID: **{transaction}**",
        inline=False
        )

        embed.add_field(
        name="📊 Total Vouches",
        value=f"{VOUCH_COUNT}+",
        inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(text="Random Hub • Verified Purchase")
        embed.timestamp = discord.utils.utcnow()

        async with vouch_channel.typing():
            await asyncio.sleep(random.uniform(2,5))

        message = await vouch_channel.send(embed=embed)

        await asyncio.sleep(random.uniform(5,15))

        await message.reply(
            f"Thank you for purchasing **{product}**! If you need help feel free to contact the seller.",
            mention_author=False
        )

        if log_channel:

            log_embed = discord.Embed(
            title="🛒 Purchase Log",
            color=discord.Color.blue()
            )

            log_embed.add_field(name="Customer",value=member.mention)
            log_embed.add_field(name="Seller",value=f"<@{seller_id}>")
            log_embed.add_field(name="Product",value=product)
            log_embed.add_field(name="Price",value=f"${price}")
            log_embed.add_field(name="Payment",value=payment)

            log_embed.timestamp = discord.utils.utcnow()

            await log_channel.send(embed=log_embed)

    async def auto_vouch_loop(self):

        while self.running:

            wait = random.uniform(1,2.5)

            await asyncio.sleep(wait * 3600)

            if self.running:
                await self.send_vouch()


bot = VouchBot()


@bot.command()
async def start(ctx):

    if bot.running:
        await ctx.send("Auto vouch already running.")
        return

    bot.running = True

    await ctx.send("Auto vouch system started.")

    for _ in range(10):

        await bot.send_vouch()

        await asyncio.sleep(random.uniform(1,3))

    bot.loop.create_task(bot.auto_vouch_loop())


@bot.command()
async def stop(ctx):

    bot.running = False

    await ctx.send("Auto vouch stopped.")


@bot.tree.command(name="vouch",description="Leave a vouch")
async def vouch(interaction: discord.Interaction):

    global VOUCH_COUNT

    channel = bot.get_channel(VOUCH_CHANNEL_ID)

    VOUCH_COUNT += 1

    product = random.choice(list(PRODUCTS.keys()))
    price = round(random.uniform(5,10),2)

    embed = discord.Embed(
        title="⭐ Customer Review",
        description=f"> {random.choice(REVIEWS)}",
        color=discord.Color.green()
    )

    embed.add_field(name="📦 Product",value=product)
    embed.add_field(name="💰 Price",value=f"${price}")
    embed.add_field(name="📊 Total Vouches",value=f"{VOUCH_COUNT}+")

    embed.set_footer(text="Verified Purchase")

    await channel.send(embed=embed)

    await interaction.response.send_message("Vouch submitted.",ephemeral=True)


@bot.tree.command(name="showvouches",description="Show total vouches")
async def showvouches(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"Total Vouches: **{VOUCH_COUNT}+**"
    )


bot.run(TOKEN)
