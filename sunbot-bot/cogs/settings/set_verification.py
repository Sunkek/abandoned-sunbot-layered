"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional
from emoji import UNICODE_EMOJI

from utils import rest_api, helpers

class SetVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
               
    @commands.command(
        name="setverificationmessage", 
        aliases=["svm"],
        description="Sets the verification message to the provided ID. It will check the reactions under that message. Provide no ID to reset.",
    )
    async def setverificationmessage(
        self, ctx, message_id:Optional[int]=None
    ):
        # Build and send the JSON to backend
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            verification_message_id=message_id
        )
        
    @commands.command(
        name="setverificationemote", 
        aliases=["sve"],
        description="Sets the verification emote. Members have to react with this emote to the verification message to get verified. Provide no emote to reset.",
    )
    async def setverificationemote(
        self, ctx, emote:Optional[str]=None
    ):
        if emote in UNICODE_EMOJI:  # Strip skintones
            emote = str(bytes(emote, "utf-8")[:4], "utf-8")
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                verification_emote=emote
            )
        if not emote or emote in [str(e) for e in ctx.guild.emojis]:
            # Build and send the JSON to backend
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                verification_emote=emote
            )
        else:
            raise commands.BadArgument()
         
    @commands.command(
        name="setunverifiedrole", 
        aliases=["sur",],
        description="Sets up the unverified role. This role is assigned to everyone who joins the server. It's also removed when they react with the verification reaction to the verification message.",
    )
    async def setunverifiedrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            verification_unverified_role_id=role.id if role else None,
        )
        
    @commands.command(
        name="setverifiedrole", 
        aliases=["svr",],
        description="Sets up the verified role. This role is assigned to those who react with the verification reaction to the verification message.",
    )
    async def setverifiedrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            verification_verified_role_id=role.id if role else None,
        )
        
def setup(bot):
    bot.add_cog(SetVerification(bot))