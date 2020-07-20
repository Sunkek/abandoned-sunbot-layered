"""Helper functions to address the REST API"""

import os


host = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}"
urls = {
    "user": f"{host}/api/v1/user/",
    
    "settings": f"{host}/api/v1/settings/",

    "born_today": f"{host}/api/v1/birthdays/today",

    "messages":f"{host}/api/v1/messages/",
    "reactions":f"{host}/api/v1/reactions/",



    
    "voice":f"{host}/api/v1/voice/",
    "games":f"{host}/api/v1/games/",

    "warnings":f"{host}/api/v1/warning/",
    
    "top_postcounts":f"{host}/api/v1/top/postcounts/",
    "top_wordcounts":f"{host}/api/v1/top/wordcounts/",
    "top_attachments":f"{host}/api/v1/top/attachments/",

    "top_reactions_given":f"{host}/api/v1/top/reactions/given/",
    "top_reactions_received":f"{host}/api/v1/top/reactions/received/",
    
    "top_voiceminutes":f"{host}/api/v1/top/voiceminutes/",

    "top_games":f"{host}/api/v1/top/games/",
    "top_players":f"{host}/api/v1/top/players/",
}


async def get_settings(bot):
    """Get settings for all servers"""
    async with bot.web.get(urls["settings"]) as resp:
        json = await resp.json()
        return json
        
async def get_user_info(bot, user_id):
    """Get user info"""
    async with bot.web.get(f"{urls['user']}{str(user_id)}/") as resp:
        json = await resp.json()
        return json

async def bind_user_param(bot, user_id, **kwargs):
    """Change user parameters"""
    async with bot.web.patch(
        f"{urls['user']}{str(user_id)}/", json=kwargs
    ) as resp:
        return resp
        
async def set_guild_param(bot, guild_id, **kwargs):
    """Change guild settings"""
    async with bot.web.patch(
        f"{urls['settings']}{guild_id}/", json=kwargs
    ) as resp:
        if guild_id not in bot.settings:
            bot.settings[guild_id] = {}
        guild = bot.settings[guild_id]
        for key, value in kwargs.items():  
            if value == "reset": guild[key] = None
            else: guild[key] = value
        return resp
    
async def get_born_today(bot):
    """Get a list of members whose birthday is today"""
    async with bot.web.get(urls['born_today']) as resp:
        json = await resp.json()
        return json
        
async def add_message(bot, **kwargs):
    """Save message data to the database"""
    async with bot.web.patch(urls["messages"], json=kwargs) as resp:
        return resp
    
async def add_reaction(bot, **kwargs):
    """Save reaction data to the database"""
    async with bot.web.patch(urls['reactions'], json=kwargs) as resp:
        return resp
