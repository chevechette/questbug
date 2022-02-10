# Questbug Bot

# TD : Error handling
# TD : Logging system

import discord
from discord.ext import commands, tasks
import traceback
from datetime import datetime

# from local config
from discordconfig import DISCORD_TOKEN
# list of modules (named cogs) to set up.
# each cog contains commands
inner_cogs = {
    'cogs.reminder',
    'cogs.info'
}

class questBot(commands.Bot):
    def __init__(self):
        questIntents = discord.Intents.default()
        # Intent set for future reading of members
        # and properly answering messages.
        questIntents.members = True
        super().__init__(command_prefix='?', intents=questIntents)

        for cog in inner_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print("Failed to load mode :" + cog)
                traceback.print_exc()

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

    async def on_ready(self):
        print("The QuestBug Bot is ready !")
        for guild in self.guilds:
            print("The QuestBug is connected to " + guild.name)

def main():
    # REMINDER : DISCORD_TOKEN is saved in discordconfig.py
    # which is not included in this repository.
    discordToken = DISCORD_TOKEN
    questBug = questBot()
    questBug.run(discordToken, reconnect=True)

# if questbug.py is launched through command line
# this serves as execution entrypoint.
if __name__ == "__main__":
    main()