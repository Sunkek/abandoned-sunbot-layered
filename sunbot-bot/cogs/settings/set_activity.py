"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Union

from utils import rest_api, helpers

class SetActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
               
    @commands.command(
        name="setactivitypermessage", 
        aliases=["sapm"],
        description="Sets the amout of activity points members get for each message. Max APM is `100`",
    )
    async def setactivitypermessage(self, ctx, amount: int=0):
        if amount > 100 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_message=amount,
        )
               
    @commands.command(
        name="setactivityminmessagewords", 
        aliases=["sammw"],
        description="Sets the minimum amount of words required for a message to reward activity points. Max `20`",
    )
    async def setactivityminmessagewords(self, ctx, amount: int=0):
        if amount > 20 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_min_message_words=amount,
        )

    @commands.command(
        name="setactivitymultiplierperword", 
        aliases=["sampw"],
        description="Each message activity points will be multiplied for this value as many times as there are words in the message. Min `1`, max `5`",
    )
    async def setactivitymultiplierperword(self, ctx, amount: int=1):
        if amount > 5 or amount < 1:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_multi_per_word=amount,
        )

    @commands.command(
        name="setactivityperattachment", 
        aliases=["sapa"],
        description="Sets the amount of activity points rewarded for sent attachments. Max `200`",
    )
    async def setactivityperattachment(self, ctx, amount: int=0):
        if amount > 200 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_attachment=amount,
        )

    @commands.command(
        name="setactivitycooldown", 
        aliases=["sacd"],
        description="Sets the amount of seconds that must pass between activity point rewards for each member. Max `3600` (1 hour)",
    )
    async def setactivitycooldown(self, ctx, amount: int=0):
        if amount > 3600 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_cooldown=amount,
        )

    @commands.command(
        name="setactivityperreaction", 
        aliases=["sapr"],
        description="Sets the amount of activity points rewarded for given reactions. Max `100`",
    )
    async def setactivityperreaction(self, ctx, amount: int=0):
        if amount > 100 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_reaction=amount,
        )

    @commands.command(
        name="setactivitypervoiceminute", 
        aliases=["sapvm"],
        description="Sets the amount of activity points rewarded for a minute in voice chat. Loners in voice don't get points. Max `100`",
    )
    async def setactivitypervoiceminute(self, ctx, amount: int=0):
        if amount > 100 or amount < 0:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_per_voice_minute=amount,
        )

    @commands.command(
        name="setactivitymultiplierpervoicemember", 
        aliases=["sampvm"],
        description="Each voice activity points will be multiplied for this value as many times as there are members in chat. Min `1`, max `5`",
    )
    async def setactivitymultiplierpervoicemember(self, ctx, amount: int=1):
        if amount > 5 or amount < 1:
            raise commands.BadArgument
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            activity_multi_per_voice_member=amount,
        )
        
    @commands.command(
        name="setactivitychannelx0", 
        aliases=["sac0"],
        description="Add or remove the selected channel(s) to/from the list of channels which reward no activity points",
    )
    async def setactivitychannelx0(self, ctx, channels:Union[discord.TextChannel, int]):
        targets = [ch.id for ch in channels]            
        await rest_api.set_guild_param_list(
            self.bot, 
            guild_id=ctx.guild.id,
            setting="activity_channels_x0",
            targets=targets,
        )

    """activity_channels_x0 = ArrayField(models.BigIntegerField(null=True, blank=True))
    activity_channels_x05 = ArrayField(models.BigIntegerField(null=True, blank=True))
    activity_channels_x2 = ArrayField(models.BigIntegerField(null=True, blank=True))"""

def setup(bot):
    bot.add_cog(SetActivity(bot))