"""This cog stores voice chat activity to the database and does various
activity statistics tracking.

Maybe I should just send this info to the backend part 
and handle the logic there?"""

import discord
from discord.ext import commands, tasks
from datetime import datetime

from utils import rest_api

class TrackGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}
        self.ignore = ("scrivener", "youtube", "spotify", "foobar2000")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Activity changed, not bot
        if all((
            before.activities != after.activities,
            not after.bot,
            self.bot.settings.get(after.guild.id, {}).get("track_games")
        )):
            before_game = None
            after_game = None
            # Getting the game before the member changed his activity
            for activity in before.activities:
                if all((
                    activity.type == discord.ActivityType.playing,
                    hasattr(activity, "application_id")
                )):
                    before_game = activity
                    break
            # Getting the game after the member changed his activity
            for activity in after.activities:
                if all((
                    activity.type == discord.ActivityType.playing,
                    hasattr(activity, "application_id")
                )):
                    after_game = activity
                    break
            # If started playing
            if after_game and not before_game:
                if after_game.name.lower() not in self.ignore:
                    self.sessions[before.id] = (
                        after_game.name, 
                        datetime.utcnow()
                    )
            # If done playing
            elif not after_game and before_game:
                game = self.sessions.pop(after.id, (None,))
                if before_game.name == game[0]:
                    played = int((datetime.utcnow()-game[1]).total_seconds())
                    if played > 0:
                        await rest_api.add_game(
                            self.bot, 
                            member_id=before.id,
                            game=game[0],
                            duration=played,
                            period=datetime.now().strftime('%Y-%m-%d')
                        )

def setup(bot):
    bot.add_cog(TrackGames(bot))
