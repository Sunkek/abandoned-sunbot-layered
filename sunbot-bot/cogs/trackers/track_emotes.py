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
                emoji_pattern = "<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>"
                emoji = set(re.findall(emoji_pattern, message.content, re.M))
                for e in emoji:
                    print(e)
                    e = e.groupdict()['id']
                    print(e)
                    await rest_api.add_emotes(
                        self.bot, 
                        guild_id=message.guild.id,
                        user_id=message.author.id,
                        emote=f"<:_:{e}>",
                        period=datetime.now().strftime("%Y-%m-%d"),
                        count=1,
                    )
        

def setup(bot):
    bot.add_cog(TrackEmotes(bot))