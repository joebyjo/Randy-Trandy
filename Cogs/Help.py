import discord
from discord.ext import commands
from discord.ext.buttons import Paginator
from discord.colour import Colour

# class Help(commands.MinimalHelpCommand):
#
#     async def send_command_help(self, command):
#         embed = discord.Embed(title='\n', color=random_color())
#         embed.add_field(name=f"` {self.get_command_signature(command)} `", value=f"` {self.get_command_signature(command)} `",)
#         alias = command.aliases
#         if alias:
#             embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
#         channel = self.get_destination()
#         await channel.send(embed=embed)
#
#     async def send_pages(self):
#         destination = self.get_destination()
#         for page in self.paginator.pages:
#             emby = discord.Embed(description=page, color=random_color())
#             await destination.send(embed=emby)


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cmds_per_page = 6

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []
        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return filtered

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self, ctx, entity=None, title=None):
        entity = entity or self.client
        title = title or self.client.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        # for i in range(0, len(filtered_commands), self.cmds_per_page):
        #     next_commands = filtered_commands[i: i + self.cmds_per_page]
        #     commands_entry = ""
        #
        #     for cmd in next_commands:
        #         desc = cmd.short_doc or cmd.description
        #         signature = self.get_command_signature(cmd, ctx)
        #         subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""
        #
        #         commands_entry += (
        #             f"```\n{signature}\n```\n{desc}\n"
        #             if isinstance(entity, commands.Command)
        #             else f"```\n{signature}\n```\n{desc}\n{subcommand}\n"
        #         )
        #     pages.append(commands_entry)

        for cogg in self.client.cogs:
            for command in self.client.get_cog(cogg).get_commands():
                print(command)

        await Pag(title=title, color=Colour.random(), entries=pages, length=1).start(ctx)

    @commands.command(name="help", description="This help command!")
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.setup_help_pag(ctx, title="Help")

        else:
            cog = self.client.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:

                command = self.client.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send("Entity not found.")

# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(Help(client))
