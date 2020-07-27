"""Miscellaneous commands limited to bot owner"""

import discord
from discord.ext import commands

from datetime import datetime

from utils import helpers


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return ctx.author.id in (self.bot.owner_id, 629552716150210562)

    @commands.command(
        name="guilds", 
        description="Shows the list of servers the bot is in",
        aliases=["servers"],
    )
    async def guilds(self, ctx):
        headers = ["ID", "MEMBERS", "NAME"]
        guild_list = [
            (guild.id, len(guild.members), guild.name)
            for guild in self.bot.guilds
        ]
        guild_list = helpers.format_columns(
            *zip(*guild_list), headers=headers
        )
        embed = discord.Embed(
            title=f"{self.bot.user.name} has joined these servers", 
            description=guild_list, 
            colour=ctx.author.color
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))