import discord
from discord import Color, slash_command, message_command
from discord.commands import Option
from discord.ext import commands

import db
import utils


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.DB()

    @slash_command(name='x-move-message', description='[ADMIN] Moves messages from a channel to the target one')
    @commands.has_permissions(administrator=True)
    async def move_message(self, ctx, channel: utils.OPTION_CHANNEL,
                           msg_ids: Option(str, 'Comma-separated message IDs')):
        content = ''
        for msg_id in utils.str_to_list(msg_ids):
            msg = await ctx.fetch_message(int(msg_id))
            await msg.delete()
            content += '**A message by <@{}> has been moved from <#{}>:**\n\n{}\n\n' \
                .format(msg.author.id, msg.channel.id, msg.content)

        await channel.send(content.replace('@everyone', 'everyone').replace('@here', 'here'))
        await utils.send_disappearing_response(ctx, 'Messages have been moved!')

    @slash_command(name='x-send-message', description='[ADMIN] Sends a message to a channel')
    @commands.has_permissions(administrator=True)
    async def send_message(self, ctx, channel: utils.OPTION_CHANNEL, message: Option(str, 'Message content')):
        await channel.send(message)
        await utils.send_disappearing_response(ctx, 'You have sent the message.')

    @slash_command(name='x-remove-point', description='[ADMIN] Removes one point from a user')
    @commands.has_permissions(administrator=True)
    async def remove_acknowledgment(self, ctx, user: utils.OPTION_USER):
        self.db.delete_single_user_acknowledgment(user.id)
        await utils.send_disappearing_response(ctx, 'You have removed 1 point.')

    @slash_command(name='x-choose-winners',
                   description='[ADMIN] Chooses N random members who have reacted to a message')
    @commands.has_permissions(administrator=True)
    async def choose_winners(self, ctx, msg_id: utils.OPTION_MSG_ID, channel: utils.OPTION_CHANNEL,
                             members_count: Option(int, 'Member count'), emoji: Option(str, 'Emoji'),
                             mention: Option(str, 'Do you want to mention the users?', choices=['Yes', 'No']) = None,
                             role: Option(discord.Role, 'Set a role') = None):
        await utils.get_reaction_users(self.bot, ctx, msg_id, channel, members_count, emoji, 'Winners', mention,
                                       role)

    @slash_command(name='x-reaction-users', description='[ADMIN] Shows all the members who have reacted to a message')
    @commands.has_permissions(administrator=True)
    async def reaction_users(self, ctx, msg_id: utils.OPTION_MSG_ID, channel: utils.OPTION_CHANNEL,
                             emoji: Option(str, 'Emoji'),
                             mention: Option(str, 'Do you want to mention the users?', choices=['Yes', 'No']) = None,
                             role: Option(discord.Role, 'Set a role') = None):
        await utils.get_reaction_users(self.bot, ctx, msg_id, channel, 0, emoji, 'Reactions', mention, role)

    @slash_command(name='x-poll', description='[ADMIN] Creates a poll')
    @commands.has_permissions(administrator=True)
    async def create_poll(self, ctx, question: Option(str, 'Poll question'),
                          options: Option(str, 'Comma-separated poll options - up to 10. '
                                               'Type "None" and they will be Yes/No.')):
        if options == 'None':
            options = ['Yes', 'No']
            reactions = ['✅', '❌']
        else:
            options = utils.str_to_list(options)
            reactions = utils.POLL_REACTIONS

        description = '**{}**\n'.format(question)
        for idx, option in enumerate(options):
            description += '\n {} {}'.format(reactions[idx], option)

        react_message = await utils.show_embed(ctx, title='📊 Poll', description=''.join(description), loadingText=True)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @slash_command(name='x-purge', description='[ADMIN] Deletes N messages from the current channel')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit: Option(int, 'Number of messages', min_value=1, max_value=99)):
        await ctx.channel.purge(limit=limit)
        await utils.send_disappearing_response(ctx, f'You have purged {limit} messages.')

    @slash_command(name='report', description='Sends a message to the admins')
    async def report(self, ctx, message: Option(str, 'Your message')):
        await utils.send_message_to_admins(self.bot, None, 'Report', message, Color.red(), ctx)
        await utils.send_disappearing_response(ctx, 'Thank you for your report!')

    @message_command(name='Report message')
    async def report_message(self, ctx, message: discord.Message):
        await utils.send_message_to_admins(self.bot, None, 'Reported message',
                                           f'{message.content}\n\nLink: {message.jump_url}', Color.red(), ctx)
        await utils.send_disappearing_response(ctx, 'Thank you for your report!')

    @move_message.error
    @send_message.error
    @remove_acknowledgment.error
    @choose_winners.error
    @reaction_users.error
    @create_poll.error
    @purge.error
    async def permssion_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await utils.send_disappearing_response(ctx, 'You have no permissions!')


def setup(bot):
    bot.add_cog(Admin(bot))
