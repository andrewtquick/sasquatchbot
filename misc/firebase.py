import os
import firebase_admin
from dotenv import load_dotenv
from misc.utils import Utils
from discord import Member as Member
from discord import Guild as Guild
from firebase_admin import credentials, db

load_dotenv()

cred = credentials.Certificate({
    "type": os.getenv('FIREBASE_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace(r'\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
    })

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
})

class DBConnection():

    def __init__(self):
        self.utils = Utils(self)
        self.db = db.reference()

    # Checking if user exists in db

    def check_user(self, guild, member):
        """
        Check if a member is registered in the Firebase database for a specific guild.

        Args:
            guild (discord.Guild): The guild to check for the member.
            member (discord.Member): The member to check for in the guild.

        Returns:
            bool: True if the member is registered in the database, False otherwise.
        """
        get_user = self.db.child(str(guild.id))
        get_data = get_user.get()

        if 'users' in get_data:
            if str(member.id) in get_data['users']:
                return True
            else:
                return False
        else:
            return False
        
    def update_user(self, guild: Guild, member: Member, args: dict):
        user_ref = db.reference()
        member = user_ref.child(str(guild.id)).child('users').child(str(member.id))
        member.update(args)

    # Getting date member joined server

    def get_date(self, guild, member):
        user_join = self.db.child(str(guild.id)).child('users')
        get_join_date = user_join.get()
        return get_join_date[str(member.id)]['joined_at']

    # Adding new user to db

    def add_new_user(self, guild: str, member: str):
        """
        Adds a new user to the Firebase database for the specified guild.

        Args:
            guild (str): The ID of the guild to add the user to.
            member (str): The member object of the user to add.

        Returns:
            None
        """
        new_user = self.db.child(str(guild.id)).child('users')
        parsed_date = self.utils.parse_date_time(str(member.joined_at))
        member_roles = [role.name for role in member.roles]
        new_user.update({
            str(member.id): {
                'member': str(member),
                'member_id': str(member.id),
                'member_name': str(member.name),
                'display_name': str(member.display_name),
                'joined_at': parsed_date,
                'roles': member_roles
            }})

    # Checking if guild exists

    def check_guild(self, guild: str):
        get_guild = self.db.child(str(guild))
        get_data = get_guild.get()

        if get_data == None:
            return False
        else:
            return True

    # Gets specified channel

    def get_channel(self, chan_type: str, guild: int):
        """
        Retrieves the specified channel from the Firebase database.

        Args:
            chan_type (str): The type of channel to get (e.g. 'mod' or 'announce').
            guild (int): The ID of the guild to retrieve the channel from.

        Returns:
            The specified channel if it exists, False otherwise.
        """
        try:
            channel = self.db.child(str(guild)).child('channels').child(chan_type).get()
            if channel:
                return channel
        except Exception:
            return False
        
    # Sets specified channel

    def set_channel(self, chan_type: str, guild: int, channel_id: int):
        """
        Sets the specified channel for the given guild and channel type in the Firebase database.

        Args:
            chan_type (str): The type of channel to set (e.g. 'mod' or 'announce').
            guild (int): The ID of the guild to set the channel for.
            channel_id (int): The ID of the channel to set.

        Returns:
            bool: True if the channel was successfully set, False otherwise.
        """
        try:
            channel_ref = self.db.child(str(guild)).child('channels')
            channel_ref.update({ chan_type: channel_id })
            return True
        except Exception:
            return False