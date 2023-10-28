import discord
import discord.utils
from discord import ApplicationContext as Context
from discord.ext import commands
from discord.ext.commands import slash_command as SlashCommand
from misc.firebase import DBConnection
from misc.utils import Utils


class ChannelAdmin(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.db = DBConnection()
        self.utils = Utils(self)

    # Set mod channel command

    @SlashCommand(name='setmodchannel', description='**ADMIN** Set channel for mod event information.')
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    async def set_mod_channel(self, ctx: Context, channel: discord.TextChannel):

        set_channel = self.db.set_channel('mod', ctx.guild_id, channel.id)

        if set_channel:
            await ctx.respond('Done.', delete_after=0)
            await ctx.user.send(f'{ctx.author.mention} -> I have set {channel.mention} as the mod channel.')
        else:
            await ctx.respond('Error.', delete_after=0)
            await ctx.user.send(f'{ctx.author.mention} -> I\'m unable to find that text channel. Please double check the spelling or channel id.')

    # Set announcement channel command

    # @SlashCommand(name='setannouncechannel', description='**ADMIN** Set channel for announcements.')
    # @discord.default_permissions(administrator=True)
    # @commands.guild_only()
    # async def set_announce_channel(self, ctx: Context, channel: discord.TextChannel):

    #     set_channel = self.db.set_channel('announce', ctx.guild_id, channel.id)

    #     if set_channel:
    #         await ctx.respond(f'{ctx.author.mention} -> I have set {channel.mention} as the announcement channel.')
    #     else:
    #         await ctx.respond(f'{ctx.author.mention} -> I\'m unable to find that text channel. Please double check the spelling or channel id.')


def setup(bot):
    bot.add_cog(ChannelAdmin(bot))
