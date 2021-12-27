import discord
from discord.ext import commands
import utils


class Progress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='last-day', brief='Checks the last day of your last message (14-day archive)')
    async def last_day(self, ctx, user: discord.User = None):
        if ctx.channel.name != 'progress':
            await utils.show_embed(ctx=ctx, description='You can use this command only in #progress.', isError=True)
            return

        await self.get_messages(ctx, user.id) if user is not None \
            else await self.get_messages(ctx, ctx.author.id)

    @staticmethod
    async def get_messages(ctx, author_id: int):
        messages = await ctx.channel.history(limit=None, after=utils.get_n_days_ago(14)).flatten()

        found = False
        for msg in reversed(messages):
            if msg.author.id == author_id:
                last_day = utils.detect_progress_day(msg.content)
                if last_day:
                    await ctx.send('The last message is marked as day **{}**.'.format(last_day))
                    found = True
                    break

        if not found:
            await utils.show_embed(ctx=ctx, isError=True,
                                   description='The last day has not been found.\n\nPossible reasons:\n**1)** Your last message has been posted more than 14 days ago.\n**2)** You have not included the day in your message *(e.g. Day 25)*.')


def setup(bot):
    bot.add_cog(Progress(bot))
