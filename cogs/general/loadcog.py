import discord
from discord import ApplicationContext as Context
from discord.ext import commands
from discord.ext.commands import slash_command as SlashCommand


class CogControl(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @SlashCommand(name='load', description='Loads a specific cog.')
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    async def load_cog(self, ctx: Context, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as err:
            await ctx.respond(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.respond(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been loaded.', delete_after=10)

    @SlashCommand(name='unload', description='Unloads a specific cog.')
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    async def unload_cog(self, ctx: Context, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as err:
            await ctx.respond(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.respond(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been unloaded.', delete_after=10)

    @SlashCommand(name='reload', description='Reloads specific cog.')
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    async def reload_cog(self, ctx: Context, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as err:
            await ctx.respond(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.respond(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been reloaded.', delete_after=10)

    @SlashCommand(name='cogs', description='List all loaded cogs.')
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    async def list_cogs(self, ctx: Context):
        cogs = self.bot.extensions.keys()
        cog_name = ', '.join(cogs)
        await ctx.respond(f"{ctx.author.mention} Currently loaded cogs: **`{cog_name}`**")


def setup(bot):
    bot.add_cog(CogControl(bot))
