import os

import discord
from dotenv import load_dotenv

import utils

load_dotenv()
activity = discord.Activity(type=discord.ActivityType.watching, name='Ken Jee')
bot = discord.Bot(intents=discord.Intents.all(), activity=activity, debug_guilds=[os.getenv('DISCORD_SERVER_ID')])


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))


@bot.event
async def on_message(message):
    if not message.guild:  # Disable DM commands.
        return

    await utils.antispam_protection(bot, message)
    if message.channel.name == 'progress':
        await utils.detect_66th_day(bot, message)


bot.load_extension('bot.admin')
bot.load_extension('bot.leaderboard')
bot.load_extension('bot.progress')

bot.run(os.getenv('TOKEN'))
