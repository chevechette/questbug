from operator import truediv
from discord.ext import commands, tasks
from datetime import date, time, datetime, timedelta
import traceback
import asyncio
import bugmsgs, questdata

CODE_ROLEID = "<@&940176217896812544>"

questChannel = 940625405742841866
questChannel = 940186747638251520

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
        for questmodule in questdata.QUEST_MOD_DURATION:
            if (todayDay >= questmodule[0] and todayDay <= questmodule[1]):
                print("Today's code is actually {} ".format(questmodule[2]))
                return questmodule[2]
        return 0000

    @staticmethod
    def isevaluationDay():
        todayDay = date.today()
        for questmodule in questdata.QUEST_MOD_DURATION:
            if (todayDay == questmodule[1]):
                return True
        return False
    
    @staticmethod
    def secondsUtilTime(hours, minutes=0, seconds=0):
        #To Upgrade ?
        currentDatetime = datetime.now()
        nextTime = time(hours, minutes, seconds)
        isTommorow = 1 if (currentDatetime.time() > nextTime) else 0
        futureExec = datetime.combine(currentDatetime + timedelta(days=isTommorow), nextTime)
        return ((futureExec - currentDatetime).total_seconds())
    
    @commands.command()
    async def evalDay(self, ctx):
        try:
            msg = bugmsgs.MSG_EVAL_Y if ReminderCog.isevaluationDay() else bugmsgs.MSG_EVAL_N
            await ctx.channel.send(msg)
        except Exception as e:
            traceback.print_exc()
            await ctx.channel.send(bugmsgs.ERR_IDK)

    @commands.command()
    async def currentQuest(self, ctx):
        try:
            todaysCode = ReminderCog.getModuleCode()
            msg = bugmsgs.ERR_IDK if todaysCode == 0000 else bugmsgs.MSG_QUESTCODE.format(questdata.CODE_ROLEID, todaysCode)
            print(msg)
            if (datetime.today().weekday() >= 5):
                msg = bugmsgs.ERR_NOTTODAY
            await ctx.channel.send(msg)
        except Exception as e:
            traceback.print_exc()
            await ctx.channel.send(bugmsgs.ERR_IDK)

    async def sendRemindQuest(self):
        currentHour = datetime.now().hour
        await self.bot.get_channel(questdata.QUEST_CHANNEL).send(bugmsgs.MSG_QUESTREMIND.format(
            questdata.CODE_ROLEID, currentHour, ReminderCog.getModuleCode()
            ))

    @tasks.loop(hours=1)
    async def remindQuest(self):
        print("ACTIVATE MY TRAP CARD")
        # Add a dismissal to avoid double message ?
        currentDT = datetime.now()
        weekday = currentDT.weekday()
        if (weekday >= 5):
            return
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