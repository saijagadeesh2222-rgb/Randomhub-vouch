import discord
from discord.ext import commands
from discord import app_commands
import random
import string
import asyncio
import os

TOKEN = os.getenv("TOKEN")

LOG_CHANNEL_ID = 1480475760618770629
VOUCH_CHANNEL_ID = 1479868238396653578

VOUCH_COUNT = 436
ORDER_NUMBER = 436
TOTAL_SALES = 0
TOTAL_REVENUE = 0

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

PAYMENTS = ["LTC","BTC","PayPal","USDT","ETH"]

# Huge review generator
START = [
"super","very","extremely","honestly","actually",
"definitely","ngl","fr","legit","really"
]

MIDDLE = [
"fast delivery","great seller","clean script",
"works perfectly","smooth transaction",
"quick response","amazing product",
"no issues at all","instant delivery",
"very good support","high quality script",
"everything works","easy setup",
"great communication","very professional"
]

END = [
"highly recommend","10/10","worth the price",
"best purchase","will buy again",
"super happy","thanks a lot",
"great experience","perfect service",
"works flawlessly"
]

def generate_review():
    return f"{random.choice(START)} {random.choice(MIDDLE)} {random.choice(END)}"

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
        global TOTAL_REVENUE
        global TOTAL_SALES

        vouch_channel = self.get_channel(VOUCH_CHANNEL_ID)
        log_channel = self.get_channel(LOG_CHANNEL_ID)

        if not vouch_channel:
            return

        guild = vouch_channel.guild
        member = await self.get_random_member(guild)

        product = random.choice(list(PRODUCTS.keys()))
        min_price,max_price = PRODUCTS[product]

        price = round(random.uniform(min_price,max_price),2)

        TOTAL_REVENUE += price
        TOTAL_SALES += 1

        rating = round(random.uniform(4.3,5.0),1)

        payment = random.choice(PAYMENTS)
        seller_id = random.choice(SELLERS)

        ORDER_NUMBER += 1
        VOUCH_COUNT += 1

        transaction = ''.join(random.choices(string.ascii_uppercase + string.digits,k=10))

        embed = discord.Embed(
            title="⭐ Verified Customer Review",
            description=f"**{generate_review()}**",
            color=discord.Color.gold()
        )

        embed.set_author(
            name=f"{member.name}",
            icon_url=member.display_avatar.url
        )

        embed.add_field(name="👤 Customer",value=member.mention)
        embed.add_field(name="🧑‍💼 Seller",value=f"<@{seller_id}>")

        embed.add_field(name="📦 Product",value=product,inline=False)

        embed.add_field(name="⭐ Rating",value=f"{rating}/5")
        embed.add_field(name="💰 Price",value=f"${price}")
        embed.add_field(name="💳 Payment",value=payment)

        embed.add_field(
            name="🧾 Order Info",
            value=f"Order #: **{ORDER_NUMBER}**\nTransaction: **{transaction}**",
            inline=False
        )

        embed.add_field(
            name="📊 Total Vouches",
            value=f"**{VOUCH_COUNT}+**",
            inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(text="Random Hub Marketplace • Verified Purchase")

        embed.timestamp = discord.utils.utcnow()

        async with vouch_channel.typing():
            await asyncio.sleep(random.uniform(2,6))

        msg = await vouch_channel.send(embed=embed)

        await asyncio.sleep(random.uniform(5,12))

        await msg.reply(
            f"Thank you for purchasing **{product}**! If you need help contact the seller.",
            mention_author=False
        )

        if log_channel:

            log = discord.Embed(
                title="🛒 Purchase Log",
                color=discord.Color.blue()
            )

            log.add_field(name="Customer",value=member.mention)
            log.add_field(name="Seller",value=f"<@{seller_id}>")
            log.add_field(name="Product",value=product)
            log.add_field(name="Price",value=f"${price}")
            log.add_field(name="Payment",value=payment)

            log.timestamp = discord.utils.utcnow()

            await log_channel.send(embed=log)

    async def auto_vouch_loop(self):

        while self.running:

            daily_vouches = random.randint(10,18)

            for _ in range(daily_vouches):

                wait = random.uniform(1,3) * 3600
                await asyncio.sleep(wait)

                if self.running:
                    await self.send_vouch()

bot = VouchBot()

@bot.command()
async def start(ctx):

    if bot.running:
        await ctx.send("Auto vouch already running.")
        return

    bot.running = True

    await ctx.send("✅ Auto vouch system started.")

    bot.loop.create_task(bot.auto_vouch_loop())

@bot.command()
async def stop(ctx):

    bot.running = False
    await ctx.send("⛔ Auto vouch stopped.")

@bot.tree.command(name="stats",description="Marketplace statistics")
async def stats(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📊 Marketplace Stats",
        color=discord.Color.green()
    )

    embed.add_field(name="Total Vouches",value=f"{VOUCH_COUNT}+")
    embed.add_field(name="Total Sales",value=TOTAL_SALES)
    embed.add_field(name="Revenue",value=f"${round(TOTAL_REVENUE,2)}")

    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
