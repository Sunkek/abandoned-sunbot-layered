"""Embed creator and formatter"""

import discord
from discord.ext import commands

import re
from typing import Optional

from utils import int_convertable

def parse_foreign_emoji(content):
    """This will try to find any "<foreign_emoji=number>" substrings and turn them 
    into "<:_:number>" so the emoji is shown (if possible)"""
    return content.replace('<foreign_emoji=', '<:_:')

class Embedder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_embed = {}

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name='newembed', 
        aliases=['ne'],
        description='Creates an embed in selected or current channel. Separate the title and description by `<|>` (yes, brackets included). To add and format the embed use `sb editembed`.',
    )
    async def new_embed(
        self, ctx, 
        channel: Optional[discord.TextChannel]=None, 
        *, content=''
    ):
        channel = channel or ctx.channel
        content = content.split('<|>') + ['', '']
        embed = discord.Embed(
            title=content[0] or discord.Embed.Empty,
            description=parse_foreign_emoji(content[1]) or discord.Embed.Empty
            )
        self.target_embed[ctx.author.id] = await channel.send(embed=embed)
        
    @commands.group(
        description="This is a command group that lets you edit a bot's embed", 
        name="editembed", 
        aliases=['ee'], 
        invoke_without_command=False
    )
    async def edit_embed(self, ctx, 
        channel: Optional[discord.TextChannel]=None, 
        message_id: Optional[int]=None
    ):
        # Check the message
        saved_message = self.target_embed.get(ctx.author.id)
        if saved_message:
            saved_message = await saved_message.channel.fetch_message(saved_message.id)
        if not saved_message and not channel and not message_id:
            raise commands.BadArgument(message='No target message.')
        if channel and message_id:
            message = await channel.fetch_message(message_id)
            if message != saved_message:
                if not message.author == self.bot.user and not message.embeds:
                    raise commands.BadArgument(message="Can't edit this message.")
                self.target_embed[ctx.author.id] = message

    @edit_embed.command(
        description="Edits selected embed's title", 
        name="title", 
        aliases=['t']
    )
    async def edit_embed_title(self, ctx, *, title=''):
        title = title or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].title = title
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Edits selected embed's description", 
        name="description", 
        aliases=['d']
    )
    async def edit_embed_description(self, ctx, *, description=''):
        description = description or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].description = parse_foreign_emoji(description)
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Edits selected embed's color. Provide a hex code.", 
        name="color", 
        aliases=['c']
    )
    async def edit_embed_color(self, ctx, color:Optional[discord.Color]=None):
        color = color or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].color = color
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Edits selected embed's image. Provide an image URL or attachment. Don't delete the latter if you want it to work properly.", 
        name="image", 
        aliases=['i', 'img']
    )
    async def edit_embed_image(self, ctx, image=''):
        if not image and ctx.message.attachments:
            image = ctx.message.attachments[0].url
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_image(url=image)
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Edits selected embed's thumbnail image. Provide an image URL or attachment. Don't delete the latter if you want it to work properly.", 
        name="thumbnail", 
        aliases=['tn', 'thumb']
    )
    async def edit_embed_thumbnail(self, ctx, image=''):
        if not image and ctx.message.attachments:
            image = ctx.message.attachments[0].url
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_thumbnail(url=image)
        await message.edit(embed=message.embeds[0])
        
    @edit_embed.command(
        description="Adds a new field to the selected embed. If you need to add a field at certain index, provide the number. Then provide field name and value separated by `<|>` (with brackets). The fields are inlined by default - if you don't want the field to inline, add `noinline`, also separated by `<|>`. It might be confusing, so here's an example:\n`sb editembed #channel 123 newfield 3 Field Name <|> Field Value <|> noinline`", 
        name="newfield", 
        aliases=['nf']
    )
    async def edit_embed_new_field(self, ctx, target: Optional[int]=0, *, content):
        content = [i.strip() for i in content.split('<|>')]
        inline = True
        if 'noinline' in content or 'NOINLINE' in content:
            inline = False
            content = [
                i for i in content 
                if i not in ('noinline', 'NOINLINE')
            ]     
        message = self.target_embed[ctx.author.id]
        if target:
            message.embeds[0].insert_field_at(
                index=target-1, name=content[0], value=parse_foreign_emoji(content[1]), inline=inline
            )
        else:
            message.embeds[0].add_field(
                name=content[0], value=parse_foreign_emoji(content[1]), inline=inline
            )
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Edits a field of the selected embed. First target the field by it's number, then provide new field name and value separated by `<|>` (with brackets). If you don't want to change name or value, leave them empty. If you don't want the field to inline, add `noinline`, otherwise add `inline`. Field name, value and inline are separated by `<|>`. It might be confusing, so here's an example:\n`sb editembed #channel 123 editfield 3 Field Name <|> Field Value <|> inline`", 
        name="editfield", 
        aliases=['ef']
    )
    async def edit_embed_edit_field(self, ctx, target: int, *, content):
        message = self.target_embed[ctx.author.id]
        content = [i.strip() for i in content.split('<|>')] + ['']*3
        inline = None  
        if 'noinline' in content or 'NOINLINE' in content:
            inline = False
            content = [
                i for i in content 
                if i not in ('noinline', 'NOINLINE')
            ]       
        elif 'inline' in content or 'INLINE' in content:
            inline = True
            content = [
                i for i in content 
                if i not in ('noinline', 'NOINLINE')
            ]   
        target = target - 1
        message.embeds[0].set_field_at(
            index=target,
            name=content[0] or message.embeds[0].fields[target].name,
            value=parse_foreign_emoji(content[1]) or message.embeds[0].fields[target].value,
            inline = inline if inline is not None else message.embeds[0].fields[target].inline
        )        
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Deletes the field at specified index from the selected embed", 
        name="removefield", 
        aliases=['rf', 'deletefield', 'df']
    )
    async def edit_embed_remove_field(self, ctx, target: int):
        message = self.target_embed[ctx.author.id]
        message.embeds[0].remove_field(index=target-1)
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets URL for the selected embed", 
        name="url",
    )
    async def edit_embed_url(self, ctx, url=''):
        message = self.target_embed[ctx.author.id]
        message.embeds[0].url = url
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets footer text for the selected embed. Send no text to reset it", 
        name="footertext",
        aliases=['ft']
    )
    async def edit_embed_footer_text(self, ctx, *, text=None):
        text=text or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_footer(
            text=text,
            icon_url=message.embeds[0].footer.icon_url,
        )
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets footer icon using the image from your URL for the selected embed. Send no URL to reset it", 
        name="footericon",
        aliases=['fi']
    )
    async def edit_embed_footer_icon(self, ctx, url=None):
        url=url or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_footer(
            text=message.embeds[0].footer.text,
            icon_url=url,
        )
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets author name for the selected embed. Send no text to reset it", 
        name="authorname",
        aliases=['an']
    )
    async def edit_embed_author_name(self, ctx, *, name=None):
        name=name or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_author(
            name=name,
            url=message.embeds[0].author.url,
            icon_url=message.embeds[0].author.icon_url
        )
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets author URL for the selected embed. Send no URL to reset it", 
        name="authorurl",
        aliases=['aurl', 'al', 'au']
    )
    async def edit_embed_author_url(self, ctx, url=None):
        url=url or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_author(
            name=message.embeds[0].author.name, 
            url=url,
            icon_url=message.embeds[0].author.icon_url
        )
        await message.edit(embed=message.embeds[0])

    @edit_embed.command(
        description="Sets author icon to the image by your URL for the selected embed. Send no URL to reset it", 
        name="authoricon",
        aliases=['ai']
    )
    async def edit_embed_author_icon(self, ctx, url=None):
        url=url or discord.Embed.Empty
        message = self.target_embed[ctx.author.id]
        message.embeds[0].set_author(
            name=message.embeds[0].author.name, 
            url=message.embeds[0].author.url,
            icon_url=url
        )
        await message.edit(embed=message.embeds[0])

def setup(bot):
    bot.add_cog(Embedder(bot))