import discord
from misc.firebase import DBConnection
from misc.utils import Utils
from datetime import datetime as dt
from discord import Member, Guild, User, Message
from discord.ext import commands
from discord import Embed


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = DBConnection()
        self.utils = Utils(self)

    # On Ready

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} online.')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Eve Online'))

        for guild in self.bot.guilds:
            if self.db.get_channel('mod', guild.id) == None:
                await guild.owner.send(
                    f'Please use the `/setmodchannel` command on your server, `{guild.name}`, to set a mod channel for events to be sent to.')

            # if self.db.get_channel('announce', guild.id) == None:
            #     await guild.owner.send(
            #         f'Please use the `/setannouncechannel` command on your server, `{guild.name}`, to send announcements to your server.')

        self.gather_all_members()

    # On Member Leave, Kick, and Ban

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', member.guild.id))

        embed = Embed(
            title=f':cry: Member left the server.',
            description=f'{member.mention} has left.',
            colour=discord.Colour.red())
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(
            text=f'User ID: {member.id} | {self.utils.parse_date_time(dt.now())}')

        self.db.update_user(member.guild, member, {
                            'left': self.utils.parse_date_time(dt.now())})
        await mod_channel.send(embed=embed)

     # On Member Unban

    @commands.Cog.listener()
    async def on_member_unban(self, guild: Guild, user: User):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', guild.id))

        embed = Embed(
            title=f':eyes: Member was unbanned.',
            description=f'{user.display_name} was unbanned from the server.',
            colour=discord.Colour.yellow())
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(
            text=f'User ID: {user.id} | {self.utils.parse_date_time(dt.now())}')

        async for _ in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            await mod_channel.send(embed=embed)

    # On Member Join Message

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', member.guild.id))

        embed = Embed(
            title=f':star_struck: Member has joined the server.',
            description=f'{member.mention} has joined the server.',
            colour=discord.Colour.green())
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(
            text=f'User ID: {member.id} | {self.utils.parse_date_time(dt.now())}')

        self.db.add_new_user(member.guild, member)
        await mod_channel.send(embed=embed)

    # Member Nickname Change Notifier

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', after.guild.id))
        guild = self.bot.get_guild(int(after.guild.id))

        if before.nick != after.nick:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if before.name != entry.user.name:
                    if entry.user.name != self.bot.user.name:
                        embed = Embed(
                            title=":eyes: Member's name was changed.",
                            description=f"{entry.user.mention} changed `{before.display_name}`'s name to {after.mention}.",
                            colour=discord.Colour.green())
                        embed.set_thumbnail(url=after.display_avatar)
                        embed.set_footer(
                            text=f'User ID: {after.id} | {self.utils.parse_date_time(dt.now())}')
                        await mod_channel.send(embed=embed)
                else:
                    embed = Embed(
                        title=":eyes: Member changed their name.",
                        description=f"{before.display_name} changed their name to {after.mention}.",
                        colour=discord.Colour.green())
                    embed.set_thumbnail(url=after.display_avatar)
                    embed.set_footer(
                        text=f'User ID: {after.id} | {self.utils.parse_date_time(dt.now())}')
                    await mod_channel.send(embed=embed)

    # Guild Role Create Notifier

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', role.guild.id))

        embed = Embed(
            title=f':eyes: Role was created.',
            description=f'`{role.name}` was created.',
            colour=discord.Colour.red())
        embed.set_footer(
            text=f'Role ID: {role.id} | {self.utils.parse_date_time(dt.now())}')

        await mod_channel.send(embed=embed)

    # Guild Role Delete Notifier

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', role.guild.id))

        embed = Embed(
            title=f':eyes: Role was deleted.',
            description=f'`{role.name}` was deleted.',
            colour=discord.Colour.red())
        embed.set_footer(
            text=f'Role ID: {role.id} | {self.utils.parse_date_time(dt.now())}')

        await mod_channel.send(embed=embed)

    # Guild Role Update Notifier

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', after.guild.id))

        embed = Embed(
            title=f':eyes: Role was modified.',
            description=f'Role `{after.name}` was modified.',
            colour=discord.Colour.yellow())
        if self.utils.compare_roles(before, after) == 'name':
            embed.add_field(
                name='Name', value=f'`{before.name}` -> `{after.name}`')
        elif self.utils.compare_roles(before, after) == 'color':
            embed.add_field(
                name='Color', value=f'[{before.colour}](https://www.color-hex.com/color/{before.colour}) -> [{after.colour}](https://www.color-hex.com/color/{after.colour})')
        elif self.utils.compare_roles(before, after) == 'colour':
            embed.add_field(
                name='Colour', value=f'[{before.colour}](https://www.color-hex.com/color/{before.colour}) -> [{after.colour}](https://www.color-hex.com/color/{after.colour})')
        elif self.utils.compare_roles(before, after) == 'hoist':
            embed.add_field(
                name='Hoist', value=f'`{before.hoist}` -> `{after.hoist}`')
        elif self.utils.compare_roles(before, after) == 'mentionable':
            embed.add_field(
                name='Mentionable', value=f'`{before.mentionable}` -> `{after.mentionable}`')
        # elif self.utils.compare_roles(before, after) == 'permissions':
        #     embed.add_field(
        #         name='Permissions', value=f'`{before.permissions}` -> `{after.permissions}`')
        embed.set_footer(
            text=f'Role ID: {after.id} | {self.utils.parse_date_time(dt.now())}')

        await mod_channel.send(embed=embed)

    # Message Delete Notifier

    async def on_message_delete(self, message: Message):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', message.guild.id))

        if message.author != self.bot:
            embed = Embed(
                title=f':eyes: Message was deleted.',
                description=f'Message from {message.author.mention} was deleted.',
                colour=discord.Colour.red())
            embed.add_field(name='Message', value=message.content)
            embed.set_footer(
                text=f'Message ID: {message.id} | {self.utils.parse_date_time(dt.now())}')

            await mod_channel.send(embed=embed)

    # Message Edit Notifier

    async def on_message_edit(self, before: Message, after: Message):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', after.guild.id))

        if before.author != self.bot:
            embed = Embed(
                title=f':eyes: Message was edited.',
                description=f'Message from {before.author.mention} was edited.',
                colour=discord.Colour.yellow())
            embed.add_field(name='Before', value=before.content)
            embed.add_field(name='After', value=after.content)
            embed.set_footer(
                text=f'Message ID: {after.id} | {self.utils.parse_date_time(dt.now())}')

            await mod_channel.send(embed=embed)

    # User Update Notifier

    async def on_user_update(self, before: User, after: User):
        mod_channel = self.bot.get_channel(
            self.db.get_channel('mod', after.guild.id))

        if before.username != after.username:
            embed = Embed(
                title=f':eyes: User changed their name.',
                description=f'{before.display_name} changed their name to {after.mention}.',
                colour=discord.Colour.green())
            embed.set_thumbnail(url=after.display_avatar)
            embed.set_footer(
                text=f'User ID: {after.id} | {self.utils.parse_date_time(dt.now())}')
            await mod_channel.send(embed=embed)

        if before.avatar != after.avatar:
            embed = Embed(
                title=f':eyes: User changed their avatar.',
                description=f'{after.mention} changed their avatar.',
                colour=discord.Colour.green())
            embed.set_thumbnail(url=after.display_avatar)
            embed.set_footer(
                text=f'User ID: {after.id} | {self.utils.parse_date_time(dt.now())}')
            await mod_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(
                title=f':eyes: User changed their discriminator.',
                description=f'{after.mention} changed their discriminator.',
                colour=discord.Colour.green())
            embed.set_thumbnail(url=after.display_avatar)
            embed.set_footer(
                text=f'User ID: {after.id} | {self.utils.parse_date_time(dt.now())}')
            await mod_channel.send(embed=embed)

    # Gathering all user information on ready

    def gather_all_members(self):
        guilds = self.bot.guilds

        for guild in guilds:
            check_guild = self.db.check_guild(guild.id)
            if check_guild:
                for member in guild.members:
                    user_check = self.db.check_user(guild, member)
                    if user_check == False:
                        self.db.add_new_user(guild, member)
            else:
                for member in guild.members:
                    self.db.add_new_user(guild, member)


def setup(bot):
    bot.add_cog(Events(bot))
