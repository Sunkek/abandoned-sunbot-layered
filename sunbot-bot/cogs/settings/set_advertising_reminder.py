"""Setting util for advertising reminder system"""

import discord
from discord.ext import commands, tasks
from typing import Optional, Union
from datetime import datetime, timedelta
from asyncio import sleep

from utils import helpers, rest_api

AD_PLATFORMS = [
    "disboard", "disforge", "discordme", "discordservers"
]

class SetAdReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ad_reminder.start()

    def cog_unload(self):
        self.ad_reminder.cancel()

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="setadreminderchannel", 
        aliases=["setadchannel", "sarch"],
        description="Sets up the specified channel as advertising reminder feed. To reset, provide no channel.",
    )
    async def setadreminderchannel(self, ctx, channel: discord.TextChannel=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            ad_reminder_channel_id=channel.id if channel else None,
        )
              
    @commands.command(
        name="setadreminderrole", 
        aliases=["setadrole", "sarr"],
        description="Sets up the role to ping on each remind",
    )
    async def setadreminderrole(self, ctx, role: discord.Role=None):
        # Build and send the JSON to the server part of the bot
        await rest_api.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            ad_reminder_role_id=role.id if role else None,
        )
       
    @commands.command(
        name="adremind", 
        alises=["ar"],
        description=f"Starts or stops reminding to bump/post on the supported advertising platforms. They currently include: `{', '.join(AD_PLATFORMS)}``",
    )
    async def adremind(self, ctx, target):
        target = target.lower()
        if target not in AD_PLATFORMS:
            raise commands.BadArgument
        # Disboard
        if target == "disboard":
            value = not self.bot.settings.get(ctx.guild.id, {}).get("ad_reminder_disboard", False)
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_disboard=value,
            )     
        # Disforge
        elif target == "disforge":            
            value = not self.bot.settings.get(ctx.guild.id, {}).get("ad_reminder_disforge", False)
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_disforge=value,
            )     
        # Discord.me
        elif target == "discordme":            
            value = not self.bot.settings.get(ctx.guild.id, {}).get("ad_reminder_discordme", False)
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_discordme=value,
            )     
        # Discord.me
        elif target == "discordservers":            
            value = not self.bot.settings.get(ctx.guild.id, {}).get("ad_reminder_discordservers", False)
            await rest_api.set_guild_param(
                self.bot, 
                guild_id=ctx.guild.id,
                ad_reminder_discordservers=value,
            )    
        
    @tasks.loop(hours=1.0)
    async def ad_reminder(self):
        """Remind server admins to advertise when it's allowed"""
        try:
            for guild, settings in self.bot.settings.items():
                if settings["ad_reminder_channel_id"]:
                    guild = self.bot.get_guild(int(guild))
                    embed = discord.Embed(
                        title="Advertising Reminder",
                        color=guild.me.color
                    )
                    # Disboard - every 2 hours
                    if settings["ad_reminder_disboard"] and datetime.now().hour % 2 == 0:
                        embed.add_field(
                            name='Disboard',
                            value=f'`every 2 hours`\nBump at [WEBSITE](https://disboard.org/server/{guild.id}) \nor with <@302050872383242240>:\n`!d bump`'
                        )
                    # Disforge - every 3 hours
                    if settings["ad_reminder_disforge"] and datetime.now().hour % 3 == 0:
                        embed.add_field(
                            name='Disforge',
                            value=f'`every 3 hours`\nBump at [WEBSITE](https://disforge.com/dashboard)'
                        )
                    # Discord.me
                    if settings["ad_reminder_discordme"] and datetime.now().hour % 6 == 0:
                        embed.add_field(
                            name='Discord.me',
                            value=f'`every 6 hours`\nBump at [WEBSITE](https://discord.me/dashboard)'
                        )
                    # discordservers
                    if settings["ad_reminder_discordservers"] and datetime.now().hour % 12 == 0:
                        embed.add_field(
                            name="discordservers",
                            value=f'`every 12 hours`\nBump at [WEBSITE](https://discordservers.com/panel/{guild.id}/bump)'
                        )

                    if embed.fields:
                        role = guild.get_role(int(settings["ad_reminder_role_id"]))
                        await guild.get_channel(
                            int(settings["ad_reminder_channel_id"])
                        ).send(content=role.mention if role else None, embed=embed)
        except Exception as e:
            print(e)

    '''@ad_reminder.before_loop
    async def before_ad_reminder(self):
        """Sleeping until the full hour"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        await sleep((next_hour - now).total_seconds())'''

def setup(bot):
    bot.add_cog(SetAdReminder(bot))
