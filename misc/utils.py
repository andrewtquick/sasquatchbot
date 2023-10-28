import time
import pytz
from discord import Role
from datetime import datetime as dt


class Utils(object):

    def __init__(self, object):
        self.utils = object
        self.tz = pytz.timezone('America/New_York')

    # Parsing Input to readable format

    def parse_date_time(self, date_time):
        entry = str(date_time)
        parsed_entry = time.strptime(entry.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parsed_entry = time.strftime('%m-%d-%Y %I:%M %p', parsed_entry)
        return parsed_entry

    # Getting date and time and parsing for output

    def get_date_time_parsed(self):
        now = str(dt.now(self.tz))
        parse_now = time.strptime(now.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parse_now = time.strftime('%m-%d-%Y %I:%M %p', parse_now)
        return parse_now

    def get_time_parsed(self):
        now = str(dt.now(self.tz))
        parse_now = time.strptime(now.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parse_now = time.strftime('%I:%M %p', parse_now)
        return parse_now

    def get_date_parsed(self):
        now = str(dt.now(self.tz))
        parse_now = time.strptime(now.split('.')[0], '%Y-%m-%d %H:%M:%S')
        parse_now = time.strftime('%Y-%m-%d', parse_now)
        return parse_now

    def compare_roles(self, before: Role, after: Role):

        if before.name != after.name:
            return 'name'
        elif before.color != after.color:
            return 'color'
        elif before.colour != after.colour:
            return 'colour'
        elif before.hoist != after.hoist:
            return 'hoist'
        elif before.mentionable != after.mentionable:
            return 'mentionable'
        # elif before.permissions != after.permissions:
        #     return 'permissions'
        else:
            return False

    def channel_parse(self, chan: str):

        try:
            int(chan)
            return True
        except ValueError:
            return False
