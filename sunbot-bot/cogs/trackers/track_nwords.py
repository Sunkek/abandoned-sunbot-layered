"""This cog stores messages to the database and does various
activity statistics tracking. Mostly made for APoC."""

import discord
from discord.ext import commands
from datetime import datetime

from utils import rest_api

class TrackNwords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # I don't want to save info about DMs and webhooks
        if message.guild and message.guild.get_member(message.author.id) and \
            not message.author.bot:
            
            if self.bot.settings.get(message.guild.id, {}).get("track_nwords"):
                nigger = message.content.lower().count("nigger")
                nigga = message.content.lower().count("nigga")
                if nigger or nigga:
                    await rest_api.add_nwords(
                        self.bot, 
                        guild_id=message.guild.id,
                        user_id=message.author.id,
                        nigger=nigger,
                        nigga=nigga,
                        period=datetime.now().strftime("%Y-%m-%d")
                    )
        

def setup(bot):
    bot.add_cog(TrackNwords(bot))