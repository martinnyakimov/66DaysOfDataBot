import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import db
import utils

load_dotenv()
WAITING_TIME = int(os.getenv('WAITING_TIME'))


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.DB()

    @commands.command(name='leaderboard', brief='Shows the ranking of the users with points')
    async def list_acknowledgments(self, ctx):
        users = self.db.list_acknowledgments()
        leaderboard_txt = ''
        medals = {1: '🥇', 2: '🥈', 3: '🥉'}

        for idx, user_count in enumerate(users):
            place = idx + 1
            place = medals[place] if place in medals else str(place) + '.'
            leaderboard_txt += '{} **{}**: {} points\n'.format(place, await self.bot.fetch_user(user_count[0]),
                                                               user_count[1])

        await utils.show_embed(ctx=ctx, title='🏆 Leaderboard', description=leaderboard_txt)

    @commands.command(name='thanks', brief='Adds one point to a user')
    async def add_acknowledgment(self, ctx, user: discord.User):
        if ctx.author.id == user.id:
            await utils.show_embed(ctx=ctx, description='You can use this command for yourself.', isError=True)
            return

        last_ackt_diff = utils.get_timestamp_difference(self.db.get_last_user_acknowledgment(ctx.author.id, user.id))
        if last_ackt_diff is not None and last_ackt_diff < WAITING_TIME:
            desc = 'You have to wait {} more minutes before to acknowledge again.'.format(
                int(WAITING_TIME - last_ackt_diff))
            await utils.show_embed(ctx=ctx, description=desc, isError=True)
            return

        self.db.add_acknowledgment(ctx.author.id, user.id)
        await utils.show_embed(ctx=ctx, description='You have acknowledged {} for their help.'.format(user.name),
                               isSuccessful=True)

    @add_acknowledgment.error
    async def add_acknowledgment_error(self, ctx, error):
        if isinstance(error, commands.errors.UserNotFound):
            await utils.show_embed(ctx=ctx, description='User not found.', isError=True)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
