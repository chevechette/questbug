# Questbug Bot

# TD : export config (token) to different file

# TD : Message standard
# TD : Charger tous event
# TD : Error handling
# TD : Add cog to ask for linl
# TD : gitignore
# TD : Logging system

# Project deadlines

import discord
from discord.ext import commands, tasks
from discordconfig import DISCORD_TOKEN
import traceback
from datetime import datetime

inner_cogs = {
    'cogs.reminder'
}

class questBot(commands.Bot):
    def __init__(self):
        questIntents = discord.Intents.default()
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

            
    def toutVaBien():
        message = "Il est {} ! Tout va BIEN @everyone !\n Le code d'aujourd'hui est {} ! Allez vous émmarger sur http://quest.ajc.didierr.odns.fr/"
        message = message.format(datetime.now(), 1234)
        print(message)

    # @tasks.loop(seconds=5.0)
    # async def printer(self):
        # toutVaBien()

def main():
    discordToken = DISCORD_TOKEN
    questBug = questBot()
    questBug.run(discordToken, reconnect=True)

if __name__ == "__main__":
    print("Let's work !")
    main()