"""This cog stores voice chat activity to the database and does various
activity statistics tracking."""

import discord
from discord.ext import commands, tasks
from datetime import datetime

from utils import rest_api

class TrackVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_check.start()

    def cog_unload(self):
        self.voice_check.cancel()

    @tasks.loop(seconds=60) # Points are given every minute
    async def voice_check(self):
        for guild in self.bot.guilds:
            if self.bot.settings.get(guild.id, {}).get("track_voice"):
                for channel in guild.voice_channels:
                    if channel.members:
                        for member in channel.members:
                            if not member.bot:
                                await rest_api.add_voice(
                                    self.bot, 
                                    guild_id=guild.id,
                                    channel_id=channel.id,
                                    user_id=member.id,
                                    members=len(channel.members),
                                    duration=60,
                                    period=datetime.now().strftime("%Y-%m-%d")
                                )

def setup(bot):
    bot.add_cog(TrackVoice(bot))