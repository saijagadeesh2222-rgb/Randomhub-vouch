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

VOUCH_COUNT = 435
ORDER_NUMBER = 436
TOTAL_SALES = 435
TOTAL_REVENUE = 1563

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
intents.message_content = True

class VouchBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.running = False

    async def setup_hook(self):
        await self.tree.sync()

    async def get_random_member(self, guild):

        members = [m for m in guild.members if not m.bot]

        if not members:
            return None

        return random.choice(members)

    async def send_vouch(self):

        global VOUCH_COUNT, ORDER_NUMBER, TOTAL_REVENUE, TOTAL_SALES

        vouch_channel = self.get_channel(VOUCH_CHANNEL_ID)
        log_channel = self.get_channel(LOG_CHANNEL_ID)

        if not vouch_channel:
            return

        guild = vouch_channel.guild
        member = await self.get_random_member(guild)

        if not member:
            return

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

        transaction = ''.join(random.choices(string.ascii_uppercase +
