from dateutil import parser
from datetime import datetime, timedelta
from discord import Embed, Color


def get_timestamp_difference(timestamp):
    if not timestamp:
        return

    diff = datetime.utcnow() - parser.parse(timestamp)
    return diff.seconds / 60

def get_n_days_ago(n):
    return datetime.now() - timedelta(days=n)

async def show_embed(ctx, description, title=None, color=Color.blue(), isSuccessful=False, isError=False,
                     addAuthor=False):
    if isSuccessful:
        title = 'Success!'
        color = Color.green()

    if isError:
        title = 'Error!'
        color = Color.red()

    embed = Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
    if addAuthor: embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
