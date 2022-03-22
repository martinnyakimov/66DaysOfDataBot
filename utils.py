import os
import random
import re
from datetime import datetime, timedelta

import discord
from dateutil import parser
from discord import Embed, Color, utils
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
SCAM_TITLE = 'Discord Nitro scam detected!'
PROGRESS_66TH_DAY_DETECTED = '66th day has been detected!'
SPAM_KEYWORDS_REGEX = r'(?i)everyone|free\b|discord|dls|discr|dis|nitro|steam|airdrop|gift|month|first'
PROGRESS_DAY_REGEX = r'(?i)\bday\b[\s]+[\d]+|day[\d]+|d[\d]+|day-[\d]+|d-[\d]+'
POLL_REACTIONS = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']


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
    if addAuthor:
        author = ctx.author if ctx is not None else message.author
        embed.set_author(name=author, icon_url=author.avatar_url)

    if channel is not None:
        return await channel.send(embed=embed)

    return await ctx.send(embed=embed)


async def send_admin_message(bot, message, title, description, color, ctx=None):
    channel = utils.get(bot.get_all_channels(), name=LOG_CHANNEL)
    await show_embed(message=message, channel=channel, ctx=ctx,
                     title=title, description=description, color=color, addAuthor=True)


async def antispam_protection(bot, message):
    if message.author.guild_permissions.administrator:
        return

    keywords_detected = len(set(re.findall(SPAM_KEYWORDS_REGEX, message.content)))
    url_detected = re.search(r'(https?://[^\s]+)', message.content)
    if keywords_detected >= 3 and url_detected:
        await message.delete()
        await send_admin_message(bot, message, SCAM_TITLE, '**Message:** ' + message.content, Color.red())
        await message.author.ban(reason=SCAM_TITLE)


def detect_progress_day(content):
    content = re.findall(PROGRESS_DAY_REGEX, content)

    if content:
        return re.findall('\d+', content[-1])[0]


async def detect_66th_day(bot, message):
    if detect_progress_day(message.content) == 66:
        await send_admin_message(bot, message, PROGRESS_66TH_DAY_DETECTED, message.jump_url, Color.green())


async def get_reaction_users(bot, ctx, msg_id: int, channel: discord.TextChannel, members_count: int, emoji_name: str,
                             title: str, mention: str, role: discord.Role = None):
    msg = await channel.fetch_message(msg_id)
    guild = bot.get_guild(ctx.guild.id)

    if 'POLL_' in emoji_name:
        emoji_name = POLL_REACTIONS[int(emoji_name.replace('POLL_', '')) - 1]  # Get a poll reaction emoji

    user_list = []
    for reaction in msg.reactions:
        if str(reaction) == emoji_name:
            user_list = [user async for user in reaction.users()]
            user_list.reverse()
            if members_count != 0: user_list = random.sample(user_list, members_count)

    usernames = []
    for user in user_list:
        if mention is not None and mention.lower() == 'yes':
            usernames.append(user.mention)
        else:
            usernames.append(str(await bot.fetch_user(user.id)))

        if role is not None:
            member = await guild.fetch_member(user.id)
            await member.add_roles(role)

    await ctx.send(f'**{title}**\n' + '\n'.join(usernames))
