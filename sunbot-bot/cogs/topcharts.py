import discord
from discord.ext import commands

from typing import Optional, Union
from datetime import datetime, timedelta
from asyncio import TimeoutError, wait, FIRST_COMPLETED

from utils import helpers, rest_api, paginator


class TopCharts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_ranges = ('month', 'year', 'alltime')

    @commands.group(
        description="This is a command group that shows you the top chart of something", 
        name="top", 
        aliases=['t'], 
        invoke_without_command=True,
    )
    async def top(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), target="top")

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
        top_chart = await rest_api.get_top(
            self.bot, 
            "postcounts", 
            time_range,
            guild_id=ctx.guild.id,
            channel_id=channel.id if channel else None,
        )
        columns = await helpers.parse_top_json(top_chart, ctx)
        headers = ["POSTCOUNT", "MEMBER"]
        footers = [top_chart["total"], "TOTAL"]
        table = helpers.format_columns(
            columns["counts"], columns["user_names"], 
            headers=headers, footers=footers
        )
        channel = f"in {channel.name}" if channel else ""
        embed = discord.Embed(
            title=f"Top postcounts for {time_range} {channel}",
            color=ctx.author.color,
            description=f"`{table}`", 
        )
        embed.set_footer(text=f"Page {top_chart['current']}/{top_chart['last']}")
        message = await ctx.send(embed=embed)
        await paginator.paginate(ctx, message, top_chart, headers, footers)

def setup(bot):
    bot.add_cog(TopCharts(bot))
