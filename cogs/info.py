from discord.ext import commands
import bugmsgs

class InfoCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ?help ping, will show HELP,
    # ?help, will show BRIEF
    @commands.command(
	    help=bugmsgs.HELP_PING,
	    brief=bugmsgs.BRIEF_PING
    )
    async def ping(self, ctx):
        await ctx.channel.send(bugmsgs.MSG_PONG)

def setup(bot):
    bot.add_cog(InfoCog(bot))