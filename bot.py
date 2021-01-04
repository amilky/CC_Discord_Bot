# bot.py
#we import os so we can access environment variables
#class that allows you to interact with the operating system
FORMAT_SYMBOLS = "```"

import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

def calc_skilling(hiscore_list):
    points = 0

    total_level = int(hiscore_list[0][1])
    if total_level < 500:
        points = 0
    elif 500 <= total_level < 750:
        points += 25
    elif 750 <= total_level < 1250:
        points += 50
    elif 1250 <= total_level < 1500:
        ponts += 100
    elif 1500 <= total_level < 1750:
        points += 200
    elif 1750 <= total_level < 2000:
        points += 400
    elif 2000 <= total_level < 2200:
        points += 800
    elif 2200 <= total_level < 2277:
        points += 1600
    elif total_level == 2277:
        points += 2600
    return points

def calc_clue(hiscore_list):
    points = 0

    beginner_clue = int(hiscore_list[28][1])
    easy_clue = int(hiscore_list[29][1])
    medium_clue = int(hiscore_list[30][1])
    hard_clue = int(hiscore_list[31][1])
    elite_clue = int(hiscore_list[32][1])
    master_clue = int(hiscore_list[33][1])

    #print(beginner_clue)
    #print(easy_clue)
    #print(medium_clue)
    #print(hard_clue)
    #print(elite_clue)
    #print(master_clue)

    if beginner_clue > 0:
        points += beginner_clue // 60
    if easy_clue > 0:
        points += easy_clue // 50
    if medium_clue > 0:
        points += medium_clue // 30
    if hard_clue > 0:
        points += hard_clue // 10
    if elite_clue > 0:
        points += elite_clue // 3
    if master_clue > 0:
        points += master_clue // 2

    return points

def calc_raids(hiscore_list):
    points = 0
    cox_kc = int(hiscore_list[41][1])
    cm_cox_kc = int(hiscore_list[42][1])
    tob_kc = int(hiscore_list[69][1])

    #print(cox_kc)
    #print(cm_cox_kc)
    #print(tob_kc)
    if cox_kc > 0:
        points += cox_kc
    if cm_cox_kc > 0:
        points += cm_cox_kc * 3
    if tob_kc > 0:
        points += tob_kc * 2

    return points

def calc_bossing(hiscore_list):
    boss_points = 0

    gwd_dict = {"Commander Zilyana": int(hiscore_list[45][1]), "General Graardor": int(hiscore_list[52][1]),
                "Kree'Arra": int(hiscore_list[59][1]), "K'ril Tsutsaroth": int(hiscore_list[60][1])}

    gwd_points = 0
    for key in gwd_dict:
        #print(gwd_dict[key])
        if gwd_dict[key] > 0:
            #print(gwd_points)
            gwd_points += gwd_dict[key]

    boss_points += gwd_points // 10
    print(boss_points)


    #GROUP A POINTS
    boss_A_dict = {"Abyssal Sire": int(hiscore_list[35][1]),"Alchemical Hydra": int(hiscore_list[36][1]),
                   "Callisto": int(hiscore_list[39][1]), "Cerberus": int(hiscore_list[40][1]), "Venenatis":
                    int(hiscore_list[73][1]), "Vet'ion": int(hiscore_list[74][1]), "Vorkath": int(hiscore_list[75][1]),
                   "Zulrah": int(hiscore_list[78][1])}

    boss_A_points = 0
    for key in boss_A_dict:
        #print(boss_A_dict, "kc", boss_A_dict[key])
        if boss_A_dict[key] > 0:
            boss_A_points += boss_A_dict[key]

    boss_points += boss_A_points // 30

    #GROUP B POINTS
    boss_B_dict = {"Chaos Elemental": int(hiscore_list[43][1]), "Chaos Fanatic": int(hiscore_list[44][1]),
                     "Dagannoth Prime": int(hiscore_list[48][1]), "Dagannoth_Rex": int(hiscore_list[49][1]),
                     "Dagannoth Supreme": int(hiscore_list[50][1]), "Giant Mole": int(hiscore_list[53][1]),
                     "Grotesque Guardians": int(hiscore_list[54][1]), "Kalphite Queen": int(hiscore_list[56][1]),
                     "King Black Dragon": int(hiscore_list[57][1]), "Kraken": int(hiscore_list[58][1]), "Sarachnis":
                      int(hiscore_list[64][1]), "Scorpia": int(hiscore_list[65][1]), "Thermonuclear Smoke Devil":
                      int(hiscore_list[70][1]), "Zalcano": int(hiscore_list[77][1])}

    boss_B_points = 0
    for key in boss_B_dict:
        #print(boss_B_dict, "kc", boss_B_dict[key])
        if boss_B_dict[key] > 0:
            boss_B_points += boss_B_dict[key]

    boss_points += boss_B_points // 60
    #print(boss_points)

    #GROUP C POINTS
    boss_C_dict = {"Barrows Chests": int(hiscore_list[37][1]),"Crazy Archaeologist": int(hiscore_list[47][1]),
                   "Deranged Archaeologist": int(hiscore_list[51][1]), "Wintertodt": int(hiscore_list[76][1])}

    boss_C_points = 0
    for key in boss_C_dict:
        print(boss_C_dict, "kc", boss_C_dict[key])
        if boss_C_dict[key] > 0:
            boss_C_points += boss_C_dict[key]

    boss_points += boss_C_points // 90
    #print(boss_C_dict["Deranged Archaeologist"])
    #print(boss_C_dict["Deranged Archaeologist"])
    print(boss_points)

    skotizo_kc = int(hiscore_list[66][1])
    if skotizo_kc > 0:
        boss_points += skotizo_kc // 3

    obor_kc = int(hiscore_list[63][1])
    if obor_kc > 0:
        boss_points += obor_kc // 10


    bryophyta_kc = int(hiscore_list[38][1])
    if bryophyta_kc > 0:
        boss_points += bryophyta_kc // 10

    mimic_kc = int(hiscore_list[61][1])
    if mimic_kc > 0:
        boss_points += mimic_kc

    hespori_kc = int(hiscore_list[55][1])
    if hespori_kc > 0:
        boss_points += hespori_kc // 5

    nightmare_kc = int(hiscore_list[62][1])
    if nightmare_kc > 0:
        boss_points += nightmare_kc // 5


    gauntlet_kc = int(hiscore_list[67][1])
    if gauntlet_kc > 0:
        boss_points += gauntlet_kc // 5

    corrupted_gauntlet_kc = int(hiscore_list[68][1])
    if corrupted_gauntlet_kc > 0:
        boss_points += corrupted_gauntlet_kc // 3

    jad_kc = int(hiscore_list[72][1])
    if jad_kc > 0:
        boss_points += jad_kc

    zuk_kc = int(hiscore_list[71][1])
    if zuk_kc > 0:
        boss_points += zuk_kc * 9

    return boss_points


@bot.event
#on_ready() is an event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #showing that a discord bot can be connected to multiple servers
    for guild in bot.guilds:
        if guild.name == GUILD:
            break


    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    for member in guild.members:
        print(f'Guild Members:\n - {member}')

@bot.event
async def on_message(message):
    #client cant tell bbot from normal user
    if message.author == bot.user:
        return
    test_response = "test response"

    if message.content == "test":
        response = test_response
        await message.channel.send(response)

    thanks_reply = "you're welcome master pinkloon!"
    if message.content == "thanks bot":
        response = thanks_reply
        await message.channel.send(response)

    # Without this command on_message will cause all .command
    # functions to be ignored
    await bot.process_commands(message)




@bot.command(name='points')
async def points(ctx, arg):

    url = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + arg
    response = ""
    osrs_response = requests.get(url)
    if osrs_response.status_code == 200:
        #text takes the webpages data and converts it to a string
        response = osrs_response.text
        split_space = response.split("\n")
        hiscore_list = []
        for index in split_space:
            split_index = index.split(",")
            hiscore_list.append(split_index)

        print(hiscore_list)

        total_points = 0

        #querying total xp from website
        total_xp = int(hiscore_list[0][2])
        #calculating total EXP points
        total_xp_points = (total_xp // 250000)
        #adds total xp points to total points
        total_points += total_xp_points
        total_xp_points = "Total EXP points: " + str(total_xp_points)

        #calculating skilling points
        skilling_points = calc_skilling(hiscore_list)
        #adds skilling points to total points
        total_points += skilling_points
        skilling_points = "Skilling points: " + str(skilling_points)

        #calculating clue points
        clue_points = calc_clue(hiscore_list)
        if clue_points > 0:
            #adds clue points to total points
            total_points += clue_points
        else:
            clue_points = 0
        clue_points = "Clue points: " + str(clue_points)

        #calculating raid points
        raid_points = calc_raids(hiscore_list)
        if raid_points > 0:
            #adds raids points to total points
            total_points += raid_points
        else:
            raid_points = 0
        raid_points = "Raid points: " + str(raid_points)

        '''
        gwd_points = calc_bossing(hiscore_list)
        if gwd_points > 0:
            total_points += gwd_points
        else:
            gwd_points = 0

        gwd_points = "GWD points: " + str(gwd_points)
        '''
        bossing_points = calc_bossing(hiscore_list)
        total_points += bossing_points

        bossing_points = "Bossing points: " + str(bossing_points)


        total_points = "Total points: " + str(total_points)
        big_string = FORMAT_SYMBOLS + total_xp_points + "\n" + skilling_points + "\n" + clue_points + "\n" + \
                     raid_points + "\n" + bossing_points + "\n" + total_points + FORMAT_SYMBOLS

    elif osrs_response.status_code == 404:
        big_string = "User not found"

    #await ctx.send(total_level)
    await ctx.send(big_string)


bot.run(TOKEN)
