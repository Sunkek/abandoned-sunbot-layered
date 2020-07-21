"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional

from utils import rest_api, utils

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
        desc = '\n'.join([
            f'{utils.format_settings_key(key)}: {utils.format_settings_value(ctx.guild, value)}' 
            for key, value in settings.items()
            if value
        ])
        embed = discord.Embed(
            title=f"Current settings for {ctx.guild.name}",
            color=ctx.author.color,
            description=desc or "No custom settings yet!"
        )
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
        name="settrackmessages", 
        aliases=["stm"],
        description="Sets message tracking on or off.",
    )
    async def settrackmessages(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_messages", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_messages=value,
        )

    @commands.command(
        name="settrackreactions", 
        aliases=["str"],
        description="Sets reaction tracking on or off.",
    )
    async def settrackreactions(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_reactions", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_reactions=value,
        )
        
    @commands.command(
        name="settrackgames", 
        aliases=["stg"],
        description="Sets game tracking on or off.",
    )
    async def settrackgames(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_games", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_games=value,
        )
        
    @commands.command(
        name="settrackvoice", 
        aliases=["stv"],
        description="Sets voice tracking on or off.",
    )
    async def settrackvoice(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_voice", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_voice=value,
        )
        
    @commands.command(
        name="settracemotes", 
        aliases=["ste"],
        description="Sets custom emote tracking on or off.",
    )
    async def settracemotes(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_emotes", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_emotes=value,
        )
        

def setup(bot):
    bot.add_cog(SetGeneral(bot))