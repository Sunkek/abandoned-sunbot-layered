import discord
from discord.ext import commands

from datetime import datetime, timedelta
from pycountry import countries
from bs4 import BeautifulSoup
from typing import Optional

from utils import rest_api

class Binder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.targets = {}
        
    @commands.group(
        description="`bind <target argument> <value>` - adds information to your profile in this bot's database. Use without `<value>` to reset.", 
        aliases = ["b"], 
        invoke_without_command=False,
    )
    async def bind(self, ctx, target: Optional[discord.Member]=None):
        pass

    @bind.command(
        description="`bind birthday <dd/mm/yyyy>` - adds the birthday date to your entry in the database. It will be used in the birthday feed, if one is set up for a server you're in.", 
        name="birthday",
    )
    async def bind_birthday(self, ctx, birthday="reset"):
        if birthday != "reset":
            birthday = datetime.strptime(birthday, "%d/%m/%Y")
            if datetime.now() - birthday > timedelta(days=365*100):
                raise commands.BadArgument
            birthday = birthday.strftime("%Y-%m-%d")
        await rest_api.bind_user_param(self.bot, ctx.author.id, birthday=birthday)

    @bind.command(
        description="`bind country <official name or 2 or 3 letter code>` - adds the country to your entry in the database.", 
        name="country"
    )
    async def bind_country(self, ctx, *, country="reset"):
        # Check the country name
        if country != "reset":
            country = countries.lookup(country) 
            if country:
                country = country.name
            else:
                raise commands.BadArgument
        await rest_api.bind_user_param(self.bot, ctx.author.id, country=country)
                
    @bind.command(
        description="`bind steam <steam profile link>` - adds the steam profile to your entry in the database.", 
        name="steam"
    )
    async def bind_steam(self, ctx, *, steam="reset"):
        # Bring the link to universal format
        if steam != "reset":
            steam = steam.rstrip("/").split("/")
            steam_id = steam[-1]
            if not steam_id.isdigit() or steam[-2] != "profiles":
                url = f"https://steamcommunity.com/id/{steam_id}/?xml=1"
                async with self.bot.web.get(url) as resp:
                    raw_user = await resp.text()
                    soup = BeautifulSoup(raw_user, 'lxml-xml')
                    steam_id = soup.find('steamID64').string
            #steam = f"https://steamcommunity.com/profiles/{steam_id}"
        await rest_api.bind_user_param(self.bot, ctx.author.id, steam=steam_id)
                
    @bind.command(
        description="`bind pcwarframe` - adds the PC Warframe name to your entry in the database.", 
        name="pcwarframe"
    )
    async def bind_pcwarframe(self, ctx, *, name="reset"):
        if name != "reset":
            if len(name) > 25:
                raise commands.BadArgument
        await rest_api.bind_user_param(self.bot, ctx.author.id, ign_warframe_pc=name)  

    @bind.command(
        description="`bind ddo` - adds the DDO character name to your entry in the database.", 
        name="ddo"
    )
    async def bind_ddo(self, ctx, *, name="reset"):
        if name != "reset":
            if len(name) > 50:
                raise commands.BadArgument
        await rest_api.bind_user_param(self.bot, ctx.author.id, ign_ddo=name)

def setup(bot):
    bot.add_cog(Binder(bot))