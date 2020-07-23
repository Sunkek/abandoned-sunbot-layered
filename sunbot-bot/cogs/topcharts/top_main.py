import discord
from discord.ext import commands


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
        if not ctx.command.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), "top")


def setup(bot):
    bot.add_cog(TopCharts(bot))
