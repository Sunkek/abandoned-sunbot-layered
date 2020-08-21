"""This cog automatically manages the ranks on the server"""

import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
from asyncio import sleep

from utils import rest_api, helpers


class Actualzier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_update_ranks.start()

    def cog_unload(self):
        self.auto_update_ranks.cancel()

    def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @tasks.loop(hours=24)
    async def auto_update_ranks(self):
        """Triggers on the 1st of every month. Reads last month's 
        activity and promotes/demotes people accordingly"""
        if datetime.now.day != 1:
            return
        for guild in self.bot.settings.keys():
            guild = self.bot.get_guild(guild)
            basic = self.bot.settings[guild.id].get("rank_basic_member_role_id")
            basic = guild.get_role(basic)
            active = self.bot.settings[guild.id].get("rank_active_member_role_id")
            active = guild.get_role(active)
            active_activity = self.bot.settings[guild.id].get("rank_active_member_required_activity")
            active_days = self.bot.settings[guild.id].get("rank_active_member_required_days", 0)
            active_days = datetime.now() - timedelta(days=active_days)
            junior = self.bot.settings[guild.id].get("rank_mod_junior_role_id")
            junior = guild.get_role(junior)
            senior = self.bot.settings[guild.id].get("rank_mod_senior_role_id")
            senior = guild.get_role(senior)
            admin = self.bot.settings[guild.id].get("rank_mod_admin_role_id")
            admin = guild.get_role(admin)
            # Active member role
            if (active and active_activity) or (active and active_days):
                eligible_members = await rest_api.get_active_members(self.bot, guild.id)
                if not eligible_members:
                    continue
                for member in guild.members:
                    if all((  # Basic to Active
                        active not in member.roles,
                        junior not in member.roles,
                        senior not in member.roles,
                        admin not in member.roles,
                        member.id in eligible_members,
                        member.joined_at < active_days
                    )):
                        await member.add_roles(active)
                    elif all((  # Active to Basic
                        active in member.roles,
                        basic not in member.roles,
                        junior not in member.roles,
                        senior not in member.roles,
                        admin not in member.roles,
                        member.id not in eligible_members
                    )):
                        await member.add_roles(basic)
                        await member.remove_roles(active)

    @auto_update_ranks.before_loop
    async def before_auto_update_ranks(self):
        """Sleeping until the full day"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())


def setup(bot):
    bot.add_cog(Actualzier(bot))