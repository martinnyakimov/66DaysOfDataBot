import discord
from discord.ext import commands
from dotenv import load_dotenv
import utils
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
activity = discord.Activity(type=discord.ActivityType.watching, name='Ken Jee')
bot = commands.Bot(command_prefix='!', activity=activity)


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))


@bot.event
async def on_message(message):
    if not message.guild:  # Disable DM commands.
        return

    await utils.antispam_protection(bot, message)
    await bot.process_commands(message)


bot.load_extension('bot.admin')
bot.load_extension('bot.leaderboard')
bot.load_extension('bot.progress')

bot.run(TOKEN)
