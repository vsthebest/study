import discord
import asyncio
import random
import os
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

'''
배그: *팀짜기, 티어보기
롤  : 포지션정하기, 티어보기 
'''

load_dotenv()
token = os.getenv('BOT_TOKKEN')

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

## 통합스탯, arg1: 이름 ##
@bot.command(aliases=["스탯"])
async def stats(ctx, arg1):
    platform = "kakao"
    playerID = os.getenv('EY_KAKAO')
    name = "IDC_Kakabenzema"
    
    url = "https://api.pubg.com/shards/kakao/seasons"
    header = { "Authorization": os.getenv('AUTHORIZATION'),
              "Accept": "application/vnd.api+json" }
    
    req = requests.get(url, headers=header)
    json_season = json.loads(req.text)

    for i in range(len(json_season['data'])):
        if json_season['data'][i]['attributes']['isCurrentSeason'] == True and json_season['data'][i]['attributes']['isOffseason'] == False:
            seasonID = json_season['data'][i]['id']
            break
    
    url = "https://api.pubg.com/shards/"+platform+"/players/"+playerID+"/seasons/"+seasonID+"/ranked"
    req = requests.get(url, headers=header)
    json_rank = json.loads(req.text)

    tier = json_rank['data']['attributes']['rankedGameModeStats']['squad']['currentTier']['tier']
    subtier = json_rank['data']['attributes']['rankedGameModeStats']['squad']['currentTier']['subTier']
    point = json_rank['data']['attributes']['rankedGameModeStats']['squad']['currentRankPoint']
    
    KDA = json_rank['data']['attributes']['rankedGameModeStats']['squad']['kda']
    rank_games = json_rank['data']['attributes']['rankedGameModeStats']['squad']['roundsPlayed']
    rank_Dealt = json_rank['data']['attributes']['rankedGameModeStats']['squad']['damageDealt']
    rank_kills = json_rank['data']['attributes']['rankedGameModeStats']['squad']['kills']
    rank_assist = json_rank['data']['attributes']['rankedGameModeStats']['squad']['assists']
    rank_chicken = json_rank['data']['attributes']['rankedGameModeStats']['squad']['wins']
    rank_top10s = round(json_rank['data']['attributes']['rankedGameModeStats']['squad']['top10Ratio'] * rank_games)


    ## 이번시즌 일반 종합 ##
    url = "https://api.pubg.com/shards/"+platform+"/players/"+playerID+"/seasons/"+seasonID
    req = requests.get(url, headers=header)
    json_normal = json.loads(req.text)

    normal_games = json_normal['data']['attributes']['gameModeStats']['squad']['roundsPlayed']
    normal_dealt = json_normal['data']['attributes']['gameModeStats']['squad']['damageDealt']
    normal_kills = json_normal['data']['attributes']['gameModeStats']['squad']['kills']
    normal_assist = json_normal['data']['attributes']['gameModeStats']['squad']['assists']
    normal_chicken = json_normal['data']['attributes']['gameModeStats']['squad']['wins']
    normal_top10s = json_normal['data']['attributes']['gameModeStats']['squad']['top10s']
    
    total_games = rank_games + normal_games
    total_dealt = round((rank_Dealt + normal_dealt) / total_games)
    total_kills = round((rank_kills + normal_kills) / total_games, 1)
    total_assist = round((rank_assist + normal_assist) / total_games, 1)
    total_chicken = rank_chicken + normal_chicken
    total_top10s = round((rank_top10s + normal_top10s) / total_games * 100)
    
    background = Image.open("back.jpg").convert("RGBA")
    txt = Image.new("RGBA", background.size, (255,255,255,0))
   
    draw1 = ImageDraw.Draw(txt)
    draw1.text((220,18), name, font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))

    tier_img = Image.open(tier+subtier+".png").convert("RGBA")
    tier_img = tier_img.resize((70,70))

    
    draw2 = ImageDraw.Draw(txt)
    draw2.text((270,55), str(point)+"point", font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    draw3 = ImageDraw.Draw(txt)
    draw3.text((130, 107), str(round(KDA,1)), font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    draw4 = ImageDraw.Draw(txt)
    draw4.text((100, 160), str(total_dealt), font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    draw5 = ImageDraw.Draw(txt)
    draw5.text((110, 215), str(total_top10s)+"%", font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    draw6 = ImageDraw.Draw(txt)
    draw6.text((360, 120), str(total_chicken)+"번", font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    draw7 = ImageDraw.Draw(txt)
    draw7.text((375, 162), str(total_kills)+"회", font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))

    draw8 = ImageDraw.Draw(txt)
    draw8.text((420, 202), str(total_assist)+"회", font=ImageFont.truetype("HMKMMAG.TTF", 16), fill=(255,255,255))
    
    out = Image.alpha_composite(background, txt)
    out.paste(tier_img, (200,30), tier_img)
    
    await ctx.send(out)
    
bot.run(token)
