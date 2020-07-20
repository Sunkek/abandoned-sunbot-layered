"""My own Discord bot, made to automate the boring admin work
and to track server statistics. Some of its features only work on 
`A Piece of Cake` server."""

import discord 
from discord.ext import commands

import aiohttp
import socket
import asyncio
import os
from random import choice, seed
from datetime import datetime

from utils import rest_api

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("sb ", "Sb ", "SB "), 
    сase_insensitive=True,
)
# Remove the default help command because there will be a custom one
bot.remove_command("help")
bot.web = None
bot.settings = None
bot.error_titles = (
    "No", "Nope", "I don't think so", "Not gonna happen", "Nah", "Not likely", 
    "Fat chance", "Fuck you", "Good try, asshole", "No way", 
    "Did you really think I would do that?", "Do this shit yourself",
)  
cogs = []
# Reading cog names
for (dirpath, dirnames, filenames) in os.walk(f"{os.getcwd()}/cogs/"):
    if "__pycache__" not in dirpath:
        # Getting relative cog path, stripping the .py extension and replacing 
        # slashes with dots for cog import
        cogs += [
            os.path.join(dirpath, file).replace(
                f"{os.getcwd()}/", 
                ""
            ).replace(".py", "").replace("/", ".") .replace("\\", ".") 
            for file in filenames if "pycache" not in file
        ]
        
@bot.event
async def on_ready():
    #bot.apoc = bot.get_guild(107900245270110208)
    #bot.guild_log = bot.apoc.get_channel(721044808080293899)
    if not bot.web:
        bot.web = aiohttp.ClientSession(
            loop=bot.loop,
            connector=aiohttp.TCPConnector( 
                family=socket.AF_INET, #https://github.com/aio-libs/aiohttp/issues/2522#issuecomment-354454800
                ssl=False, 
                ),
            )
    if not bot.settings:
        settings = await rest_api.get_settings(bot)
        # Because JSON turned all guild IDs into strings
        bot.settings = {int(k): v for k, v in settings(items)}
    if not bot.cogs:
        for cog in cogs:
            try:
                if cog not in bot.cogs.values():
                    bot.load_extension(cog)
            except Exception as e:
                print(f"Error on loading {cog}:\n{e}")
    await bot.change_presence(activity=discord.Game(name=("sb ")))
    print(f"{bot.user} online")
    print(datetime.now())

@bot.event 
async def on_message(message):
    await bot.wait_until_ready()   
    """if bot.user.mentioned_in(message):
        # Ping reee
        # The emoji is from apoc
        await message.add_reaction("a:ping:456710949215272981")"""
    # Without this it will ignore all commands
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    await ctx.message.add_reaction("👌")

@bot.event 
async def on_command_error(ctx, error):
    """Command error handler"""
    await ctx.message.add_reaction("✋")
    # Refresh random seed just in case
    seed()
    embed = discord.Embed(
        title=choice(bot.error_titles),
        color=ctx.author.color
    )
    if isinstance(error, commands.CommandNotFound):
        embed.description = "There is no such command."
        return await ctx.send(embed=embed)
    if ctx.command.description:
        embed.add_field(
            name="Command help", 
            value=ctx.command.description,
            inline=False
        )
    if isinstance(error, asyncio.TimeoutError):
        embed.description = "You took too long to reply."
    elif isinstance(error, commands.MissingPermissions):
        embed.description = (
            "You are missing permissions to use this "
            f"command: **{error.missing_perms[0]}**."
        )
    elif isinstance(error, commands.BadArgument):
        embed.description = "Something is wrong with the arguments."
        if ctx.command.description:
            embed.add_field(
                name="Command help", 
                value=ctx.command.description,
                inline=False
            )
    else:
        embed.description = "Something went wrong."
        embed.add_field(
            name="Error", 
            value=error,
            inline=False
        )
    await ctx.send(embed=embed)

"""@bot.event 
async def on_guild_join(guild):
    desc = f"Name: {guild.name}\nMembers: {len(guild.members)}\nID: {guild.id}\nOwned by: {guild.owner.mention if guild.owner else None}"
    embed = discord.Embed(
        title=f"{bot.user.name} joined a new server!",
        #color=bot.apoc.me.color,
        description=desc
    )
    embed.set_image(url=guild.icon_url)
    await bot.guild_log.send(embed=embed)

@bot.event 
async def on_guild_remove(guild):
    desc = f"Name: {guild.name}\nMembers: {len(guild.members)}\nID: {guild.id}\nOwned by: {guild.owner.mention if guild.owner else None}"
    embed = discord.Embed(
        title=f"{bot.user.name} was removed from a server",
        #color=bot.apoc.me.color,
        description=desc
    )
    embed.set_image(url=guild.icon_url)
    await bot.guild_log.send(embed=embed)"""

@commands.check(commands.is_owner())
@bot.command(description=f"`reload <cog name>` - reloads the specified cog")
async def reload(ctx, *, ext):
    cog = f"cogs.{ext}"
    try:
        bot.unload_extension(cog)
    except commands.ExtensionNotLoaded:
        pass
    bot.load_extension(cog)

bot.run(os.environ.get("DISCORD_TOKEN"))