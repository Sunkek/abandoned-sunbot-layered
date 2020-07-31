"""This cog stores reactions to the database and does various
activity statistics tracking."""

import discord
from discord.ext import commands
from datetime import datetime
from emoji import UNICODE_EMOJI

from utils import rest_api

class TrackReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignore_emoji = ["⏮️", "⏪", "⏩", "⏭️"]
        
    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload):
        # I don't want to save info about DMs with the bot
        if payload.guild_id:
            if self.bot.settings.get(payload.guild_id, {}).get("track_reactions"):
                guild = self.bot.get_guild(payload.guild_id)
                channel = guild.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                # Not the topchart scrollers please
                if message.embeds and str(payload.emoji) in self.ignore_emoji:
                    return
                giver = guild.get_member(payload.user_id)
                receiver = message.author
                if giver.bot or giver == receiver: 
                    return
                if str(payload.emoji) in UNICODE_EMOJI:
                    # Stripping skintones and other modifiers
                    emoji = str(bytes(str(payload.emoji), "utf-8")[:4], "utf-8")[0]
                else: 
                    # Just turn it into string
                    emoji = str(payload.emoji).split(":")
                    emoji = f"{emoji[0]}:_:{emoji[2]}"

                await rest_api.add_reaction(
                    self.bot, 
                    guild_id=guild.id,
                    giver_id=giver.id,
                    receiver_id=receiver.id,
                    emote=emoji,
                    count=1,
                    period=datetime.now().strftime("%Y-%m-%d")
                )

    @commands.Cog.listener() 
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id:
            if self.bot.settings.get(payload.guild_id, {}).get("track_reactions"):
                guild = self.bot.get_guild(payload.guild_id)
                channel = guild.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                # Not the topchart scrollers please
                if message.embeds and str(payload.emoji) in self.ignore_emoji:
                    return
                giver = guild.get_member(payload.user_id)
                receiver = message.author
                if giver.bot or giver == receiver: 
                    return
                if str(payload.emoji) in UNICODE_EMOJI:
                    # Stripping skintones and other modifiers
                    emoji = str(bytes(str(payload.emoji), "utf-8")[:4], "utf-8")[0]
                else: 
                    # Just turn it into string
                    emoji = str(payload.emoji).split(":")
                    emoji = f"{emoji[0]}:_:{emoji[2]}"
                await rest_api.add_reaction(
                    self.bot, 
                    guild_id=guild.id,
                    giver_id=giver.id,
                    receiver_id=receiver.id,
                    emote=emoji,
                    count=-1,
                    period=datetime.now().strftime("%Y-%m-%d")
                )

def setup(bot):
    bot.add_cog(TrackReactions(bot))