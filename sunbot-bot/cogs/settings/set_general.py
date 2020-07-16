"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional
import utils
import rest_api

class SetGeneral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name='showsettings', 
        aliases=['settings', 'checksettings', 'ss'],
        description='Shows current settings for this server.',
    )
    async def showsettings(self, ctx):
        settings = self.bot.settings[ctx.guild.id]
        desc = '\n'.join([
            f'{utils.format_settings_key(key)}: {utils.format_settings_value(ctx.guild, value)}' 
            for key, value in settings.items()
            if value
        ])
        embed = discord.Embed(
            title=f'Current settings for {ctx.guild.name}',
            color=ctx.author.color,
            description=desc
        )
        await ctx.send(embed=embed)
       
    """@commands.command(
        name='setbirthdayfeed', 
        aliases=['birthdayfeed'],
        description='Sets up the specified channel as birthday feed. To reset, provide no channel.',
    )
    async def setbirthdayfeed(
        self, 
        ctx, 
        channel:Optional[discord.TextChannel]=9223372036854775800
    ):
        # Check if there's a channel specified
        if isinstance(channel, discord.TextChannel):
            birthday_feed = channel.id
            channel_log = channel.mention
        elif type(channel) == int and channel == 9223372036854775800:
            birthday_feed = channel
            channel_log = 'none'
        else:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await rest_api.set_param(
            self.bot, 
            server_id=ctx.guild.id,
            birthday_feed_channel_id=birthday_feed
        )
        await utils.log(
            ctx,
            target='General server settings',
            channel=self.bot.settings.get(
                str(ctx.guild.id), 
                {}
            ).get('warnings_log_channel_id'),
            title='Settings changed',
            details=f'Birthday feed channel set to {channel_log}',
        )"""


def setup(bot):
    bot.add_cog(SetGeneral(bot))