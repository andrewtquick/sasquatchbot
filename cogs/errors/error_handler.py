import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands import MissingAnyRole, MemberNotFound
from discord.member import Member

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, err):
        if isinstance(err, MissingAnyRole):
            await ctx.send(f'Sorry {ctx.author.mention}, you do not have the permission to perform this command.', delete_after=20)
        if isinstance(err, MemberNotFound):
            await ctx.send(f"Sorry {ctx.author.mention}, I can't find that user. Please double check the spelling.", delete_after=20)

   
def setup(bot):
    bot.add_cog(ErrorHandler(bot))