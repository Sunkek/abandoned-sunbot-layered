"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional

from utils import rest_api, helpers


class SetGeneral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="showsettings", 
        aliases=['settings', 'checksettings', 'ss'],
        description="Shows current settings for this server.",
    )
    async def showsettings(self, ctx):

        settings = self.bot.settings.get(ctx.guild.id, {})
        activity = helpers.format_settings(
            settings, ctx, include=["activity_"], ignore=[]
        )
        print(activity)
        ranks = helpers.format_settings(
            settings, ctx, include=["rank_"], ignore=[]
        )
        print(ranks)
        trackers = helpers.format_settings(
            settings, ctx, include=["track_"], ignore=[]
        )
        print(trackers)
        ad_reminder = helpers.format_settings(
            settings, ctx, include=["ad_reminder_"], ignore=[]
        )
        print(ad_reminder)
        verification = helpers.format_settings(
            settings, ctx, include=["verification_"], ignore=[]
        )
        print(verification)
        welcome = helpers.format_settings(
            settings, ctx, include=["welcome_", "leave_"], ignore=[]
        )
        print(welcome)
        desc = helpers.format_settings(
            settings, ctx, include=[], ignore=[
                "track_", "activity_", "ad_reminder_", "verification_", "welcome_", 
                "leave_", "rank_"
            ],
        )
        print(desc)
        embed = discord.Embed(
            title=f"Current settings for {ctx.guild.name}",
            color=ctx.author.color,
            description=desc or "No custom settings yet!"
        )
        if activity: embed.add_field(name="Activity", value=activity)
        if ranks: embed.add_field(name="Ranks", value=ranks)
        if trackers: embed.add_field(name="Trackers", value=trackers)
        if ad_reminder: embed.add_field(name="Ad Reminder", value=ad_reminder)
        if verification: embed.add_field(name="Verification", value=verification)
        if welcome: embed.add_field(name="Welcome/Leave", value=welcome)
        await ctx.send(embed=embed)
       
    @commands.command(
        name="setbirthdayfeed", 
        aliases=["sbdf"],
        description="Sets up the specified channel as birthday feed. To reset, provide no channel.",
    )
    async def setbirthdayfeed(
        self, 
        ctx, 
        channel:Optional[discord.TextChannel]=None
    ):
        # Check if there's a channel specified
        if channel: birthday_feed = channel.id
        else: birthday_feed = channel
        # Build and send the JSON to backend
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            birthday_feed_channel_id=birthday_feed
        )
        
    @commands.command(
        name="setwelcomechannel", 
        aliases=["swc"],
        description="Sets up the channel where welcome, verification and leave messages will be sent.",
    )
    async def setwelcomechannel(
        self, 
        ctx, 
        channel:Optional[discord.TextChannel]=None
    ):
        # Build and send the JSON to backend
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_channel_id=channel.id if channel else channel
        )

    @commands.command(
        name="setwelcomemessage", 
        aliases=["swm"],
        description=f"Sets up the welcome message which is sent when a new member joins the server. Available placeholders:\n{helpers.PLACEHOLDERS}",
    )
    async def setwelcomemessage(self, ctx, text=None):
        # Build and send the JSON to backend
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_message=text
        )
        
    @commands.command(
        name="setwelcomeembed", 
        aliases=["swe"],
        description=f"Sets up the welcome embed which is sent when a new member joins the server. You should build a dummy embed with `Embedder` and then copy it with this command. Available placeholders:\n{helpers.PLACEHOLDERS}",
    )
    async def setwelcomeembed(
        self, ctx,
        channel: Optional[discord.TextChannel]=None, 
        message_id: Optional[int]=0
    ):
        channel = channel or ctx.channel
        message = await channel.fetch_message(message_id)
        if message.embeds:
            embed = message.embeds[0].to_dict()
        # Build and send the JSON to backend
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_message_embed=embed
        )
                

def setup(bot):
    bot.add_cog(SetGeneral(bot))