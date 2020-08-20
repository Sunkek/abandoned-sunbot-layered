"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional

from utils import rest_api, helpers

class SetTrackers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
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
        name="settrackemotes", 
        aliases=["ste"],
        description="Sets custom emote tracking on or off.",
    )
    async def settrackemotes(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_emotes", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_emotes=value,
        )
        
    @commands.command(
        name="settracknwords", 
        aliases=["stn"],
        description="Sets N-words tracking on or off.",
    )
    async def settracknwords(self, ctx):
        value = not self.bot.settings.get(ctx.guild.id, {}).get("track_nwords", False)
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            track_nwords=value,
        )
        

def setup(bot):
    bot.add_cog(SetTrackers(bot))