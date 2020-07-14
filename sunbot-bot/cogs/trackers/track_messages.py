"""This cog stores messages to the database and does various
activity statistics tracking. Mostly made for APoC."""

import discord
from discord.ext import commands
from datetime import datetime

from utils import rest_api

class TrackMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # I don't want to save info about DMs, also no webhooks
        if message.guild and message.guild.get_member(message.author.id):
            await rest_api.add_message(
                self.bot, 
                guild_id=message.guild.id,
                channel_id=message.channel.id,
                user_id=message.author.id,
                postcount=1,
                attachments=len(message.attachments),
                words=len(message.content.split()),
                period=datetime.now().strftime("%Y-%m-%d")
            )
        

def setup(bot):
    bot.add_cog(TrackMessages(bot))