import discord
import asyncio
import random
from discord.ext import commands

'''
배그: *팀짜기, 티어보기
롤  : 포지션정하기, 티어보기 
'''

token = "OTQ2NjM1OTIyNjg5MTE0MjEy.YhhlZw.k1tNTJa7875rhVOkbXMle3ua1PY"

comment = discord.Game("!명령어 - 명령어확인")
bot = commands.Bot(command_prefix="!", status=discord.Status.online, activity=comment)






## 명령어 리스트 출력 ##
@bot.command(aliases=["명령어"])
async def orders(ctx):
    await ctx.send("!팀짜기, !team :: 5명이상일때 배그 팀나누기 4/3 or 3/3 or 3/2")
    
################################################################################################

## 배그 팀짜기 ##
@bot.command(aliases=["팀짜기"])
async def team(ctx):
    channel = bot.get_channel(946638295302029326)
    curMembers = []
    team_one = []
    team_two = []
    

    for member in channel.members:
        one = str(member)
        curMembers.append(one)


    if len(curMembers) < 5:
        await ctx.send("총 인원: "+str(len(curMembers))+"명, ["+ ' '.join(curMembers)+"]")
        await ctx.send("팀을 나눌 충분한 인원이 되지 않습니다")

    else:
        await ctx.send("총 인원: "+str(len(curMembers))+"명, ["+ ' '.join(curMembers)+"]")
        
        if len(curMembers) == 7:
            team_one_size = 4    
        else:
            team_one_size = 3
            
        team_two_size = len(curMembers) - team_one_size

        for i in range(team_one_size):
            member = random.choice(curMembers)
            curMembers.remove(member)

            team_one.append(member)

        team_two = curMembers

        
        await ctx.send("첫번째팀: "+' '.join(team_one) + ", 두번째팀: "+' '.join(team_two))

####################################################################################################




bot.run(token)
