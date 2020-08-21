"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional

from utils import rest_api, helpers


class SetRanks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
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
            rank_mute_role_id=role.id if role else None,
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
            rank_basic_member_role_id=role.id if role else None,
        )

    @commands.command(
        name="setactivememberrole", 
        aliases=["samr",],
        description="Sets up the active member role. This role is assigned to those who have enough activity points and were on the server long enough.",
    )
    async def setactivememberrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_role_id=role.id if role else None,
        )

    @commands.command(
        name="setactivememberroledays", 
        aliases=["samrd",],
        description="Sets up the amount of days a member must be on your server to have the active member role.",
    )
    async def setactivememberroledays(self, ctx, amount: int=0):
        if amount > 10000 or amount < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_required_days=amount,
        )
        
    @commands.command(
        name="setactivememberroleactivity", 
        aliases=["samra",],
        description="Sets up the amount of activity a member must get in the previous or current month to have the active member role.",
    )
    async def setactivememberroleactivity(self, ctx, amount: int=0):
        if amount > 1000000 or amount < 0:
            raise commands.BadArgument
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            rank_active_member_required_activity=amount,
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
            rank_mod_junior_role_id=role.id if role else None,
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
            rank_mod_senior_role_id=role.id if role else None,
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
            rank_mod_admin_role_id=role.id if role else None,
        )
                

def setup(bot):
    bot.add_cog(SetRanks(bot))