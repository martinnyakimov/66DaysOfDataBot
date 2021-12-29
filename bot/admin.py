import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import has_permissions
import utils
import db


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.DB()

    @commands.command(name='move-msg', hidden=True)
    @has_permissions(administrator=True)
    async def move_message(self, ctx, channel: discord.TextChannel, msg_id: int):
        msg = await ctx.fetch_message(msg_id)
        await msg.delete()
        await ctx.message.delete()

        await channel.send('**A message by <@{}> has been moved from <#{}>:**\n\n{}'
                           .format(msg.author.id, msg.channel.id, msg.content))

    @commands.command(name='msg', hidden=True)
    @has_permissions(administrator=True)
    async def send_message(self, ctx, channel: discord.TextChannel, *, message):
        await ctx.message.delete()
        await channel.send(message)

    @commands.command(name='rm-point', hidden=True)
    @has_permissions(administrator=True)
    async def remove_acknowledgment(self, ctx, user: discord.User):
        self.db.delete_single_user_acknowledgment(user.id)
        await ctx.send('You have removed 1 point.')

    @commands.command(name='report', brief='Sends a message to the admins')
    async def report(self, ctx, *, message):
        await ctx.message.delete()
        await utils.send_admin_message(self.bot, None, 'Report', message, Color.red(), ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
