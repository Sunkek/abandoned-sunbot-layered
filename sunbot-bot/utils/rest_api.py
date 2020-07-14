"""Helper functions to address the REST API"""

host = "api:8080"
urls = {
    "settings":f"{host}/api/v1/settings",

    "guilds":f"{host}/api/v1/server",
    "user":f"{host}/api/v1/user",
    
    "messages":f"{host}/api/v1/messages",
    "voice":f"{host}/api/v1/voice",
    "reactions":f"{host}/api/v1/reactions",
    "games":f"{host}/api/v1/games",

    "warnings":f"{host}/api/v1/warning",
    
    "top_postcounts":f"{host}/api/v1/top/postcounts",
    "top_wordcounts":f"{host}/api/v1/top/wordcounts",
    "top_attachments":f"{host}/api/v1/top/attachments",

    "top_reactions_given":f"{host}/api/v1/top/reactions/given",
    "top_reactions_received":f"{host}/api/v1/top/reactions/received",
    
    "top_voiceminutes":f"{host}/api/v1/top/voiceminutes",

    "top_games":f"{host}/api/v1/top/games",
    "top_players":f"{host}/api/v1/top/players",
}

async def add_message(bot, **kwargs):
    """Save message data to the database"""
    async with bot.web.post(
        urls["messages"], json=kwargs
    ) as resp:
        return resp
    return

async def get_user_info(bot, user_id):
    """Get user info"""
    async with bot.web.get(urls['user']+str(user_id)) as resp:
        json = await resp.json()
        print(json)
        return json

async def bind_user_param(bot, user_id, **kwargs):
    """Change user parameters"""
    async with bot.web.patch(
        urls['user']+str(user_id), json=kwargs
    ) as resp:
        return resp