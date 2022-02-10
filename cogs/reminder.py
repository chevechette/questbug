from discord.ext import commands, tasks
from datetime import date, time, datetime, timedelta
import traceback
import asyncio

CODE_ROLEID = "<@&940176217896812544>"

MSG_QUESTREMIND = "{} !\nIl est {} HEURES ! Tout va BIEN ! ... Si vous avez déjà Quest aujourd'hui du moins.\n"
MSG_QUESTREMIND += "Le code d'aujourd'hui est **{}** ! Allez vous émmarger sur http://quest.ajc.didierr.odns.fr/"
MSG_QUESTCODE = "{}!\nLe code d'aujourd'hui est {} ! Allez vous émmarger sur http://quest.ajc.didierr.odns.fr/"
MSG_ALIVE = "https://media0.giphy.com/media/YEL7FJP6ed008/giphy.gif?cid=ecf05e47u10m4ufjbala1sc4k758gopnb7tihj8vit26aefz&rid=giphy.gif&ct=g"

ERR_IDK = "https://media2.giphy.com/media/LOQJOHXx1mozCccfev/giphy.gif?cid=ecf05e47sw7v0984sua5uietrnjfzyu0n92b1c54ircp4qb1&rid=giphy.gif&ct=g"

questChannel = 940186747638251520
questChannel = 940625405742841866

questFirstDay = date(2022, 2, 7)
questModuleDuration = [
    [date(2022, 2, 7), date(2022, 2, 7), 2925],
    [date(2022, 2, 8), date(2022, 2, 9), 1463],
    [date(2022, 2, 10), date(2022, 2, 10), 9262],
    [date(2022, 2, 11), date(2022, 2, 16), 2206],
    [date(2022, 2, 17), date(2022, 2, 21), 4611],
    [date(2022, 2, 22), date(2022, 2, 22), 9376],
    [date(2022, 2, 23), date(2022, 2, 23), 7902],
    [date(2022, 2, 24), date(2022, 2, 25), 7758],
    [date(2022, 2, 28), date(2022, 2, 28), 6647],

    [date(2022, 3, 1), date(2022, 3, 4), 8960],
    [date(2022, 3, 7), date(2022, 3,11), 8843],
    [date(2022, 3, 14), date(2022, 3, 15), 2620],
    [date(2022, 3, 16), date(2022, 3, 16), 8136],
    [date(2022, 3, 17), date(2022, 3, 17), 1834],
    [date(2022, 3, 18), date(2022, 3, 18), 9403],
    [date(2022, 3, 21), date(2022, 3, 23), 2298],
    [date(2022, 3, 24), date(2022, 3, 25), 7223],
    [date(2022, 3, 28), date(2022, 3, 28), 7921],
    [date(2022, 3, 29), date(2022, 3, 29), 5038],
    [date(2022, 3, 30), date(2022, 4, 1), 4689],

    [date(2022, 4, 4), date(2022, 4, 6), 1551],
    [date(2022, 4, 7), date(2022, 4, 7), 2200],
    [date(2022, 4, 8), date(2022, 4, 11), 9258],
    [date(2022, 4, 12), date(2022, 4, 15), 7920],
    [date(2022, 4, 19), date(2022, 4, 19), 2196],
    [date(2022, 4, 20), date(2022, 4, 20), 9450],
    [date(2022, 4, 21), date(2022, 4, 27), 2319],
]

class ReminderCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.remindQuest.start()
        print(self.remindQuest.next_iteration)

    def cog_unload(self):
        self.remindQuest.cancel()

    @staticmethod
    def getModuleCode():
        todayDay = date.today()
        for questmodule in questModuleDuration:
            if (todayDay >= questmodule[0] and todayDay <= questmodule[1]):
                print("Today's code is actually {} ".format(questmodule[2]))
                return questmodule[2]
        return 0000
    
    @staticmethod
    def secondsUtilTime(hours, minutes=0, seconds=0):
        #To Upgrade ?
        currentDatetime = datetime.now()
        nextTime = time(hours, minutes, seconds)
        isTommorow = 1 if (currentDatetime.time() > nextTime) else 0
        futureExec = datetime.combine(currentDatetime + timedelta(days=isTommorow), nextTime)
        return ((futureExec - currentDatetime).total_seconds())

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send("Yes, I am online!")

    @commands.command()
    async def currentQuest(self, ctx):
        try:
            todaysCode = ReminderCog.getModuleCode()
            msg = ERR_IDK if todaysCode == 0000 else MSG_QUESTCODE.format(CODE_ROLEID, todaysCode)
            print(msg)
            await ctx.channel.send(msg)
        except Exception as e:
            traceback.print_exc()
            await ctx.channel.send(ERR_IDK)

    async def sendRemindQuest(self):
        currentHour = datetime.now().hour
        #await self.bot.get_channel(questChannel).send(MSG_ALIVE)
        await self.bot.get_channel(questChannel).send(MSG_QUESTREMIND.format(
            CODE_ROLEID, currentHour, ReminderCog.getModuleCode()
            ))

    @tasks.loop(hours=1)
    async def remindQuest(self):
        print("ACTIVATE MY TRAP CARD")
        # Add a dismissal to avoid double message ?
        currentDT = datetime.now()
        print(ReminderCog.getModuleCode())
        if (currentDT.hour == 9 and currentDT.minute < 30):
            print("Good morning America !")
            await asyncio.sleep(self.secondsUtilTime(9, 30))
            print(datetime.now())
            await self.sendRemindQuest()
        elif (currentDT.hour == 13) :
            print("The eleventh hour")
            await asyncio.sleep(self.secondsUtilTime(14, 00))
            print(datetime.now())
            await self.sendRemindQuest()
        else:
            print("Try later")

def setup(bot):
    bot.add_cog(ReminderCog(bot))