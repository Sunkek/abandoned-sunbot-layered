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

    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload):
        now = datetime.now()
        # If it's the vote period
        guild = self.bot.get_guild(payload.guild_id)
        junior_vote_months = self.bot.settings[guild.id].get("rank_mod_junior_vote_months", list())
        senior_vote_months = self.bot.settings[guild.id].get("rank_mod_senior_vote_months", list())
        admin_vote_months = self.bot.settings[guild.id].get("rank_mod_admin_vote_months", list())
        if now.day < 5 and now.month not in \
            junior_vote_months + senior_vote_months + admin_vote_months:  # now.day > 5
            return
        # If the reaction is ballot and not bot's
        if str(payload.emoji) != "☑️" or payload.user_id == self.bot.user.id:
            return
        # If it's the vote message
        vote_channel = self.bot.settings[guild.id].get("rank_vote_channel_id")
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if channel.id != vote_channel and message.author != self.bot.user and \
            not message.embeds:
            return
        # Now fetch the candidates from the mesage
        vote_emebed = message.embeds[0]
        candidates = vote_emebed.fields[0].value.split("\n")
        print(candidates)
        desc_embed = discord.Embed(
            title=vote_emebed.title[:-5],
            color=guild.me.color
        )
        desc_embed.description = "React to the messages below with candidate numbers to vote for them. **Important** - If you're among the candidates, but don't want the promotion - don't upvote yourself. If the embed misses reactions, rereact to the initial vote message on server."
        embeds = []
        for i in range(len(candidates)/20):
            embed = discord.Embed(
                title="Cadidates",
                description="\n".join(candidates[i*20:(i+1)*20])
            )
            embeds.append(embed)
            print(embed.description)
        # Sending embeds and adding reaactions to them
        user = await self.bot.fetch_user(payload.user_id)
        for embed in embeds:
            await user.send(embed=embed)
            

        

        
        

    @tasks.loop(hours=24)
    async def auto_vote(self):
        """1st of the vote month: vote begins. 
        People click on reaction and receive the ballots.
        6th of the same month: vote ends.
        The votes are counted and members get promoted/demoted."""
        try:
            now = datetime.now()
            if now.day:  # if now.day == 1:
                for guild, settings in self.bot.settings.items():
                    guild = self.bot.get_guild(guild)
                    vote_channel = settings.get("rank_vote_channel_id")
                    vote_channel = guild.get_channel(vote_channel)
                    if not vote_channel:
                        continue

                    junior_vote_months = settings.get("rank_mod_junior_vote_months", list()) or list()
                    senior_vote_months = settings.get("rank_mod_senior_vote_months", list()) or list()
                    admin_vote_months = settings.get("rank_mod_admin_vote_months", list()) or list()
                    if now.month not in \
                        junior_vote_months + senior_vote_months + admin_vote_months:
                        continue
                    
                    junior = settings.get("rank_mod_junior_role_id")
                    junior = guild.get_role(junior)
                    junior_limit = self.bot.settings[guild.id].get("rank_mod_junior_limit")
                    junior_activity = self.bot.settings[guild.id].get("rank_mod_junior_required_activity")
                    junior_days = self.bot.settings[guild.id].get("rank_mod_junior_required_days", 0) or 0
                    junior_join = datetime.now() - timedelta(days=junior_days)

                    senior = self.bot.settings[guild.id].get("rank_mod_senior_role_id")
                    senior = guild.get_role(senior)
                    senior_activity = self.bot.settings[guild.id].get("rank_mod_senior_required_activity")
                    senior_days = self.bot.settings[guild.id].get("rank_mod_senior_required_days", 0) or 0
                    senior_days = datetime.now() - timedelta(days=senior_days)

                    admin = self.bot.settings[guild.id].get("rank_mod_admin_role_id")
                    admin = guild.get_role(admin)
                    admin_activity = self.bot.settings[guild.id].get("rank_mod_admin_required_activity")
                    admin_days = self.bot.settings[guild.id].get("rank_mod_admin_required_days", 0) or 0
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
                                member.joined_at < junior_join
                            )):  
                                candidates.append(member.mention)
                        if not candidates:
                            continue
                        date = now.strftime("%m/%y")
                        embed = discord.Embed(
                            title=f"{junior.name} vote {date} open",
                            color=guild.me.color
                        )
                        embed.description = (
                            f"- The vote happens on {', '.join(helpers.MONTHS[i-1] for i in sorted(junior_vote_months))}\n"
                            "- It's anonymous. React to this message with ☑️ to receive your voting ballot in DM (make sure DMs are open).\n"
                            f"- Candidates must earn {junior_activity} activity points and be on the server for at least {junior_days} days.\n"
                            f"- To get promoted, a candidate must upvote themself in the ballot and get the support of at least 1/3 of the voters."
                        )
                        if junior_limit:
                            embed.description += f"\n- Max number of {junior_limit} candidates will be picked from this vote."
                        embed.add_field(name="Candidates", value="\n".join(candidates))
                    message = await vote_channel.send(embed=embed)
                    await message.add_reaction("☑️")
        except Exception as e:
            print(e)
                

    '''@auto_vote.before_loop
    async def before_auto_vote(self):
        """Sleeping until the full day"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())'''


def setup(bot):
    bot.add_cog(Vote(bot))