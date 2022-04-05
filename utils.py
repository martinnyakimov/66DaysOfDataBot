import os
import random
import re
from datetime import datetime, timedelta

import discord
from dateutil import parser
from discord import Embed, Color, utils
from discord.commands import Option
from dotenv import load_dotenv

load_dotenv()
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
OPTION_CHANNEL = Option(discord.TextChannel, 'Choose a channel')
OPTION_USER = Option(discord.User, 'Choose a user')
OPTION_MSG_ID = Option(str, 'Message ID')

SCAM_TITLE = 'Discord Nitro scam detected!'
PROGRESS_66TH_DAY_DETECTED = '66th day has been detected!'

SPAM_KEYWORDS_REGEX = r'(?i)everyone|free\b|discord|dls|discr|dis|nitro|steam|airdrop|gift|month|first'
PROGRESS_DAY_REGEX = r'(?i)\bday\b[\s]+[\d]+|day[\d]+|d[\d]+|day-[\d]+|d-[\d]+'
POLL_REACTIONS = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']


async def send_disappearing_response(ctx, message, delete_after=1):
    await ctx.respond(message, delete_after=delete_after)


async def show_embed(ctx, description, title=None, color=Color.blue(), isSuccessful=False, isError=False,
                     message=None, channel=None, addAuthor=False, loadingText=False):
    if isSuccessful:
        title = 'Success!'
        color = Color.green()

    if isError:
        title = 'Error!'
        color = Color.red()

    embed = Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
    if addAuthor:
        author = ctx.author if ctx is not None else message.author
        embed.set_author(name=author, icon_url=author.display_avatar)

    if channel is not None:
        return await channel.send(embed=embed)

    if loadingText:
        await send_disappearing_response(ctx, 'Loading...', 0.5)
        return await ctx.channel.send(embed=embed)

    return await ctx.respond(embed=embed)


async def send_message_to_admins(bot, message, title, description, color, ctx=None):
    channel = utils.get(bot.get_all_channels(), name=os.getenv('LOG_CHANNEL'))
    await show_embed(message=message, channel=channel, ctx=ctx,
                     title=title, description=description, color=color, addAuthor=True)


async def antispam_protection(bot, message):
    if message.author.guild_permissions.administrator:
        return

    keywords_detected = len(set(re.findall(SPAM_KEYWORDS_REGEX, message.content)))
    url_detected = re.search(r'(https?://[^\s]+)', message.content)
    if keywords_detected >= 3 and url_detected:
        await message.delete()
        await send_message_to_admins(bot, message, SCAM_TITLE, '**Message:** ' + message.content, Color.red())
        await message.author.ban(reason=SCAM_TITLE)


def detect_progress_day(content):
    content = re.findall(PROGRESS_DAY_REGEX, content)

    if content:
        return int(re.findall('\d+', content[-1])[0])


async def detect_66th_day(bot, message):
    if detect_progress_day(message.content) == 66:
        await send_message_to_admins(bot, message, PROGRESS_66TH_DAY_DETECTED, message.jump_url, Color.green())


async def get_reaction_users(bot, ctx, msg_id: int, channel: discord.TextChannel, members_count: int, emoji: str,
                             title: str, mention: str, role: discord.Role = None):
    msg = await channel.fetch_message(msg_id)
    guild = bot.get_guild(ctx.guild.id)

    if 'POLL_' in emoji:
        emoji = POLL_REACTIONS[int(emoji.replace('POLL_', '')) - 1]  # Get a poll reaction emoji

    user_list = []
    for reaction in msg.reactions:
        if str(reaction) == emoji:
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

    await ctx.respond(f'**{title}**\n' + '\n'.join(usernames))


def str_to_list(string: str):
    return string.replace(' ', '').split(',')


def get_timestamp_difference(timestamp):
    if not timestamp:
        return

    diff = datetime.utcnow() - parser.parse(timestamp)
    return diff.seconds / 60


def get_n_days_ago(n):
    return datetime.now() - timedelta(days=n)
