# bot.py
#we import os so we can access environment variables
#class that allows you to interact with the operating system
FORMAT_SYMBOLS = "```"
BOLD = "**"

import os
from os import path
import random
import datetime
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

def calc_skilling(hiscore_list, user_type):
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
    if user_type == "hardcore" or user_type == "ironman":
        points = int(points * 1.1)
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

    boss_points += boss_A_points // 20

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

    boss_points += boss_B_points // 50
    #print(boss_points)

    #GROUP C POINTS
    boss_C_dict = {"Barrows Chests": int(hiscore_list[37][1]),"Crazy Archaeologist": int(hiscore_list[47][1]),
                   "Deranged Archaeologist": int(hiscore_list[51][1]), "Wintertodt": int(hiscore_list[76][1])}

    boss_C_points = 0
    for key in boss_C_dict:
        print(boss_C_dict, "kc", boss_C_dict[key])
        if boss_C_dict[key] > 0:
            boss_C_points += boss_C_dict[key]

    boss_points += boss_C_points // 80
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





def get_user_data(username, account_type, force):
    flag = check_highscore_status(username)
    if flag == "UTD" and not force:
        return get_data_from_file(username)
    else:
        high_score_data = query_website(username, account_type)
        # If website is down but an older file exists for that user, we
        # want to query using old data since that is better than nothing
        if high_score_data == False:
            if flag == "Old":
                return get_data_from_file(username)
            else:
                return "Down"
        # If the query returned a 404 that means we want to return that the
        # user wasn't found
        elif high_score_data == "404":
            return "UNF"
        # If it is neither of the above it returned a proper response from the runescape
        # api with the user's data
        else:
            create_file(username, account_type, high_score_data)
            return high_score_data

#def check_account_type(username):
#    hiscore_list = get_hiscore_list(username, "main")
#    if hiscore_list:
#        return [hiscore_list, "main"]
#    else:
#        hiscore_list = get_hiscore_list(username, "ironman")
#        if hiscore_list:
#            return [hiscore_list, "ironman"]
#    return False

def query_website(username, account_type):
    base_url = ''
    if account_type == "main":
        base_url = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='
    if account_type == "ironman":
        base_url = 'https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player='
    url = base_url + username
    try:
        osrs_response = requests.get(url, timeout=10)
        if osrs_response.status_code == 200:
            # text takes the webpages data and converts it to a string
            response = osrs_response.text
            split_space = response.split("\n")
            if len(split_space) > 85:
                # Goes to the except block if what is returned is a 200 but not what we expected
                # Most likely returns html from the website down page
                return False
            return response
        elif osrs_response.status_code == 404:
            return "404"
        else:
            return False
    except:
        return False

# This is checking if the user's highscore file exists
# returns False if doesn't exist
# returns "UTD" (Up to Date) if up to date
# returns "Old" if it needs to be updated
def check_highscore_status(username):
    hiscore_file = "_hiscoreFile"
    file_path = 'hiscore_files/' + username + hiscore_file + ".txt"

    # if file does not exist already then we need to write the time its created to the file
    if path.exists(file_path) == False:
        return False
    else:
        with open(file_path) as f:
            current_time = datetime.datetime.now()
            file_modified_date_str = f.readline().strip()
            file_modified_date = datetime.datetime.strptime(file_modified_date_str, '%Y-%m-%d %H:%M:%S')
            if file_modified_date < current_time - datetime.timedelta(hours=4):
                return "Old"
            else:
                return "UTD"


def create_file(username, account_type, high_score_data):
    hiscore_file = "_hiscoreFile"
    file_path = 'hiscore_files/' + username + hiscore_file + ".txt"

    myFile = open(file_path, 'w')
    current_time = datetime.datetime.now()
    saved_time =str(current_time).split(".")[0]

    fileContents = saved_time + "\n" + high_score_data

    myFile.write(fileContents)
    myFile.close()


def get_data_from_file(username):
    hiscore_file = "_hiscoreFile"
    file_path = 'hiscore_files/' + username + hiscore_file + ".txt"

    myFile = open(file_path, 'r')

    high_scores = myFile.readlines()[1:]
    high_score_data = ""
    for line in high_scores:
        high_score_data = high_score_data + line

    return high_score_data

def get_hiscore_list(user_data):
    split_space = user_data.split("\n")
    hiscore_list = []
    for index in split_space:
        split_index = index.split(",")
        hiscore_list.append(split_index)
    return hiscore_list


@bot.command(name='points')
async def points(ctx, rsn, type=None, force=None):
    big_string = ""
    account_type = "ironman"

    if force == "force":
        force = True
    else:
        force = False

    if type != "ironman":
        account_type = "main"

    user_data = get_user_data(rsn, account_type, force)

    if user_data == "Down":
        big_string = "OH NO! The OSRS Highscore Page is down. Please try again later."
    elif user_data == "UNF":
        big_string = "User Not Found. Please make sure the username and account type you put are correct"
    else:
        hiscore_list = get_hiscore_list(user_data)

        #print(hiscore_list)

        total_points = 0

        #querying total xp from website
        total_xp = int(hiscore_list[0][2])
        #calculating total EXP points
        total_xp_points = (total_xp // 250000)
        #adds total xp points to total points
        total_points += total_xp_points
        total_xp_points = "Total EXP points: " + str(total_xp_points)

        #calculating skilling points
        skilling_points = calc_skilling(hiscore_list, account_type)
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

        #calculating bossing points
        bossing_points = calc_bossing(hiscore_list)
        total_points += bossing_points
        bossing_points = "Bossing points: " + str(bossing_points)

        total_points = "Total points: " + str(total_points)

        user = f"User: " + rsn

        big_string = FORMAT_SYMBOLS + user + "\n" + total_xp_points + "\n" + skilling_points + "\n" + clue_points + "\n" + \
                     raid_points + "\n" + bossing_points + "\n" + total_points + FORMAT_SYMBOLS

    #await ctx.send(total_level)
    await ctx.send(big_string)


@bot.command(name='apply')
async def save_application(ctx, rsn, type=None, about_me=""):
    application_received = ""
    account_type = "ironman"

    if type != "ironman":
        account_type = "main"

    user_data = get_user_data(rsn, account_type)

    if user_data == "Down":
        application_received = "OH NO! The OSRS Highscore Page is down. Please try again later."
    elif user_data == "UNF":
        application_received = "RSN Not Found. Please make sure the username and account type you put are correct"
    else:
        hiscore_list = get_hiscore_list(user_data)
        discord_name = ctx.author
        print(discord_name)
        os.makedirs('applications', exist_ok=True)

        skill_points = calc_skilling(hiscore_list, account_type)
        clue_points = calc_clue(hiscore_list)
        raid_points = calc_raids(hiscore_list)
        bossing_points = calc_bossing(hiscore_list)

        total_xp = int(hiscore_list[0][2])
        total_xp_points = (total_xp // 250000)

        total_points = skill_points + clue_points + raid_points + bossing_points + total_xp_points

        fileName = 'applications/' + rsn + ".txt"
        myFile = open(fileName, 'w')
        fileContents = \
        '''RSN: %s
        About Me: %s
        Discord Name: %s
        Raids Points: %s
        PVM Points: %s
        Level Points: %s
        Exp Points: %s
        Total Points: %d
            ''' % (rsn, about_me, discord_name, raid_points, bossing_points, skill_points, total_xp_points, total_points)

        myFile.write(fileContents)
        myFile.close()
        application_received = "Your application has been submitted for review!"

    await ctx.send(application_received)

bot.run(TOKEN)

#@bot.command(name='rules')
#rules = ""