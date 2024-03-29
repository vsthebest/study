import discord
import asyncio
import random
import os
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

'''
배그: *팀짜기, 티어보기
롤  : 포지션정하기, 티어보기 
'''

load_dotenv()
token = os.getenv('BOT_TOKKEN')

comment = discord.Game("!명령어 - 명령어확인")
bot = commands.Bot(command_prefix="!", status=discord.Status.online, activity=comment)

header = {
    "Authorization": os.getenv('AUTHORIZATION'),
    "Accept": "application/vnd.api+json"
    }




## 명령어 리스트 출력 ##
@bot.command(aliases=["명령어"])
async def orders(ctx):
    await ctx.send("1. !팀짜기, !team :: 5명이상일때 배그 팀나누기 4/3 or 3/3 or 3/2")
    await ctx.send("2. !스탯 [이름] [카카오/스팀], !stat [이름] [카카오/스팀] :: KDA제외 일반+랭 합산")
    await ctx.send("이름: 은영, 익현, 장훈, 동혁, 승민, 태진, 민수")

    
################################################################################################

## 배그 팀짜기 ##
@bot.command(aliases=["팀짜기"])
async def team(ctx):
    channel = bot.get_channel(569069485529628705)
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
async def stats(ctx, arg1, arg2):
    nex = 1
    playerID = ""
    name = ""
    point = 0
    
    total_games = 0
    total_dealt = 0
    total_kills = 0
    total_assist = 0
    total_chicken = 0
    total_top10s = 0
    
    rank_games = 0
    rank_Dealt = 0
    rank_kills = 0
    rank_assist = 0
    rank_chicken = 0
    rank_top10s = 0
    
    tier = ""
    subtier = 0
    KDA = 0.0    
    
    if arg2 == "스팀":
        arg2 = "steam"
        if arg1 == "은영":
            playerID = os.getenv('EY_STEAM')
            name = os.getenv('EY_STEAM_ID')

        elif arg1 == "승민" or arg1 == "오잉":
            playerID = os.getenv('SM_STEAM')
            name = os.getenv('SM_STEAM_ID')

        elif arg1 == "익현" or arg1 == "익돌":
            playerID = os.getenv('IH_STEAM')
            name = os.getenv('IH_STEAM_ID')

        elif arg1 == "민수" or arg1 == "만수":
            playerID = os.getenv('MS_STEAM')
            name = os.getenv('MS_STEAM_ID')

        elif arg1 == "태진" or arg1 == "오크":
            playerID = os.getenv('TJ_STEAM')
            name = os.getenv('TJ_STEAM_ID')

        elif arg1 == "장훈" or arg1 == "쫄":
            playerID = os.getenv('JH_STEAM')
            name = os.getenv('JH_STEAM_ID')

        elif arg1 == "동혁" or arg1 == "댕":
            playerID = os.getenv('DH_STEAM')
            name = os.getenv('DH_STEAM_ID')

        else:
            nex = 0
            
    elif arg2 == "카카오":
        arg2 = "kakao"
        if arg1 == "은영":
            playerID = os.getenv('EY_KAKAO')
            name = os.getenv('EY_KAKAO_ID')

        elif arg1 == "승민" or arg1 == "오잉":
            playerID = os.getenv('SM_KAKAO')
            name = os.getenv('SM_KAKAO_ID')

        elif arg1 == "익현" or arg1 == "익돌":
            playerID = os.getenv('IH_KAKAO')
            name = os.getenv('IH_KAKAO_ID')

        elif arg1 == "민수" or arg1 == "만수":
            playerID = os.getenv('MS_KAKAO')
            name = os.getenv('MS_KAKAO_ID')

        elif arg1 == "태진" or arg1 == "오크":
            playerID = os.getenv('TJ_KAKAO')
            name = os.getenv('TJ_KAKAO_ID')

        elif arg1 == "장훈" or arg1 == "쫄":
            playerID = os.getenv('JH_KAKAO')
            name = os.getenv('JH_KAKAO_ID')

        elif arg1 == "동혁" or arg1 == "댕":
            playerID = os.getenv('DH_KAKAO')
            name = os.getenv('DH_KAKAO_ID')

        else:
            nex = 0
        
    else:
        nex = 0
    
    
    if nex == 1:
        seasonID = os.getenv('season_ID')
        url = "https://api.pubg.com/shards/"+arg2+"/players/"+playerID+"/seasons/"+seasonID+"/ranked"
        req = requests.get(url, headers=header)
        json_rank = json.loads(req.text)

        if 'squad' in json_rank['data']['attributes']['rankedGameModeStats']:
            if point < json_rank['data']['attributes']['rankedGameModeStats']['squad']['currentRankPoint']:
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
        url = "https://api.pubg.com/shards/"+arg2+"/players/"+playerID+"/seasons/"+seasonID
        req = requests.get(url, headers=header)
        json_normal = json.loads(req.text)

        normal_games = json_normal['data']['attributes']['gameModeStats']['squad']['roundsPlayed']
        normal_dealt = json_normal['data']['attributes']['gameModeStats']['squad']['damageDealt']
        normal_kills = json_normal['data']['attributes']['gameModeStats']['squad']['kills']
        normal_assist = json_normal['data']['attributes']['gameModeStats']['squad']['assists']
        normal_chicken = json_normal['data']['attributes']['gameModeStats']['squad']['wins']
        normal_top10s = json_normal['data']['attributes']['gameModeStats']['squad']['top10s']

        total_games = rank_games + normal_games
        total_dealt = rank_Dealt + normal_dealt
        total_kills = rank_kills + normal_kills
        total_assist = rank_assist + normal_assist
        total_chicken = rank_chicken + normal_chicken
        total_top10s = rank_top10s + normal_top10s

        if total_games > 0:
            total_dealt = round((total_dealt) / total_games)
            total_kills = round((total_kills) / total_games, 1)
            total_assist = round((total_assist) / total_games, 1)
            total_top10s = round((total_top10s) / total_games * 100)

        background = Image.open("back.jpg").convert("RGBA")
        txt = Image.new("RGBA", background.size, (255,255,255,0))

        draw1 = ImageDraw.Draw(txt)
        draw1.text((220,18), name+"("+arg1+")", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        if tier != "":
            tier_img = Image.open(tier+subtier+".png").convert("RGBA")
            tier_img = tier_img.resize((70,70))


        draw2 = ImageDraw.Draw(txt)
        draw2.text((270,55), str(point)+"point"+"("+arg2+")", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw3 = ImageDraw.Draw(txt)
        draw3.text((130, 107), str(round(KDA,1)), font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw4 = ImageDraw.Draw(txt)
        draw4.text((100, 160), str(total_dealt), font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw5 = ImageDraw.Draw(txt)
        draw5.text((110, 215), str(total_top10s)+"%", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw6 = ImageDraw.Draw(txt)
        draw6.text((360, 120), str(total_chicken)+"번", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw7 = ImageDraw.Draw(txt)
        draw7.text((375, 162), str(total_kills)+"회", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        draw8 = ImageDraw.Draw(txt)
        draw8.text((420, 202), str(total_assist)+"회", font=ImageFont.truetype("HMKMMAG.TTF", 18), fill=(255,255,255))

        out = Image.alpha_composite(background, txt)
        if tier != "":
            out.paste(tier_img, (200,30), tier_img)

        with BytesIO() as image_binary:
            out.save(image_binary, "png")
            image_binary.seek(0)
            result = discord.File(fp=image_binary, filename="image.png")
            await ctx.send(file=result)
    else:
        await ctx.send("명령어 오류입니다.")
    
bot.run(token)
