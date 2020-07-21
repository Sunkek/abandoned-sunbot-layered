"""This cog sends custom emoji usage to the database."""

import discord
from discord.ext import commands
from datetime import datetime

import re

from utils import rest_api

class TrackEmotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # I don't want to save info about DMs and webhooks
        if message.guild and message.guild.get_member(message.author.id):
            if self.bot.settings.get(message.guild.id, {}).get("track_emotes"):
                emoji = re.findall("<:[\w+]:[\d+]>", message.content)
                print(message.content)
                print(emoji)
                if emoji:
                    """await rest_api.add_emotes(
                        self.bot, 
                        guild_id=message.guild.id,
                        channel_id=message.channel.id,
                        user_id=message.author.id,
                        postcount=1,
                        attachments=len(message.attachments),
                        words=len(message.content.split()),
                        period=datetime.now().strftime("%Y-%m-%d")
                    )"""
        

def setup(bot):
    bot.add_cog(TrackEmotes(bot))