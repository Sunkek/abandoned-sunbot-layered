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
            settings, ctx, include=["activity"], ignore=[]
        )
        trackers = helpers.format_settings(
            settings, ctx, include=["track"], ignore=[]
        )
        ad_reminder = helpers.format_settings(
            settings, ctx, include=["ad_reminder"], ignore=[]
        )
        verification = helpers.format_settings(
            settings, ctx, include=["verification"], ignore=[]
        )
        welcome = helpers.format_settings(
            settings, ctx, include=["welcome", "leave"], ignore=[]
        )
        desc = helpers.format_settings(
            settings, ctx, include=[], ignore=[
                "track", "activity", "ad_reminder", "verification", "welcome", 
                "leave",
            ],
        )
        embed = discord.Embed(
            title=f"Current settings for {ctx.guild.name}",
            color=ctx.author.color,
            description=desc or "No custom settings yet!"
        )
        if activity: embed.add_field(name="Activity", value=activity)
        if trackers: embed.add_field(name="Trackers", value=trackers)
        if ad_reminder: embed.add_field(name="Ad Reminder", value=ad_reminder)
        if verification: embed.add_field(name="Verification", value=verification)
        if welcome: embed.add_field(name="Welcome/Leave", value=verification)
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
        name="setmuterole", 
        aliases=["smr",],
        description="Sets up the mute role. This role is assigned with multiple ways - command, warnings (not implemented yet!)",
    )
    async def setmuterole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            mute_role_id=role.id if role else None,
        )

    @commands.command(
        name="setbasicmemberrole", 
        aliases=["sbmr",],
        description="Sets up the basic member role. This role is assigned to those who pass the verification.",
    )
    async def setbasicmemberrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            basic_member_role_id=role.id if role else None,
        )
        
    @commands.command(
        name="setjuniormodrole", 
        aliases=["sjmr",],
        description="Sets up the junior moderator role. This role is assigned with multiple ways - command, vote (not implemented yet!)",
    )
    async def setjuniormodrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            mod_junior_role_id=role.id if role else None,
        )
        
    @commands.command(
        name="setseniormodrole", 
        aliases=["ssmr",],
        description="Sets up the senior moderator role. This role is assigned with multiple ways - command, vote (not implemented yet!)",
    )
    async def setseniormodrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            mod_senior_role_id=role.id if role else None,
        )
        
    @commands.command(
        name="setadminrole", 
        aliases=["sar",],
        description="Sets up the administrator role. This role is assigned with multiple ways - command, vote (not implemented yet!)",
    )
    async def setadminrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            mod_admin_role_id=role.id if role else None,
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