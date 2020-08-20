import discord
from discord.ext import commands, tasks

from utils import helpers


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends the initial welcome message"""
        channel = self.bot.settings.get(member.guild.id, {}).get("welcome_channel")
        text = self.bot.settings.get(member.guild.id, {}).get("welcome_message")
        embed = self.bot.settings.get(member.guild.id, {}).get("welcome_message_embed")
        if channel and (text or embed):
            channel = member.guild.get_channel(channel)
            text = helpers.format_message(text, guild=member.guild, user=member)
            embed = discord.Embed.from_dict(
                helpers.format_message(embed, guild=member.guild, user=member)
            )
            await channel.send(content=text or None, embed=embed or None)
    
def setup(bot):
    bot.add_cog(Welcome(bot))