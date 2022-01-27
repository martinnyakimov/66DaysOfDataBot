import random

import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import has_permissions

import db
import utils


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.DB()

    @commands.command(name='move-msg', hidden=True)
    @has_permissions(administrator=True)
    async def move_message(self, ctx, channel: discord.TextChannel, *, msg_ids: str):
        await ctx.message.delete()

        content = ''
        for msg_id in msg_ids.split(' '):
            msg = await ctx.fetch_message(int(msg_id))
            await msg.delete()
            content += '**A message by <@{}> has been moved from <#{}>:**\n\n{}\n\n' \
                .format(msg.author.id, msg.channel.id, msg.content)

        await channel.send(content)

    @commands.command(name='msg', hidden=True)
    @has_permissions(administrator=True)
    async def send_message(self, ctx, channel: discord.TextChannel, *, message: str):
        await ctx.message.delete()
        await channel.send(message)

    @commands.command(name='rm-point', hidden=True)
    @has_permissions(administrator=True)
    async def remove_acknowledgment(self, ctx, user: discord.User):
        self.db.delete_single_user_acknowledgment(user.id)
        await ctx.send('You have removed 1 point.')

    @commands.command(name='choose-winners', hidden=True)
    @has_permissions(administrator=True)
    async def choose_winners(self, ctx, msg_id: int, channel: discord.TextChannel, num_of_winners: int,
                             emoji_name: str):
        msg = await channel.fetch_message(msg_id)

        for reaction in msg.reactions:
            if str(reaction) == emoji_name:
                user_list = [user async for user in reaction.users()]
                winners = random.sample(user_list, num_of_winners)
                await ctx.send('**Winners**\n' + '\n'.join(user.mention for user in winners))

    @commands.command(name='poll', hidden=True)
    @has_permissions(administrator=True)
    async def create_poll(self, ctx, question: str, *options: str):
        await ctx.message.delete()

        if len(options) == 0:
            options = ['Yes', 'No']
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = '**{}**\n'.format(question)
        for idx, option in enumerate(options):
            description += '\n {} {}'.format(reactions[idx], option)

        react_message = await utils.show_embed(ctx, title='📊 Poll', description=''.join(description))
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @commands.command(name='report', brief='Sends a message to the admins')
    async def report(self, ctx, *, message: str):
        await ctx.message.delete()
        await utils.send_admin_message(self.bot, None, 'Report', message, Color.red(), ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
