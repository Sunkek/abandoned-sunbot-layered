"""Helper functions to address the REST API"""

host = "http://api:8080"
urls = {
    "user":f"{host}/api/v1/user/",
    
    "settings":f"{host}/api/v1/settings/",





    "guilds":f"{host}/api/v1/server/",
    
    "messages":f"{host}/api/v1/messages/",
    "voice":f"{host}/api/v1/voice/",
    "reactions":f"{host}/api/v1/reactions/",
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
        
async def add_message(bot, **kwargs):
    """Save message data to the database"""
    async with bot.web.patch(
        urls["messages"], json=kwargs
    ) as resp:
        return resp
    return

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
        f"{urls['settings']}guild_id/", json=kwargs
    ) as resp:
        guild = bot.settings[guild_id]
        for key, value in kwargs.items():  
            if value == "reset": guild[key] = 0
            else: guild[key] = value
        return resp
