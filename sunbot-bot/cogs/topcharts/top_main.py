import discord
from discord.ext import commands

from typing import Optional, Union
from datetime import datetime, timedelta
from asyncio import TimeoutError, wait, FIRST_COMPLETED

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
        channel_name = f"in {channel.name}" if channel else ""
        channel = channel.id if channel else channel
        top_chart = await rest_api.get_top(
            self.bot, 
            "postcounts", 
            time_range,
            guild_id=ctx.guild.id,
            channel_id=channel,
        )
        user_ids = [i["user_id"] for i in top_chart["results"]]
        postcounts = [i["count"] for i in top_chart["results"]]
        user_ids, postcounts = zip(*[
            (i["user_id"], i["count"]) for i in top_chart["results"]
        ])
        user_ids = [
            await utils.get_member_name(
                self.bot, ctx.guild, i
            ) for i in user_ids
        ]
        postcounts = list(postcounts)
        headers = ["POSTCOUNT", "MEMBER"]
        footers = [top_chart["total"], "TOTAL"]
        table = utils.format_columns(
            postcounts, user_ids, headers=headers, footers=footers
        )
        embed = discord.Embed(
            title=f"Top postcounts for {time_range} {channel_name}",
            color=ctx.author.color,
            description=f"`{table}`", 
        )
        embed.set_footer(text=f"Page {top_chart['current']}/{top_chart['last']}")
        message = await ctx.send(embed=embed)
        for i in ["⏮️", "⏪", "⏩", "⏭️"]:
            await message.add_reaction(i)
        
        def check(payload):
            return all((
                payload.user_id == ctx.author.id,
                payload.message_id == message.id,
                str(payload.emoji) in ["⏮️", "⏪", "⏩", "⏭️"],
            ))

        while True:
            done, pending = await wait([
                self.bot.wait_for("raw_reaction_add", check=check),
                self.bot.wait_for("raw_reaction_remove", check=check),
            ], return_when=FIRST_COMPLETED, timeout=20.0, )
            try:
                payload = done.pop().result()
            except KeyError:
                await message.clear_reactions()
                for future in pending: future.cancel()
                break
            if str(payload.emoji) == "⏮️" and top_chart["current"] != 1:
                url = top_chart["next"] or top_chart["previous"]
                url = url.split("?")[0] + "?page=1"
                top_chart = await rest_api.send_get(
                    self.bot, 
                    url, 
                    guild_id=ctx.guild.id,
                    channel_id=channel,
                )
                user_ids = [
                    await utils.get_member_name(
                        self.bot, ctx.guild, i
                    ) for i in user_ids
                ]
                postcounts = list(postcounts)
                headers = ["POSTCOUNT", "MEMBER"]
                footers = [top_chart["total"], "TOTAL"]
                table = utils.format_columns(
                    postcounts, user_ids, headers=headers, footers=footers
                )
                embed.description=f"`{table}`"
                embed.set_footer(
                    text=f"Page {top_chart['current']}/{top_chart['last']}"
                )
                await message.edit(embed=embed)
            elif str(payload.emoji) == "⏪" and top_chart["previous"]:
                top_chart = await rest_api.send_get(
                    self.bot, 
                    top_chart["previous"], 
                    guild_id=ctx.guild.id,
                    channel_id=channel,
                )
                user_ids = [i["user_id"] for i in top_chart["results"]]
                postcounts = [i["count"] for i in top_chart["results"]]
                user_ids, postcounts = zip(*[
                    (i["user_id"], i["count"]) for i in top_chart["results"]
                ])
                user_ids = [
                    await utils.get_member_name(
                        self.bot, ctx.guild, i
                    ) for i in user_ids
                ]
                postcounts = list(postcounts)
                headers = ["POSTCOUNT", "MEMBER"]
                footers = [top_chart["total"], "TOTAL"]
                table = utils.format_columns(
                    postcounts, user_ids, headers=headers, footers=footers
                )
                embed.description=f"`{table}`"
                embed.set_footer(
                    text=f"Page {top_chart['current']}/{top_chart['last']}"
                )
                await message.edit(embed=embed)
            elif str(payload.emoji) == "⏩" and top_chart["next"]:
                top_chart = await rest_api.send_get(
                    self.bot, 
                    top_chart["next"], 
                    guild_id=ctx.guild.id,
                    channel_id=channel,
                )
                user_ids = [i["user_id"] for i in top_chart["results"]]
                postcounts = [i["count"] for i in top_chart["results"]]
                user_ids, postcounts = zip(*[
                    (i["user_id"], i["count"]) for i in top_chart["results"]
                ])
                user_ids = [
                    await utils.get_member_name(
                        self.bot, ctx.guild, i
                    ) for i in user_ids
                ]
                postcounts = list(postcounts)
                headers = ["POSTCOUNT", "MEMBER"]
                footers = [top_chart["total"], "TOTAL"]
                table = utils.format_columns(
                    postcounts, user_ids, headers=headers, footers=footers
                )
                embed.description=f"`{table}`"
                embed.set_footer(
                    text=f"Page {top_chart['current']}/{top_chart['last']}"
                )
                await message.edit(embed=embed)
            elif str(payload.emoji) == "⏭️" and top_chart["current"] != top_chart["last"]:
                url = top_chart["next"] or top_chart["previous"]
                url = url.split("?")[0] + f"?page={top_chart['last']}"
                top_chart = await rest_api.send_get(
                    self.bot, 
                    url, 
                    guild_id=ctx.guild.id,
                    channel_id=channel,
                )
                user_ids = [i["user_id"] for i in top_chart["results"]]
                postcounts = [i["count"] for i in top_chart["results"]]
                user_ids, postcounts = zip(*[
                    (i["user_id"], i["count"]) for i in top_chart["results"]
                ])
                user_ids = [
                    await utils.get_member_name(
                        self.bot, ctx.guild, i
                    ) for i in user_ids
                ]
                postcounts = list(postcounts)
                headers = ["POSTCOUNT", "MEMBER"]
                footers = [top_chart["total"], "TOTAL"]
                table = utils.format_columns(
                    postcounts, user_ids, headers=headers, footers=footers
                )
                embed.description=f"`{table}`"
                embed.set_footer(
                    text=f"Page {top_chart['current']}/{top_chart['last']}"
                )
                await message.edit(embed=embed)
            for future in pending: future.cancel()



def setup(bot):
    bot.add_cog(TopCharts(bot))
