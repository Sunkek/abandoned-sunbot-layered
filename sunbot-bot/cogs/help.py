import discord
from discord.ext import commands
        
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='help', 
        description="Shows all bot cogs. If you ask help for specific cog, it shows commands for that cog. If you ask for specific command, it shows the command's description and other available info.",
        aliases=['h']
    )
    async def help(self, ctx, *, target=None):
        # General help
        if not target:
            e = discord.Embed(
                title='Help categories', 
                description='For help about any specific cog, type `sb help <cog>`, case-sensitive.',
                color=ctx.author.color,
            )
            cog_list = []
            for name, cog in self.bot.cogs.items():
                if [command for command in cog.walk_commands()]:
                    cog_list.append(name)
            cog_list.sort()
            e.add_field(
                name='Cogs',
                value='`' + '\n'.join(cog_list) + '`'
            )
        # Help for a cog
        elif target in self.bot.cogs.keys():
            e = discord.Embed(
                title=f'Help for {target}', 
                color=ctx.author.color,
            )
            cog = self.bot.get_cog(target)
            command_set = set()
            for command in cog.walk_commands():
                # Only show the command if author can use it
                try:
                    await command.can_run(ctx)
                    command_set.add(f'`{command.qualified_name}`')
                except commands.CommandError:
                    pass
            if command_set:
                command_set = sorted(list(command_set))
                e.add_field(name='Commands', value='\n'.join(command_set))
            else:
                e.add_field(name='Commands', value='No available commands')
        # Help for a command
        elif target in [c.qualified_name for c in self.bot.walk_commands()]:   
            command = self.bot.get_command(target)
            await command.can_run(ctx)
            args = [
                f'<{p.name}>' for p in command.params.values() 
                if p.name not in ('self', 'ctx')
            ]
            e = discord.Embed(
                title='Command Help', 
                description=f'`{command.qualified_name} {" ".join(args)}`',
                color=ctx.author.color,
            )
            if command.description:
                e.add_field(
                    name="Description", 
                    value=command.description, 
                    inline=False
                )   
            # If the command has subcommands, list them
            if hasattr(command, 'commands'):
                command_set = set()
                for subcommand in command.commands:
                    # Only show the subcommand if author can use it
                    try:
                        await subcommand.can_run(ctx)
                        command_set.add(f'`{subcommand.qualified_name}`')
                    except commands.CommandError:
                        pass
                if command_set:
                    e.add_field(
                        name="Subcommands", 
                        value='\n'.join(sorted(list(command_set))), 
                        inline=False
                    )   
            if command.aliases:
                e.add_field(
                    name="Aliases", 
                    value=f"`{', '.join(command.aliases)}`",
                    inline=False
                )
        else:
            raise commands.BadArgument

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Help(bot))