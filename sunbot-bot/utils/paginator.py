from discord import Embed
from asyncio import wait, TimeoutError, FIRST_COMPLETED

import rest_api, helpers

async def paginate(ctx, message, data, headers, footers):
    for i in ["⏮️", "⏪", "⏩", "⏭️"]:
        await message.add_reaction(i)
        
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

        if str(payload.emoji) == "⏮️" and data["current"] != 1:
            url = data["next"] or data["previous"]
            url = url.split("?")[0] + "?page=1"
            top_chart = await rest_api.send_get(
                ctx.bot, url, 
                guild_id=ctx.guild.id, channel_id=ctx.kwargs.get("channel"),
            )
            
            columns = await helpers.parse_top_json(top_chart, ctx)
            table = helpers.format_columns(
                columns["counts"], columns["user_names"], 
                headers=headers, footers=footers
            )
            time_range = ctx.kwargs.get("time_range")
            if ctx.kwargs.get("channel"):
                channel = f"in {ctx.kwargs.get('channel').name}" 
            else:
                channel = ""
            embed = message.embeds[0]
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {data['current']}/{data['last']}"
            )
            await message.edit(embed=embed)





            
        elif str(payload.emoji) == "⏪" and top_chart["previous"]:
            top_chart = await rest_api.send_get(
                self.bot, 
                top_chart["previous"], 
                guild_id=ctx.guild.id,
                channel_id=channel,
            )
            user_ids = [i["user_id"] for i in top_chart["results"]]
            postcounts = [i["count"] for i in top_chart["results"]]
            user_ids, postcounts = zip(*[
                (i["user_id"], i["count"]) for i in top_chart["results"]
            ])
            user_ids = [
                await helpers.get_member_name(
                    self.bot, ctx.guild, i
                ) for i in user_ids
            ]
            postcounts = list(postcounts)
            headers = ["POSTCOUNT", "MEMBER"]
            footers = [top_chart["total"], "TOTAL"]
            table = helpers.format_columns(
                postcounts, user_ids, headers=headers, footers=footers
            )
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {top_chart['current']}/{top_chart['last']}"
            )
            await message.edit(embed=embed)
        elif str(payload.emoji) == "⏩" and top_chart["next"]:
            top_chart = await rest_api.send_get(
                self.bot, 
                top_chart["next"], 
                guild_id=ctx.guild.id,
                channel_id=channel,
            )
            user_ids = [i["user_id"] for i in top_chart["results"]]
            postcounts = [i["count"] for i in top_chart["results"]]
            user_ids, postcounts = zip(*[
                (i["user_id"], i["count"]) for i in top_chart["results"]
            ])
            user_ids = [
                await helpers.get_member_name(
                    self.bot, ctx.guild, i
                ) for i in user_ids
            ]
            postcounts = list(postcounts)
            headers = ["POSTCOUNT", "MEMBER"]
            footers = [top_chart["total"], "TOTAL"]
            table = helpers.format_columns(
                postcounts, user_ids, headers=headers, footers=footers
            )
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {top_chart['current']}/{top_chart['last']}"
            )
            await message.edit(embed=embed)
        elif str(payload.emoji) == "⏭️" and top_chart["current"] != top_chart["last"]:
            url = top_chart["next"] or top_chart["previous"]
            url = url.split("?")[0] + f"?page={top_chart['last']}"
            top_chart = await rest_api.send_get(
                self.bot, 
                url, 
                guild_id=ctx.guild.id,
                channel_id=channel,
            )
            user_ids = [i["user_id"] for i in top_chart["results"]]
            postcounts = [i["count"] for i in top_chart["results"]]
            user_ids, postcounts = zip(*[
                (i["user_id"], i["count"]) for i in top_chart["results"]
            ])
            user_ids = [
                await helpers.get_member_name(
                    self.bot, ctx.guild, i
                ) for i in user_ids
            ]
            postcounts = list(postcounts)
            headers = ["POSTCOUNT", "MEMBER"]
            footers = [top_chart["total"], "TOTAL"]
            table = helpers.format_columns(
                postcounts, user_ids, headers=headers, footers=footers
            )
            embed.description=f"`{table}`"
            embed.set_footer(
                text=f"Page {top_chart['current']}/{top_chart['last']}"
            )
            await message.edit(embed=embed)
        for future in pending: future.cancel()