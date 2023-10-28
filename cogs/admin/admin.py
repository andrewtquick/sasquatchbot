import discord
import os
import discord.utils
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context, BadArgument, CommandError
from misc.firebase import DBConnection
from misc.utils import Utils
from firebase_admin import db

class AdminControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OFFICER_CHANNEL = os.getenv('OFFICER_CHANNEL')
        self.ANNOUNCE_CHAN = os.getenv('ANNOUNCE_CHAN')
        self.AMONG_US_CHAN = os.getenv('AMOUNG_US_CHAN')
        self.utils = Utils(self)
        self.ecdb = DBConnection()

    # Kick Command

    @Command(
        name='kick',
        aliases=['k'],
        help='Kick a user from the server',
        usage='<user name> or <user id>')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: Context, member: Member):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.kick()

    @kick.error
    async def kick_error(self, ctx: Context, error: str):
        
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)

    # Ban command

    @Command(
        name='ban',
        aliases=['b'],
        help='Ban a user from the server',
        usage='<user name> [reason] or <user id> [reason]')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: Context, member: Member, *, reason='No reason given.'):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx: Context, error: str):
        
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)

    # Mute Command

    @Command(
        name='mute',
        aliases=['m'],
        help='Mute a user',
        usage='<user name> or <user id>')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx: Context, member: Member):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.edit(mute=True)

    @mute.error
    async def ban_error(self, ctx: Context, error: str):
        
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)

    #Unmute Command

    @Command(
        name='unmute',
        aliases=['um'],
        help='Unmute a user',
        usage='<user name> or <user id>')
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx: Context, member: Member):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.edit(mute=False)

    @unmute.error
    async def ban_error(self, ctx: Context, error: str):
        
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)

    # Mute All Command

    @Command(
        name='muteall',
        aliases=['ma'],
        help='Mute all users in a specific voice channel',
        usage='<channel name> or <channel id>')
    @commands.has_permissions(administrator=True)
    async def mute_all(self, ctx: Context, chan):
        check_chan = self.utils.channel_parse(chan)

        if check_chan:
            chan_id = self.bot.get_channel(int(chan))

            if len(chan_id.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in chan_id.members:
                    await member.edit(mute=True)

        if check_chan == False:
            get_channel = discord.utils.get(self.bot.get_all_channels(), name=chan, type=discord.ChannelType.voice)

            if len(get_channel.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in get_channel.members:
                    await member.edit(mute=True)
        
    @mute_all.error
    async def muteall_error(self, ctx: Context, error: str):
        if isinstance(error, CommandError):
            await ctx.send(f"{ctx.author.mention} -> I don't recognize that channel. Please specify a voice channel name or double check the spelling.")

    # Un-Mute All Command

    @Command(
        name='unmuteall',
        aliases=['uma'],
        help="Unmute all users in a specific voice channel",
        usage="<channel name> or <channel id>")
    @commands.has_permissions(administrator=True)
    async def unmute_all(self, ctx: Context, chan=None):
        check_chan = self.utils.channel_parse(chan)

        if check_chan:
            chan_id = self.bot.get_channel(int(chan))

            if len(chan_id.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in chan_id.members:
                    await member.edit(mute=False)

        if check_chan == False:
            get_channel = discord.utils.get(self.bot.get_all_channels(), name=chan, type=discord.ChannelType.voice)

            if len(get_channel.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in get_channel.members:
                    await member.edit(mute=False)

    @unmute_all.error
    async def unmuteall_error(self, ctx: Context, error: str):
        if isinstance(error, CommandError):
            await ctx.send(f"{ctx.author.mention} -> I don't recognize that channel. Please specify a voice channel name or double check the spelling.")

    # Squelch Command

    @Command(
        name='squelch',
        aliases=['s'],
        help='Squelch all users in a specific voice channel',
        usage="<channel name> or <channel id>")
    @commands.has_permissions(administrator=True)
    async def squelch(self, ctx: Context, chan=None):
        check_chan = self.utils.channel_parse(chan)

        if check_chan:
            chan_id = self.bot.get_channel(int(chan))

            if len(chan_id.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in chan_id.members:
                    await member.edit(mute=False)

        if check_chan == False:
            get_channel = discord.utils.get(self.bot.get_all_channels(), name=chan, type=discord.ChannelType.voice)

            if len(get_channel.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in get_channel.members:
                    await member.edit(mute=True, deafen=True)

    @squelch.error
    async def squelch_error(self, ctx: Context, error: str):
        if isinstance(error, CommandError):
            await ctx.send(f"{ctx.author.mention} -> I don't recognize that channel. Please specify a voice channel name or double check the spelling.")

    # Unsquelch Command

    @Command(
        name='unsquelch',
        aliases=['us'],
        help='Unsquelch all users in a specific voice channel',
        usage="<channel name> or <channel id>")
    @commands.has_permissions(administrator=True)
    async def unsquelch(self, ctx: Context, chan=None):
        check_chan = self.utils.channel_parse(chan)

        if check_chan:
            chan_id = self.bot.get_channel(int(chan))

            if len(chan_id.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in chan_id.members:
                    await member.edit(mute=False)

        if check_chan == False:
            get_channel = discord.utils.get(self.bot.get_all_channels(), name=chan, type=discord.ChannelType.voice)

            if len(get_channel.members) == 0:
                await ctx.send(f"{ctx.author.mention} -> There are no connected users in {chan}.")
            else:
                for member in get_channel.members:
                    await member.edit(mute=False)

    @unsquelch.error
    async def unsquelch_error(self, ctx: Context, error: str):
        if isinstance(error, CommandError):
            await ctx.send(f"{ctx.author.mention} -> I don't recognize that channel. Please specify a voice channel name or double check the spelling.")

    # Deafen Command

    @Command(
        name='deafen',
        aliases=['d'],
        help='Deafen a user in any voice channel',
        usage='<user name> or <user id>')
    @commands.has_permissions(administrator=True)
    async def deafen(self, ctx: Context, member: Member):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.edit(mute=True)

    @deafen.error
    async def deafen_error(self, ctx: Context, error: str):
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)

    # Undeafen Command

    @Command(
        name='undeafen',
        aliases=['ud'],
        help='Undeafen a user in any voice channel',
        usage='<user name> or <user id>')
    @commands.has_permissions(administrator=True)
    async def undeafen(self, ctx: Context, member: Member):
        user = self.bot.get_guild(int(ctx.guild.id)).get_member_named(member.name)
        await user.edit(mute=False)

    @undeafen.error
    async def undeafen_error(self, ctx: Context, error: str):
        if isinstance(error, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that user. Please double check the spelling.", delete_after=20)
 
    # Announcement Command

    @Command(
        name='announce',
        aliases=['a'],
        help='Send an announcement to the announcement channel',
        usage='<message>')
    @commands.has_permissions(administrator=True)
    async def announce(self, *, msg: str):
        announce_chan = self.bot.get_channel(int(self.ANNOUNCE_CHAN))
        await announce_chan.send(msg)

    # Whois command

    @Command(
        name='whois',
        help='Displays information about a user',
        usage='<user>')
    @commands.has_permissions(administrator=True)
    async def whois(self, ctx: Context, member: Member):
        user_ref = db.reference().child(str(member.guild.id)).child('users')
        user_check = user_ref.child(str(member.id))
        ret_data = user_check.get()
        nicknames = []

        embed = discord.Embed(
            title=f'Whois information for {member.display_name}',
            description=f'Here is all the information I found for **{member.display_name}**',
            colour=discord.Colour.orange())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Member', value=ret_data['member'], inline=False)
        embed.add_field(name='ID', value=ret_data['member_id'], inline=False)
        embed.add_field(name='Member Name', value=ret_data['member_name'], inline=False)
        embed.add_field(name='Display Name', value=ret_data['display_name'], inline=False)
        embed.add_field(name='Joined Date', value=ret_data['joined_at'], inline=False)

        if 'nickname' in ret_data:
            for k,v in ret_data.items():
                if k == 'nickname':
                    nicknames.append(v)
            embed.add_field(name='Nicknames', value=', '.join(name for name in nicknames), inline=False)

        if 'self_leave' in ret_data:
            left_date = self.utils.parse_date_time(str(ret_data['left']))
            embed.add_field(name='Date and time user left', value=left_date)

        if 'ban_reason' in ret_data:
            reason = ret_data['ban_reason']
            ban_ts = ret_data['ban_timestamp']
            embed.add_field(name='User is banned', value=f'Reason: {reason}')
            embed.add_field(name='Timestamp', value=f'Reason: {ban_ts}')

        await ctx.send(f'{ctx.author.mention}', embed=embed)

def setup(bot):
    bot.add_cog(AdminControl(bot))