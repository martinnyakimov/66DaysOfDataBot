from dateutil import parser
from datetime import datetime, timedelta
from discord import Embed, Color, utils
from dotenv import load_dotenv
import os
import re

load_dotenv()
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
SCAM_TITLE = 'Discord Nitro scam detected!'
PROGRESS_66TH_DAY_DETECTED = '66th day has been detected!'


def get_timestamp_difference(timestamp):
    if not timestamp:
        return

    diff = datetime.utcnow() - parser.parse(timestamp)
    return diff.seconds / 60


def get_n_days_ago(n):
    return datetime.now() - timedelta(days=n)


async def show_embed(ctx, description, title=None, color=Color.blue(), isSuccessful=False, isError=False,
                     message=None, channel=None, addAuthor=False):
    if isSuccessful:
        title = 'Success!'
        color = Color.green()

    if isError:
        title = 'Error!'
        color = Color.red()

    embed = Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
    author = ctx.author if ctx is not None else message.author
    if addAuthor: embed.set_author(name=author, icon_url=author.avatar_url)

    if channel is not None:
        await channel.send(embed=embed)
    else:
        await ctx.send(embed=embed)


async def send_admin_message(bot, message, title, description, color):
    channel = utils.get(bot.get_all_channels(), name=LOG_CHANNEL)
    await show_embed(message=message, channel=channel, ctx=None,
                     title=title, description=description, color=color, addAuthor=True)


async def antispam_protection(bot, message):
    keywords_detected = len(re.findall(r'(?i)free|discord|nitro|everyone|steam|dls|airdrop', message.content))
    if keywords_detected >= 3:
        await message.delete()
        await send_admin_message(bot, message, SCAM_TITLE, '**Message:** ' + message.content, Color.red())
        await message.author.ban(reason=SCAM_TITLE)


def detect_progress_day(content):
    content = re.findall(r'(?i)\bday\b[\s]+[\d-]+|day[\d-]+', content)

    if content:
        return int(content[-1].lower().replace('day', '').strip())


async def detect_66th_day(bot, message):
    if detect_progress_day(message.content) == 66:
        await send_admin_message(bot, message, PROGRESS_66TH_DAY_DETECTED, message.jump_url, Color.green())
