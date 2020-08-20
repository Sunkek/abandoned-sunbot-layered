"""Misc helper functions"""

from datetime import datetime, timedelta

import discord
import collections

PLACEHOLDERS = (
    "`user.name` - replaced with the target user name, if applicable\n"
    "`user.id` - replaced with the target user ID, if applicable\n"
    "`user.mention` - replaced with the target user mention, if applicable"
)

def int_convertable(string):
    """Return True if string is convertable into int"""
    try: 
        int(string)
        return True
    except (ValueError, TypeError):
        return False

def format_seconds(seconds):
    """Format seconds into easily readable format"""
    years = seconds // (60*60*24*365)
    seconds %= (60*60*24*365)
    days = seconds // (60*60*24)
    seconds %= (60*60*24)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    ye = f"{int(years)}y " if years else ''
    da = f"{int(days)}d " if days else ''
    ho = f"{int(hours)}h " if hours else ''
    mi = f"{int(minutes)}m " if minutes else ''
    se = f"{int(seconds)}s" if seconds else ''
    return f"{ye}{da}{ho}{mi}{se}".strip()

async def get_member_name(bot, guild, member_id):
    """Return member's guild nickname if possible, otherwise just name"""
    try:
        return guild.get_member(member_id).display_name
    except AttributeError:
        member = await bot.fetch_user(member_id)
        return member.name

def format_columns(*columns, headers=None, footers=None):
    """Tabulate columns (lists) into a neatly aligned table"""
    columns = list(columns)
    for i in range(len(columns)):
        if type(columns[i]) != list: columns[i] = list(columns[i])
        if headers: columns[i] = [headers[i]] + columns[i]
        if footers: columns[i] += [footers[i]]
    maxlens = [max(len(str(line)) for line in column) for column in columns]
    if headers:
        for i in range(len(headers)):
            if headers[i] == "EMOTE":
                maxlens[i] = 5
                break
    table = []
    for row in zip(*columns):
        line = f'{row[0]:.<{maxlens[0]}}'
        for num, value in enumerate(row[1:-1], 1):
            line += f'..{value:.^{maxlens[num]}}'
        line += f'..{row[-1]:.>{maxlens[-1]}}'
        table.append(line)
    return '\n'.join(table)
    
def format_settings_key(string):
    result = string.lower().replace("activity", "").replace("track", "")
    result = result.replace("ad_reminder", "").replace("verification", "")
    result = result.lstrip("_").replace("_id", "").replace("_", " ").capitalize()
    return f'`{result}`'
    
def format_settings_value(guild, value):
    if type(value) == list:
        result = []
        for i in value:
            formatted_value = ""
            if int_convertable(i) and not type(i) == bool:
                formatted_value = guild.get_channel(int(i))
                if not formatted_value:
                    formatted_value = guild.get_role(int(i))
                if not formatted_value:
                    formatted_value = guild.get_member(int(i))
                if formatted_value:
                    formatted_value = formatted_value.mention
            elif type(i) == dict or type(i) == list:
                formatted_value = "Set"
            elif value == True:
                formatted_value = "On"
            if not formatted_value:
                formatted_value = i
            result.append(formatted_value)
        result = ", ".join(result)
    else:
        result = ""        
        if int_convertable(value) and not type(value) == bool:
            result = guild.get_channel(int(value))
            if not result:
                result = guild.get_role(int(value))
            if not result:
                result = guild.get_member(int(value))
            if result:
                result = result.mention
        elif type(value) == dict or type(value) == list:
            result = "Set"
        elif value == True:
            result = "On"
        if not result:
            result = value
    return result

def format_info_key(string):
    result = [
        i.capitalize() 
        if i not in ('ign', 'pc', 'ps4', 'id', "ddo")
        else i.upper()
        for i in string.split('_')
    ]
    return ' '.join(result)
    
def format_settings(settings, ctx, include=[], ignore=[]):
    return "\n".join([
        f"{format_settings_key(key)}: \
            {format_settings_value(ctx.guild, value)}"
        for key, value in settings.items()
        if value \
            and any([i in key for i in include] if include else [True]) \
            and all([i not in key for i in ignore])])

async def parse_top_json(json, ctx):
    """Turn the backend response into result lists"""
    if not json: return
    lists = collections.defaultdict(list)
    for i in json:
        for key, value in i.items():
            if key == "emote":  # Excape codeblock for emotes
                lists[key].append(f"`{value}`")
            else:
                lists[key].append(value)
            if key == "user_id":
                lists["user_name"].append(
                    await get_member_name(ctx.bot, ctx.guild, value)
                )
    return lists

def make_guild_emote_list(ctx):
    return [":_:".join(str(emoji).split(":")[::2]) for emoji in ctx.guild.emojis]

def format_message(text, guild=None, user=None):
    print(guild)
    print(user)
    if not text:
        return None
    if user:
        text = text.replace("user.name", user.name)
        text = text.replace("user.id", str(user.id))
        text = text.replace("user.mention", user.mention)
    return text





def columns_to_table(columns, numerate=False):
    if numerate:
        nums = ['#'] + [i for i in range(1, len(columns[0])-1)] + ['']
        columns = [nums] + columns
    maxlens = [max(len(str(row)) for row in column) for column in columns]
    table = []
    for row in zip(*columns):
        line = f'{row[0]:.<{maxlens[0]}}'
        for num, value in enumerate(row[1:-1], 1):
            line += f'.{value:.^{maxlens[num]}}'
        line += f'.{row[-1]:.>{maxlens[-1]}}'
        table.append(line)
    return '`' + '\n'.join(table) + '`'

def parse_topchart_args(args):
    lowered_args = [i.lower() for i in args]
    args = list(args)
    result = {}
    if 'year' in lowered_args: 
        result['time_range'] = 'year'
        args.remove('year')
    elif 'alltime' in lowered_args:
        result['time_range'] = 'alltime'
        args.remove('alltime')
    elif 'month' in lowered_args:
        result['time_range'] = 'month'
        args.remove('month')
    else:
        result['time_range'] = 'month'
    if any((i in lowered_args for i in ('id', 'ids', 'showid', 'showids'))):
        result['show_ids'] = True
        args = [i for i in args if i not in ('id', 'ids', 'showid', 'showids')]
    else:
        result['show_ids'] = False
    if any((i in lowered_args for i in ('nonum', 'nonumeration', 'nonembers'))):
        result['numeration'] = False
        args = [i for i in args if i not in ('nonum', 'nonumeration', 'nonembers')]
    else:
        result['numeration'] = True
    if any((i in lowered_args for i in ('p', 'personal', 'my', 'me'))):
        result['personal'] = True
    else:
        result['personal'] = False
    result['other'] = args[0] if args else None
    return result

async def log(
    ctx,
    target=None,
    channel=0, # Have a default log channel for each server?
    title=discord.Embed.Empty, 
    details=None, 
):
    channel = ctx.guild.get_channel(channel)
    if channel:
        e = discord.Embed(
            title=title,
            description=f'Initiator: {ctx.author.mention}\nTarget: {target}',
            color=ctx.author.color,
            timestamp=datetime.utcnow(),
        )
        if details:
            e.add_field(name='Details', value=details)
        e.add_field(
            name='Link',
            value=f'[jump]({ctx.message.jump_url})',
            inline=False
            )
        await channel.send(embed=e)
