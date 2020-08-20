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
        try:
            channel = self.bot.settings.get(member.guild.id, {}).get("welcome_channel")
            print(channel)
            text = self.bot.settings.get(member.guild.id, {}).get("welcome_message")
            print(text)
            embed = self.bot.settings.get(member.guild.id, {}).get("welcome_message_embed")
            print(embed)
            if channel and (text or embed):
                channel = member.guild.get_channel(channel)
                text = helpers.format_message(text, guild=member.guild, user=member)
                embed = discord.Embed.from_dict(
                    helpers.format_message(embed, guild=member.guild, user=member)
                )
                await channel.send(content=text or None, embed=embed or None)
        except Exception as e:
            print(e)
            
    @commands.command(
        description="Displays the current welcome message", 
        name='displaywelcome',
        aliases = ["dw"]
    )
    async def displaywelcome(self, ctx):
        text = self.bot.settings.get(ctx.guild.id, {}).get("welcome_message")
        embed = self.bot.settings.get(ctx.guild.id, {}).get("welcome_message_embed")
        if text or embed:
            text = helpers.format_message(text, guild=ctx.guild, user=ctx.author)
            embed = discord.Embed.from_dict(
                helpers.format_message(embed, guild=ctx.guild, user=ctx.author)
            )
            await ctx.send(content=text or None, embed=embed or None)
        else:
            raise commands.MissingRequiredArgument("No welcome message or channel set!")
    
def setup(bot):
    bot.add_cog(Welcome(bot))