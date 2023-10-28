import discord
from random import randint as random
from discord import Embed
from discord import ApplicationContext as Context
from discord.ext import commands
from discord.ext.commands import slash_command as SlashCommand
from misc.utils import Utils


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self)

    @SlashCommand(name='about', description='About the bot.')
    @commands.guild_only()
    async def about(self, ctx: Context):
        embed = Embed(
            title='About Sasquatch',
            description='Sasquatch is a Discord bot created by @Xylr',
            colour=discord.Colour.blue()
        )
        embed.add_field(name='Version', value='1.0.0', inline=False)
        embed.add_field(name='Author', value='@Xylr', inline=False)
        embed.add_field(name="Language", value='Python v3.11.5', inline=False)
        embed.add_field(name='Library', value='py-cord v2.4.1', inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
