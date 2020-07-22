import discord
from discord.ext import commands

from typing import Optional, Union
from datetime import datetime, timedelta

from utils import utils, rest_api


class TopCharts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_ranges = ('month', 'year', 'alltime')

    async def topchart(
        self, ctx, chart, time_range, 
        member_ids=None, guild_id=None, channel_id=None, game=None,
    ):
        result = await rest_api.get_top(
            self.bot, 
            chart, 
            time_range,
            member_ids=member_ids,
            guild_id=guild_id,
            channel_id=channel_id,
            game=game,
        )
        return result

    @commands.group(
        description="This is a command group that shows you the top chart of something", 
        name="top", 
        aliases=['t'], 
        invoke_without_command=True,
    )
    async def top(self, ctx):
        if not ctx.command.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), "top")

    # Top postcounts
    @top.command(
        description="Shows you who posted the most in the current `month/year/alltime`",
        name="postcounts", 
        aliases=["pc",],
    )
    async def top_postcounts(
        self, ctx, channel: Optional[discord.TextChannel]=None, time_range="month"
    ):
        if time_range not in self.time_ranges:
            raise commands.BadArgument
        channel = channel.id if channel else channel
        top_chart = await rest_api.get_top(
            self.bot, 
            "postcounts", 
            time_range,
            guild_id=ctx.guild.id,
            channel_id=channel,
        )
        print(top_chart)

        user_ids = top_chart["results"][0].keys()
        postcounts = top_chart["results"][0].values()
        table = utils.format_columns(user_ids, postcounts)

        embed = discord.Embed(
            description=f"`{table}`", 
            color=ctx.author.color,
            title=f"Top postcounts for {time_range}"
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TopCharts(bot))
