import discord
import os
from discord.ext import commands

bot = commands.Bot(
    intents=discord.Intents().all(),
    help_command=None)

exts = [
    # 'cogs.admin.admin',
    'cogs.events.events',
    'cogs.errors.error_handler',
    'cogs.general.loadcog',
    'cogs.general.misc',
    'cogs.channel.channels',
]

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)

    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)
