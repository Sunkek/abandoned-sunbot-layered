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
            self.bot, "postcounts", time_range,
            guild_id=ctx.guild.id,
            channel_id=channel.id if channel else None,
        )
        columns = await helpers.parse_top_json(top_chart["results"], ctx)
        headers = ["POSTCOUNT", "MEMBER"]
        column_keys = ["count", "user_name"]
        footers = [top_chart["total"], "TOTAL"]
        use_columns = [columns[i] for i in column_keys]
        table = helpers.format_columns(
            *use_columns, 
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
        await paginator.paginate(
            ctx, message, top_chart, column_keys, headers=headers, footers=footers
        )

    # Top postcounts
    @top.command(
        description="Shows you the most used emotes for the current `month/year/alltime`",
        name="emotes", 
        aliases=["e",],
    )
    async def top_emotes(
        self, ctx, time_range="month"
    ):
        if time_range not in self.time_ranges:
            raise commands.BadArgument
        target_pool = helpers.make_guild_emote_list(ctx)
        top_chart = await rest_api.get_top(
            self.bot, "emotes", time_range,
            guild_id=ctx.guild.id, target_pool=target_pool,
        )
        columns = await helpers.parse_top_json(top_chart["results"], ctx)
        headers = ["TOTAL", "MESSAGES", "REACTIONS", "EMOTE"]
        column_keys = ["total_count", "message_count", "reaction_count", "emote"]
        use_columns = [columns[i] for i in column_keys]
        table = helpers.format_columns(
            *use_columns, 
            headers=headers, 
        )
        embed = discord.Embed(
            title=f"Top used emotes for {time_range}",
            color=ctx.author.color,
            description=f"`{table.rstrip('``')}", 
        )
        embed.set_footer(text=f"Page {top_chart['current']}/{top_chart['last']}")
        message = await ctx.send(embed=embed)
        await paginator.paginate(
            ctx, message, top_chart, column_keys, 
            headers=headers, target_pool=target_pool,
        )

def setup(bot):
    bot.add_cog(TopCharts(bot))
