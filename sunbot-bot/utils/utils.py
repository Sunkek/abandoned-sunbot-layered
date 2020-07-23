"""Misc helper functions"""

from datetime import datetime, timedelta
import discord

def int_convertable(string):
    """Return True if string is convertable into int"""
    try: 
        int(string)
        return True
    except ValueError:
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
        if headers: columns[i] = [headers[i]] + columns[i]
        if footers: columns[i] += [footers[i]]
    maxlens = [max(len(str(line)) for line in column) for column in columns]
    table = []
    for row in zip(*columns):
        line = f'{row[0]:.<{maxlens[0]}}'
        for num, value in enumerate(row[1:-1], 1):
            line += f'..{value:.^{maxlens[num]}}'
        line += f'..{row[-1]:.>{maxlens[-1]}}'
        table.append(line)
    return '\n'.join(table)


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

async def add_name_column(bot, guild, chart):
    return [
        [
            item['member_id'], 
            item['count'],
            await get_member_name(bot, guild, item['member_id'])
        ] if item['member_id'] != "TOTAL" else ['TOTAL', '', item['count']]
        for item in chart
    ]

    
def format_settings_key(string):
    return string.lower().replace('_id', '').replace('_', ' ').capitalize()
    
def format_settings_value(guild, value):
    result = ''
    if int_convertable(value) and not type(value) == bool:
        value = int(value)
        result = guild.get_channel(value)
    if not result:
        result = guild.get_role(value)
    if not result:
        result = guild.get_member(value)
    if result:
        result = result.mention
    else:
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