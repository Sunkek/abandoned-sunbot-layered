"""This cog automatically manages the ranks on the server"""

import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
from asyncio import sleep

from utils import rest_api, helpers


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_vote.start()

    def cog_unload(self):
        self.auto_vote.cancel()

    def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @tasks.loop(hours=24)
    async def auto_vote(self):
        """1st of the vote month: vote begins. 
        People click on reaction and receive the ballots.
        6th of the same month: vote ends.
        The votes are counted and members get promoted/demoted."""
        now = datetime.now()
        if now.day == 1:
            for guild in self.bot.settings.keys():
                guild = self.bot.get_guild(guild)
                vote_channel = self.bot.settings[guild].get("rank_vote_channel_id")
                vote_channel = guild.get_channel(vote_channel)
                if not vote_channel:
                    continue

                junior_vote_months = self.bot.settings[guild.id].get("rank_mod_junior_vote_months")
                senior_vote_months = self.bot.settings[guild.id].get("rank_mod_senior_vote_months")
                admin_vote_months = self.bot.settings[guild.id].get("rank_mod_admin_vote_months")
                if now.month not in \
                    junior_vote_months + senior_vote_months + admin_vote_months:
                    continue
                
                junior = self.bot.settings[guild.id].get("rank_mod_junior_role_id")
                junior = guild.get_role(junior)
                junior_limit = self.bot.settings[guild.id].get("rank_mod_junior_limit")
                junior_activity = self.bot.settings[guild.id].get("rank_mod_junior_required_activity")
                junior_days = self.bot.settings[guild.id].get("rank_mod_junior_required_days", 0)
                junior_days = datetime.now() - timedelta(days=junior_days)

                senior = self.bot.settings[guild.id].get("rank_mod_senior_role_id")
                senior = guild.get_role(senior)
                senior_activity = self.bot.settings[guild.id].get("rank_mod_senior_required_activity")
                senior_days = self.bot.settings[guild.id].get("rank_mod_senior_required_days", 0)
                senior_days = datetime.now() - timedelta(days=senior_days)

                admin = self.bot.settings[guild.id].get("rank_mod_admin_role_id")
                admin = guild.get_role(admin)
                admin_activity = self.bot.settings[guild.id].get("rank_mod_admin_required_activity")
                admin_days = self.bot.settings[guild.id].get("rank_mod_admin_required_days", 0)
                admin_days = datetime.now() - timedelta(days=admin_days)

                # Junior vote
                if now.month in junior_vote_months:
                    # Make a list of candidates
                    eligible_members = await rest_api.get_junior_mods(self.bot, guild.id)    
                    if not eligible_members:
                        continue
                    candidates = []
                    for member in guild.members:
                        if all((
                            senior not in member.roles,
                            admin not in member.roles,
                            member.id in eligible_members,
                            member.joined_at < junior_days
                        )):  
                            candidates.append(member.mention)
                    if not candidates:
                        continue                    

                    embed = discord.Embed(
                        title=f"{junior.name} vote {now.month}/{now.year} open",
                        color=guild.me.color
                    )
                    embed.description = (
                        f"The vote happens on these months: {', '.join(junior_vote_months)}\n"
                        "It's anonymous. React to this message with ☑️ to receive your voting ballot in DM (make sure DMs are open).\n"
                        f"Candidates must earn {junior_activity} activity points and be on the server for at least {junior_days} days.\n"
                        f"To get promoted, a candidate must upvote themself in the ballot and get the support of at least 1/3 of the voters.\n"
                        f"Max number of {junior_limit} candidates will be picked from this vote."
                    )
                message = await vote_channel.send(embed=embed)
                await message.add_reaction("☑️")
                

    @auto_vote.before_loop
    async def before_auto_vote(self):
        """Sleeping until the full day"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())


def setup(bot):
    bot.add_cog(Vote(bot))