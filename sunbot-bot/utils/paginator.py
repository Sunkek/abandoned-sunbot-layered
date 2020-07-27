"""Pagination logic for topcharts"""

from discord import Embed
from asyncio import wait, TimeoutError, FIRST_COMPLETED

from . import rest_api, helpers

async def paginate(ctx, message, data, headers=None, footers=None):
    for i in ["⏮️", "⏪", "⏩", "⏭️"]:
        await message.add_reaction(i)
    print(data)
        
    def check(payload):
        return all((
            payload.user_id == ctx.author.id,
            payload.message_id == message.id,
            str(payload.emoji) in ["⏮️", "⏪", "⏩", "⏭️"],
        ))

    while True:
        done, pending = await wait([
            ctx.bot.wait_for("raw_reaction_add", check=check),
            ctx.bot.wait_for("raw_reaction_remove", check=check),
        ], return_when=FIRST_COMPLETED, timeout=20.0)

        try:
            payload = done.pop().result()
        except KeyError:
            # Triggers on timeout if no reactions made
            await message.clear_reactions()
            for future in pending: future.cancel()
            break

        # First page
        if str(payload.emoji) == "⏮️" and data["current"] != 1:
            url = data["next"] or data["previous"]
            url = url.split("?")[0] + "?page=1"
            channel = ctx.kwargs.get("channel")
            if channel: channel = channel.id
            data = await rest_api.send_get(
                ctx.bot, url,
                guild_id=ctx.guild.id, channel_id=channel,
            )
            columns = await helpers.parse_top_json(data["results"], ctx)
            table = helpers.format_columns(
                columns["count"], columns["user_name"], 
                headers=headers, footers=footers
            )
            embed = message.embeds[0]
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {data['current']}/{data['last']}"
            )
            await message.edit(embed=embed)

        # Previous page            
        elif str(payload.emoji) == "⏪" and data["previous"]:
            channel = ctx.kwargs.get("channel")
            if channel: channel = channel.id
            data = await rest_api.send_get(
                ctx.bot, data["previous"],
                guild_id=ctx.guild.id, channel_id=channel,
            )
            print("DATA")
            print(data)
            columns = await helpers.parse_top_json(data["results"], ctx)
            print("COLUMNS")
            print(columns)
            table = helpers.format_columns(
                columns["count"], columns["user_name"], 
                headers=headers, footers=footers
            )
            print("TABLE")
            print(table)
            embed = message.embeds[0]
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {data['current']}/{data['last']}"
            )
            await message.edit(embed=embed)

        # Next page
        elif str(payload.emoji) == "⏩" and data["next"]:
            channel = ctx.kwargs.get("channel")
            if channel: channel = channel.id
            data = await rest_api.send_get(
                ctx.bot, data["next"],
                guild_id=ctx.guild.id, channel_id=channel,
            )
            columns = await helpers.parse_top_json(data["results"], ctx)
            table = helpers.format_columns(
                columns["count"], columns["user_name"], 
                headers=headers, footers=footers
            )
            embed = message.embeds[0]
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {data['current']}/{data['last']}"
            )
            await message.edit(embed=embed)
        
        # Last page
        elif str(payload.emoji) == "⏭️" and data["current"] != data["last"]:
            url = data["next"] or data["previous"]
            url = url.split("?")[0] + f"?page={data['last']}"
            channel = ctx.kwargs.get("channel")
            if channel: channel = channel.id
            data = await rest_api.send_get(
                ctx.bot, url,
                guild_id=ctx.guild.id, channel_id=channel,
            )
            columns = await helpers.parse_top_json(data["results"], ctx)
            table = helpers.format_columns(
                columns["count"], columns["user_name"], 
                headers=headers, footers=footers
            )
            embed = message.embeds[0]
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {data['current']}/{data['last']}"
            )
            await message.edit(embed=embed)

        for future in pending: future.cancel()