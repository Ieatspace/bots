import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

print("Token loaded:", TOKEN is not None)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_NAME = "Private Chats"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is in these servers:", bot.guilds)

    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)

        if category is None:
            category = await guild.create_category(CATEGORY_NAME)

        for member in guild.members:
            if member.bot:
                continue
            await create_private_channel(member, category)


@bot.event
async def on_member_join(member):
    guild = member.guild
    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)

    if category is None:
        category = await guild.create_category(CATEGORY_NAME)

    await create_private_channel(member, category)


async def create_private_channel(member, category):
    guild = member.guild
    owner = guild.owner

    channel_name = f"private-{member.name.lower()}"

    # Check if channel already exists
    existing = discord.utils.get(category.channels, name=channel_name)
    if existing:
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        owner: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    channel = await guild.create_text_channel(
        channel_name,
        overwrites=overwrites,
        category=category
    )

    await channel.send(
        f"Hello {member.mention}! This is your private channel with the server owner."
    )


bot.run(TOKEN)
