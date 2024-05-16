# bot.py
# we import os so we can access environment variables
# class that allows you to interact with the operating system
FORMAT_SYMBOLS = "```"
TOTAL_POINTS_MIN = 0
MAX_PEOPLE = 7
MONTH = 30

import os
from os import path
import random
import datetime
import sys
import re
import time
import datetime
from dateutil.relativedelta import relativedelta
from bosses_enum import Bosses

import discord
from discord.ext import commands
from dotenv import load_dotenv  # comment out if testing locally
from collections import deque
import requests
from raid_queue import *

from pointsdisplay import pointsdisplay
from pointsdisplay import fullpointsdisplay
from threading import Lock

image_file_lock = Lock()

import how_to_rank_up

load_dotenv()  # comment out if testing locally
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

global_raids_list = [RaidTeachingSession("learner-raids-1"),
                     RaidTeachingSession("learner-raids-2")]


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
        points += 100
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
    if user_type == "hardcore" or user_type == "ironman" or user_type == "gim":
        points = int(points * 1.1)
    return points


def calc_clue(hiscore_list):
    points = 0

    beginner_clue = int(hiscore_list[30][1])
    easy_clue = int(hiscore_list[31][1])
    medium_clue = int(hiscore_list[32][1])
    hard_clue = int(hiscore_list[33][1])
    elite_clue = int(hiscore_list[34][1])
    master_clue = int(hiscore_list[35][1])

    # print(beginner_clue)
    # print(easy_clue)
    # print(medium_clue)
    # print(hard_clue)
    # print(elite_clue)
    # print(master_clue)

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


# Calculate raid points
def calc_raids(hiscore_list):
    placeHolder = 0  # When kc is 0
    # cox
    cox_points = 0
    cm_points = 0
    cox_kc = int(hiscore_list[Bosses.COX.value][1])
    cm_cox_kc = int(hiscore_list[Bosses.COX_CM.value][1])
    # tob
    tob_points = 0
    tob_hm_points = 0
    tob_kc = int(hiscore_list[Bosses.TOB.value][1])
    tob_hm_kc = int(hiscore_list[Bosses.TOB_HM.value][1])
    # toa
    toa_points = 0
    toa_hard_points = 0
    toa_kc = int(hiscore_list[Bosses.TOA.value][1])
    toa_hard_kc = int(hiscore_list[Bosses.TOA_HM.value][1])

    raid_list = []
    # print(cox_kc)
    # print(cm_cox_kc)
    # print(tob_kc)
    # print('tob hm kc', tob_hm_kc)

    # Add cox kc
    if cox_kc > 0:
        cox_points += cox_kc
        raid_list.append(cox_points)
    else:
        raid_list.append(placeHolder)
    # Add cm cox kc
    if cm_cox_kc > 0:
        cm_points += cm_cox_kc * 3
        raid_list.append(cm_points)
    else:
        raid_list.append(placeHolder)
    # Add tob kc
    if tob_kc > 0:
        tob_points += tob_kc * 2
        raid_list.append(tob_points)
    else:
        raid_list.append(placeHolder)
    # Add tob hm kc
    if tob_hm_kc > 0:
        tob_hm_points += tob_hm_kc * 3
        raid_list.append(tob_hm_points)
    else:
        raid_list.append(placeHolder)
    # Add toa kc
    if toa_kc > 0:
        toa_points += toa_kc
        raid_list.append(toa_points)
    else:
        raid_list.append(placeHolder)
    # Add toa expert kc
    if toa_hard_kc > 0:
        toa_hard_points += toa_hard_kc * 2
        raid_list.append(toa_hard_points)
    else:
        raid_list.append(placeHolder)
    # print(raid_list)
    return raid_list


def calc_lms(hiscore_list):
    points = 0
    lms_kc = int(hiscore_list[36][1])
    if lms_kc > 0:
        points = (lms_kc - 500) // 10

    return points


def calc_soulWars(hiscore_list):
    points = 0
    soulWars_kc = int(hiscore_list[38][1])
    # print("this is my soulwars kc", soulWars_kc)
    if soulWars_kc > 0:
        points += (soulWars_kc // 300)

    return points

def calc_glory(hiscore_list):
    points = 0
    glory_pts = int(hiscore_list[41][1])
    # print("this is my soulwars kc", soulWars_kc)
    if glory_pts > 0:
        points += (glory_pts // 1000)

    return points


def calc_bossing(hiscore_list):
    boss_points = 0

    gwd_dict = {
        "Commander Zilyana": int(hiscore_list[Bosses.COMMANDER_ZILYANA.value][1]),
        "General Graardor": int(hiscore_list[Bosses.GENERAL_GRAARDOR.value][1]),
        "Kree'Arra": int(hiscore_list[Bosses.KREEARRA.value][1]),
        "K'ril Tsutsaroth": int(hiscore_list[Bosses.KRIL_TSUTSAROTH.value][1]),
        "Nex": int(hiscore_list[Bosses.NEX.value][1])
    }
    # print("nex kc: ", hiscore_list[65][1])
    gwd_points = 0
    for key in gwd_dict:
        # print(gwd_dict[key])
        if gwd_dict[key] > 0:
            # print(gwd_points)
            gwd_points += gwd_dict[key]
    # print("GWD KC:", gwd_points)

    boss_points += gwd_points // 10
    # print(boss_points)

    # GROUP A POINTS
    boss_A_dict =\
        {"Abyssal Sire": int(hiscore_list[Bosses.ABYSSAL_SIRE.value][1]),
         "Alchemical Hydra": int(hiscore_list[Bosses.ALCHEMICAL_HDYRA.value][1]),
         "Callisto": int(hiscore_list[Bosses.CALLISTO.value][1]),
         "Cerberus": int(hiscore_list[Bosses.CERBERUS.value][1]),
         "Venenatis": int(hiscore_list[Bosses.VENENATIS.value][1]),
         "Vet'ion": int(hiscore_list[Bosses.VETION.value][1]),
         "Vorkath": int(hiscore_list[Bosses.VORKATH.value][1]),
         "Zulrah": int(hiscore_list[Bosses.ZULRAH.value][1]),
         "Phantom Muspah": int(hiscore_list[Bosses.PHANTOM_MUSPAH.value][1])}


    boss_A_points = 0
    for key in boss_A_dict:
        # print(boss_A_dict, "kc", boss_A_dict[key])
        if boss_A_dict[key] > 0:
            boss_A_points += boss_A_dict[key]

    boss_points += boss_A_points // 20
    print("TIER 1:", boss_A_points)
    # print('sire', int(hiscore_list[Bosses.ABYSSAL_SIRE.value][1]))

    # GROUP B POINTS
    boss_B_dict =\
        {"Chaos Elemental": int(hiscore_list[Bosses.CHAOS_ELEMENTAL.value][1]),
         "Chaos Fanatic": int(hiscore_list[Bosses.CHAOS_FANATIC.value][1]),
         "Dagannoth Prime": int(hiscore_list[Bosses.DAG_PRIME.value][1]),
         "Dagannoth_Rex": int(hiscore_list[Bosses.DAG_REX.value][1]),
         "Dagannoth Supreme": int(hiscore_list[Bosses.DAG_SUPREME.value][1]),
         "Giant Mole": int(hiscore_list[Bosses.GIANT_MOLE.value][1]),
         "Grotesque Guardians": int(hiscore_list[
                                        Bosses.GROTESQUE_GUARDIANS.value][1]),
         "Kalphite Queen": int(hiscore_list[Bosses.KALPHITE_QUEEN.value][1]),
         "King Black Dragon": int(hiscore_list[Bosses.KING_BLACK_DRAGON.value][
                                      1]),
         "Kraken": int(hiscore_list[Bosses.KRAKEN.value][1]),
         "Sarachnis": int(hiscore_list[Bosses.SARACHNIS.value][1]),
         "Scorpia": int(hiscore_list[Bosses.SCORPIA.value][1]),
         "Thermonuclear Smoke Devil": int(hiscore_list[
                    Bosses.THERMONUCLEAR_SMOKE_DEVIL.value][1]),
         "Zalcano": int(hiscore_list[Bosses.ZALCANO.value][1]),
         "Artio": int(hiscore_list[Bosses.ARTIO.value][1]),
         "Calvar'ion": int(hiscore_list[Bosses.CALVARION.value][1]),
         "Spindel": int(hiscore_list[Bosses.SPINDEL.value][1])}

    # print("Sarachnis", int(hiscore_list[69][1]))
    # print("Scorpia", int(hiscore_list[Bosses.SCORPIA.value][1]))

    boss_B_points = 0
    for key in boss_B_dict:
        # print(boss_B_dict, "kc", boss_B_dict[key])
        if boss_B_dict[key] > 0:
            boss_B_points += boss_B_dict[key]

    boss_points += boss_B_points // 50
    print("TIER 2:", boss_B_points)
    # print(boss_B_dict)

    # GROUP C POINTS
    boss_C_dict =\
        {"Barrows Chests": int(hiscore_list[Bosses.BARROWS.value][1]),
         "Crazy Archaeologist": int(hiscore_list[
                                    Bosses.CRAZY_ARCHAEOLOGIST.value][1]),
         "Deranged Archaeologist": int(hiscore_list[
                                    Bosses.DERANGED_ARCHAEOLOGIST.value][1]),
         "Wintertodt": int(hiscore_list[Bosses.WINTERTODT.value][1]),
         "Guardians of the Rift": int(hiscore_list[40][1]),
         "Tempoross": int(hiscore_list[Bosses.TEMPOROSS.value][1]),
         "Scurrius": int(hiscore_list[Bosses.SCURRIUS.value][1])}

    # print("SCURRIUS:", int(hiscore_list[Bosses.SCURRIUS.value][1]))

    boss_C_points = 0
    for key in boss_C_dict:
        # print(boss_C_dict, "kc", boss_C_dict[key])
        if boss_C_dict[key] > 0:
            boss_C_points += boss_C_dict[key]

    boss_points += boss_C_points // 80
    print("TIER 3:", boss_C_points)
    # print(boss_C_dict["Deranged Archaeologist"])
    # print(boss_C_dict["Deranged Archaeologist"])
    # print(boss_points)

    dt2_dict = {
        "Vardorvis": int(hiscore_list[Bosses.VARDORVIS.value][1]),
        "Whisperer": int(hiscore_list[Bosses.WHISPERER.value][1]),
        "Duke Sucellus": int(hiscore_list[Bosses.DUKE_SUCELLUS.value][1]),
        "Leviathan": int(hiscore_list[Bosses.LEVIATHAN.value][1])
    }

    # print("VARD", dt2_dict["Vardorvis"])
    # print("WHISP", dt2_dict["Whisperer"])
    # print("DUKE", dt2_dict["Duke Sucellus"])
    # print("LEVI", dt2_dict["Leviathan"])

    dt2_points = 0
    for key in dt2_dict:
        if dt2_dict[key] > 0:
            print("ADDING:", dt2_dict[key])
            dt2_points += dt2_dict[key]
    boss_points += dt2_points // 15

    skotizo_kc = int(hiscore_list[Bosses.SKOTIZO.value][1])
    if skotizo_kc > 0:
        boss_points += skotizo_kc // 3
    # print("skotizo", skotizo_kc)

    lunar_chests_kc = int(hiscore_list[Bosses.LUNAR_CHESTS.value][1])
    if lunar_chests_kc > 0:
        boss_points += lunar_chests_kc // 65

    print("LUNAR CHESTS:", lunar_chests_kc)

    obor_kc = int(hiscore_list[Bosses.OBOR.value][1])
    if obor_kc > 0:
        boss_points += obor_kc // 10
    # print("obor", obor_kc)

    bryophyta_kc = int(hiscore_list[Bosses.BRYOPHYTA.value][1])
    if bryophyta_kc > 0:
        boss_points += bryophyta_kc // 10
    # print("bryophyta_kc", bryophyta_kc)

    corporeal_kc = int(hiscore_list[Bosses.CORPORAL_BEAST.value][1])
    if corporeal_kc > 0:
        boss_points += corporeal_kc // 7
    print(corporeal_kc)

    mimic_kc = int(hiscore_list[Bosses.MIMIC.value][1])
    if mimic_kc > 0:
        boss_points += mimic_kc
    # print("mimic_kc", mimic_kc)

    hespori_kc = int(hiscore_list[Bosses.HESPORI.value][1])
    if hespori_kc > 0:
        boss_points += hespori_kc // 5
    # print("hespori", hespori_kc)

    nightmare_kc = int(hiscore_list[Bosses.NIGHTMARE.value][1])
    if nightmare_kc > 0:
        boss_points += nightmare_kc // 5
    # print("nightmare_kc", nightmare_kc)

    phosani_nm_kc = int(hiscore_list[Bosses.PHOSANIS_NIGHTMARE.value][1])
    if phosani_nm_kc > 0:
        boss_points += phosani_nm_kc // 2
    # print("pnm_kc", phosani_nm_kc)

    gauntlet_kc = int(hiscore_list[Bosses.GAUNTLET.value][1])
    if gauntlet_kc > 0:
        boss_points += gauntlet_kc // 5
    # print("gauntlet_kc", gauntlet_kc)

    corrupted_gauntlet_kc = int(hiscore_list[
                                    Bosses.CORRUPTED_GAUNTLET.value][1])
    if corrupted_gauntlet_kc > 0:
        boss_points += corrupted_gauntlet_kc // 3
    # print("corrupted_gauntlet_kc", corrupted_gauntlet_kc)

    jad_kc = int(hiscore_list[Bosses.JAD.value][1])
    if jad_kc > 0:
        boss_points += jad_kc
    # print("jad_kc", jad_kc)

    zuk_kc = int(hiscore_list[Bosses.ZUK.value][1])
    if zuk_kc > 0:
        boss_points += zuk_kc * 9
    # print("zuk_kc", zuk_kc)
    # print(boss_points)

    sol_kc = int(hiscore_list[Bosses.SOL_HEREDIT.value][1])
    if sol_kc > 0:
        boss_points += sol_kc * 4

    # print("SOL KC", sol_kc)

    return boss_points


@bot.event
# on_ready() is an event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # showing that a discord bot can be connected to multiple servers
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # for member in guild.members:
    # print(f'Guild Members:\n - {member}')


@bot.event
async def on_message(message):
    # client cant tell bbot from normal user
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


def query_website(username, account_type):
    base_url = ''
    if account_type == "main" or account_type == "gim":
        base_url = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='
    if account_type == "ironman":
        base_url = 'https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws?player='
    url = base_url + username
    print("Querying: " + str(url))
    try:
        osrs_response = requests.get(url, timeout=10)
        # print("Responded?" + str(osrs_response))
        if osrs_response.status_code == 200:
            # text takes the webpages data and converts it to a string
            response = osrs_response.text
            print(response)
            split_space = response.split("\n")
            # if len(split_space) > 85:
            # Goes to the except block if what is returned is a 200 but not what we expected
            # Most likely returns html from the website down page
            #    return False
            print("Responded OK")
            return response
        elif osrs_response.status_code == 404:

            print("Responded 404")
            return "404"
        else:

            print("Responded ???")
            return False
    except:
        print("Failed to query website")
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
            file_modified_date = datetime.datetime.strptime(
                file_modified_date_str, '%Y-%m-%d %H:%M:%S')
            if file_modified_date < current_time - datetime.timedelta(hours=4):
                return "Old"
            else:
                return "UTD"


def create_file(username, account_type, high_score_data):
    hiscore_file = "_hiscoreFile"
    file_path = 'hiscore_files/' + username + hiscore_file + ".txt"

    myFile = open(file_path, 'w')
    current_time = datetime.datetime.now()
    saved_time = str(current_time).split(".")[0]

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
async def points(ctx, rsn, *args):
    force = False
    advanced = False
    account_type = "main"
    # print("In !points")
    for arg in args:
        if arg == "force":
            force = True
        if arg == "advanced":
            advanced = True
        if arg == "ironman":
            account_type = "ironman"
        if arg == "gim" or arg == "ugim":
            account_type = "gim"

    user_data = get_user_data(rsn, account_type, force)

    if user_data == "Down":
        big_string = "OH NO! The OSRS Highscore Page is down. Please try again later."
    elif user_data == "UNF":
        big_string = "User Not Found. Please make sure the username and account type you put are correct"
        await ctx.channel.send("User Not Found! Please make sure the "
                               "username and account type are correct.")
    else:
        hiscore_list = get_hiscore_list(user_data)

        # print(hiscore_list)

        total_points = 0
        skill_points = 0
        # print(int(hiscore_list[35][1]))
        # querying total xp from website
        total_xp = int(hiscore_list[0][2])
        # calculating total EXP points
        total_xp_points = (total_xp // 250000)
        # adds total xp points to total points
        total_points += total_xp_points
        skill_points += total_xp_points
        total_xp_points_str = "  Exp: " + str(total_xp_points)
        # print('this is my total expp: ', total_xp_points)
        # print('this is my total exp: ', total_xp)
        # for x in range(len(hiscore_list)):
        # print(str(x) + ": " + str(hiscore_list[x]))

        # calculating skilling points
        skilling_points = calc_skilling(hiscore_list, account_type)
        # adds skilling points to total points
        total_points += skilling_points
        skill_points += skilling_points
        skilling_points_str = "  Level: " + str(skilling_points)
        skill_points_str = "Skill points: " + str(skill_points)

        miscellaneous_points = 0

        # calculating clue points
        clue_points = calc_clue(hiscore_list)
        if clue_points > 0:
            # adds clue points to total points
            total_points += clue_points
        else:
            clue_points = 0
        clue_points_str = "  Clues: " + str(clue_points)

        # calculating lms points
        lms_points = calc_lms(hiscore_list)
        if lms_points > 0:
            total_points += lms_points
        else:
            lms_points = 0
        lms_points_str = "  LMS: " + str(lms_points)

        miscellaneous_points += lms_points
        # print("misc points before soul wars", miscellaneous_points)
        # calculating soul wars points

        soulWars_points = calc_soulWars(hiscore_list)
        # print("soul wars points", soulWars_points)
        if soulWars_points > 0:
            total_points += soulWars_points
        else:
            soulWars_points = 0
        miscellaneous_points += soulWars_points

        glory_points = calc_glory(hiscore_list)
        # print("glory points", glory_points)
        if glory_points > 0:
            total_points += glory_points
        else:
            glory_points = 0
        miscellaneous_points += glory_points

        # print("misc points after soul", miscellaneous_points)
        # print("soul wars points", miscellaneous_points)

        pvm_points = 0

        # calculating raid points
        raid_list = calc_raids(hiscore_list)
        # print(raid_list)
        raid_points = 0
        for raid in raid_list:
            if raid > 0:
                raid_points += raid
        total_points += raid_points
        pvm_points += raid_points
        raid_points_str = "  Raids: " + str(raid_points)
        cox_points = raid_list[0]
        cox_points_str = "    COX: " + str(cox_points)
        cm_points = raid_list[1]
        cm_points_str = "    CM: " + str(cm_points)
        tob_points = raid_list[2]
        tob_points_str = "    TOB: " + str(tob_points)
        tob_hm_points = raid_list[3]
        tob_hm_points_str = "    TOB HM: " + str(tob_hm_points)
        toa_points = raid_list[4]
        toa_points_str = "    TOA: " + str(toa_points)
        toa_hard_points = raid_list[5]
        toa_hard_points_str = "    TOA HM: " + str(toa_hard_points)

        # calculating bossing points
        bossing_points = calc_bossing(hiscore_list)
        total_points += bossing_points
        pvm_points += bossing_points
        bossing_points_str = "  Other: " + str(bossing_points)
        pvm_points_str = "PVM Points: " + str(pvm_points)
        total_points_str = "TOTAL POINTS: " + str(total_points)

        user = f"USER: " + "⚔️ " + rsn + " ⚔️"
        misc_points_str = f"Misc points: " + str(miscellaneous_points)

        big_string = FORMAT_SYMBOLS + user + "\n" + "\n" + pvm_points_str + \
                     "\n" + raid_points_str + "\n" + cox_points_str + \
                     "\n" + cm_points_str + "\n" + tob_points_str + "\n" + \
                     tob_hm_points_str + "\n" + toa_points_str + "\n" + \
                     toa_hard_points_str + "\n" + bossing_points_str + "\n" + \
                     "\n" + skill_points_str + "\n" + total_xp_points_str + \
                     "\n" + skilling_points_str + "\n" + "\n" + \
                     misc_points_str + "\n" + clue_points_str + "\n" + \
                     lms_points_str + "\n" + "\n" + total_points_str + \
                     FORMAT_SYMBOLS
        print('big string: ', '\n', big_string)
        raids_tuple = calc_raids(hiscore_list)

        print()

        cm_pts = raids_tuple[1]
        tob_pts = raids_tuple[2]
        tob_hm_pts = raids_tuple[3]
        toa_pts = raids_tuple[4]
        toa_hard_pts = raids_tuple[5]
        raids_pts = raids_tuple[0] + cm_pts + tob_pts + tob_hm_pts + toa_pts \
                    + toa_hard_pts
        # await ctx.send(total_level)
        # pvm_points = (cm, tob, raids, other)
        # skilling_points=[tlbonus=0, tepoints=0, allsps=0]
        image_file_lock.acquire()
        player = pointsdisplay.PointsImage()
        image_file = player.draw_all_text(rsn,
                                          total_points,
                                          pvm_points=[raids_pts, cox_points,
                                                      cm_points, tob_points,
                                                      tob_hm_points,
                                                      toa_points,
                                                      toa_hard_points,
                                                      bossing_points],
                                          skilling_points=[skilling_points,
                                                           total_xp_points,
                                                           skilling_points +
                                                           total_xp_points],
                                          other_points=[clue_points,
                                                        miscellaneous_points])
        # input("WAIT7")
        if advanced:
            await ctx.channel.send(big_string)
        else:
            discord_file = discord.File(image_file)
            await ctx.channel.send(file=discord_file)
            # input("WAIT")
            discord_file.close()

        image_file_lock.release()


@bot.command(name='fullpoints')
async def full_points(ctx, rsn, *args):
    force = False
    advanced = False
    account_type = "main"

    for arg in args:
        if arg == "force":
            force = True
        if arg == "advanced":
            advanced = True
        if arg == "ironman":
            account_type = "ironman"

    user_data = get_user_data(rsn, account_type, force)

    if user_data == "Down":
        big_string = "OH NO! The OSRS Highscore Page is down. Please try again later."
    elif user_data == "UNF":
        big_string = "User Not Found. Please make sure the username and account type you put are correct"
    else:
        hiscore_list = get_hiscore_list(user_data)

        # print(hiscore_list)

        total_points = 0
        skill_points = 0
        # print(int(hiscore_list[35][1]))
        # querying total xp from website
        total_xp = int(hiscore_list[0][2])
        # calculating total EXP points
        total_xp_points = (total_xp // 250000)
        # adds total xp points to total points
        total_points += total_xp_points
        skill_points += total_xp_points
        total_xp_points_str = "  Exp: " + str(total_xp_points)
        # print('this is my total expp: ', total_xp_points)
        # print('this is my total exp: ', total_xp)
        # for x in range(len(hiscore_list)):
        # print(str(x) + ": " + str(hiscore_list[x]))

        # calculating skilling points
        skilling_points = calc_skilling(hiscore_list, account_type)
        # adds skilling points to total points
        total_points += skilling_points
        skill_points += skilling_points
        skilling_points_str = "  Level: " + str(skilling_points)
        skill_points_str = "Skill points: " + str(skill_points)

        miscellaneous_points = 0

        # calculating clue points
        clue_points = calc_clue(hiscore_list)
        if clue_points > 0:
            # adds clue points to total points
            total_points += clue_points
        else:
            clue_points = 0
        clue_points_str = "  Clues: " + str(clue_points)

        # calculating lms points
        lms_points = calc_lms(hiscore_list)
        if lms_points > 0:
            total_points += lms_points
        else:
            lms_points = 0
        lms_points_str = "  LMS: " + str(lms_points)

        miscellaneous_points += lms_points
        # print("misc points before soul wars", miscellaneous_points)
        # calculating soul wars points

        soulWars_points = calc_soulWars(hiscore_list)

        # print("soul wars points", soulWars_points)
        if soulWars_points > 0:
            total_points += soulWars_points
        else:
            soulWars_points = 0
        miscellaneous_points += soulWars_points

        # print("misc points after soul", miscellaneous_points)
        # print("soul wars points", miscellaneous_points)

        pvm_points = 0

        # calculating raid points
        raid_list = calc_raids(hiscore_list)
        # print(raid_list)
        raid_points = 0
        for raid in raid_list:
            if raid > 0:
                raid_points += raid
        total_points += raid_points
        pvm_points += raid_points
        raid_points_str = "  Raids: " + str(raid_points)
        cox_points = raid_list[0]
        cox_points_str = "    COX: " + str(cox_points)
        cm_points = raid_list[1]
        cm_points_str = "    CM: " + str(cm_points)
        tob_points = raid_list[2]
        tob_points_str = "    TOB: " + str(tob_points)
        tob_hm_points = raid_list[3]
        tob_hm_points_str = "    TOB HM: " + str(tob_hm_points)
        toa_points = raid_list[4]
        toa_points_str = "    TOA: " + str(toa_points)
        toa_hard_points = raid_list[5]
        toa_hard_points_str = "    TOA HM: " + str(toa_hard_points)

        # calculating bossing points
        bossing_points = calc_bossing(hiscore_list)
        total_points += bossing_points
        pvm_points += bossing_points
        bossing_points_str = "  Other: " + str(bossing_points)
        pvm_points_str = "PVM Points: " + str(pvm_points)
        total_points_str = "TOTAL POINTS: " + str(total_points)

        user = f"USER: " + "⚔️ " + rsn + " ⚔️"
        misc_points_str = f"Misc points: " + str(miscellaneous_points)

        big_string = FORMAT_SYMBOLS + user + "\n" + "\n" + pvm_points_str + \
                     "\n" + raid_points_str + "\n" + cox_points_str + \
                     "\n" + cm_points_str + "\n" + tob_points_str + "\n" + \
                     tob_hm_points_str + "\n" + toa_points_str + "\n" + \
                     toa_hard_points_str + "\n" + bossing_points_str + "\n" + \
                     "\n" + skill_points_str + "\n" + total_xp_points_str + \
                     "\n" + skilling_points_str + "\n" + "\n" + \
                     misc_points_str + "\n" + clue_points_str + "\n" + \
                     lms_points_str + "\n" + "\n" + total_points_str + \
                     FORMAT_SYMBOLS
        # print('big string: ', '\n', big_string)
        raids_tuple = calc_raids(hiscore_list)

        # print()

        cm_pts = raids_tuple[1]
        tob_pts = raids_tuple[2]
        tob_hm_pts = raids_tuple[3]
        toa_pts = raids_tuple[4]
        toa_hard_pts = raids_tuple[5]
        raids_pts = raids_tuple[0] + cm_pts + tob_pts + tob_hm_pts + toa_pts \
                    + toa_hard_pts
        # await ctx.send(total_level)
        # pvm_points = (cm, tob, raids, other)
        # skilling_points=[tlbonus=0, tepoints=0, allsps=0]
        image_file_lock.acquire()
        player = fullpointsdisplay.FullPointsImage()
        image_file = player.draw_all_text(rsn,
                                          total_points,
                                          pvm_points=[raids_pts, cox_points,
                                                      cm_points, tob_points,
                                                      tob_hm_points,
                                                      toa_points,
                                                      toa_hard_points,
                                                      bossing_points],
                                          skilling_points=[skilling_points,
                                                           total_xp_points,
                                                           skilling_points +
                                                           total_xp_points],
                                          other_points=[clue_points,
                                                        miscellaneous_points])
        # input("WAIT7")
        if advanced:
            await ctx.channel.send(big_string)
        else:
            discord_file = discord.File(image_file)
            await ctx.channel.send(file=discord_file)
            # input("WAIT")
            discord_file.close()

        image_file_lock.release()

        # Check when user is eligible for next rank
        # Calculate point parameters
        total_cox_points = cox_points + cm_points
        total_tob_points = tob_points + tob_hm_points
        total_toa_points = toa_points + toa_hard_points

        # Find date of last rank upgrade
        # Get all CC role-related ranks
        Trialist = discord.utils.get(ctx.guild.roles, name='Trialist')
        Battlemage = discord.utils.get(ctx.guild.roles, name='Battlemage')
        Artillery = discord.utils.get(ctx.guild.roles, name='Artillery')
        Infantry = discord.utils.get(ctx.guild.roles, name='Infantry')
        Crusader = discord.utils.get(ctx.guild.roles, name='Crusader')
        Sniper = discord.utils.get(ctx.guild.roles, name='Sniper')
        Carry = discord.utils.get(ctx.guild.roles, name='Carry')
        Guthixian = discord.utils.get(ctx.guild.roles, name='Guthixian')
        Skiller = discord.utils.get(ctx.guild.roles, name='Skiller')
        Maxed = discord.utils.get(ctx.guild.roles, name='Maxed')

        # List that contains all role ranks
        role_list = [Trialist, Battlemage, Artillery, Infantry, Crusader,
                     Sniper, Carry, Guthixian, Skiller, Maxed]
        current_role = Trialist

        file_path = ''
        # Find if user has current rank in CC (and if so, what rank it is)
        for role in ctx.author.roles:
            if role in role_list:
                file_path = 'applications/' + str(role) + '/' + rsn + '.txt'
                file_exists = path.exists(file_path)
                if file_exists:
                    current_role = role
                    break

        index = 0
        # Find index of current_role in role_list
        for role in role_list:
            if current_role != role:
                index += 1
            else:
                break

        my_file = open(file_path, 'r')
        eligible_date = my_file.readlines()[12]
        my_file.close()

        eligible_message = check_eligibility(total_points, pvm_points,
                                             raid_points,
                                             total_cox_points, total_tob_points,
                                             total_toa_points, eligible_date,
                                             current_role, index)
        await ctx.channel.send(eligible_message)


def check_eligibility(total_points, pvm_points, raid_points,
                      total_cox_points, total_tob_points,
                      total_toa_points, eligible_date, current_role, index):
    '''
    # List of all roles
    role_list = ['Trialist', 'Battlemage', 'Artillery', 'Infantry', 'Crusader',
                 'Sniper', 'Carry', 'Guthixian', 'Skiller', 'Maxed']

    # Determine next role for which to check eligibility
    role_to_check = role_list[index + 1]
    eligible_role = 'Trialist'

    # Compare user's points with next rank
    # Check Battlemage
    '''

    # Compare time since last upgraded role
    # Find today's date
    # date_today = datetime.datetime.today()
    # Find 1 month from last rank up

    date_message = 'You can apply for this rank after ' + eligible_date

    return date_message


def verify_rsn(rsn):
    rsn_re = re.compile('^[a-z0-9 \_]+$').search
    if bool(rsn_re(rsn)) and len(rsn) < 25:
        return True
    else:
        return False


@bot.command(name='createparty')
@commands.has_role('Teacher CoX')
async def create_party(ctx):
    output_string = "You are not in a learner raids channel."
    discord_name = ctx.author.mention
    discord_name = str(discord_name)
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].open_queue()
        output_string = discord_name + " has opened the queue."

    await ctx.channel.send(output_string)


@bot.command(name='test')
async def nine_nine(ctx):
    print("hello")
    brooklyn_99_quotes = [
        'hi',
        (
            'hi'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='endparty')
@commands.has_role('Teacher CoX')
async def end_party(ctx):
    output_string = "You are not in a learner raids channel."
    discord_name = ctx.author
    ping_name = ctx.author.mention
    discord_name = str(discord_name)
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].close_queue()
        output_string = ping_name + " has closed the queue."

    await ctx.channel.send(output_string)


@bot.command(name='teach')
@commands.has_role('Teacher CoX')
async def teacher_join(ctx, rsn):
    output_string = "You are not in a learner raids channel."
    discord_name = ctx.author
    ping_name = ctx.author.mention
    ping_name = str(ping_name)
    discord_name = str(discord_name)
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].add_teacher(discord_name,
                                                                 rsn)
        output_string = ping_name + " has been added as a teacher."

    await ctx.channel.send(output_string)


@bot.command(name='join')
async def join_queue(ctx, rsn):
    if verify_rsn(rsn) == False:
        return
    Flag = False
    channel_name = ctx.channel.name
    raid_roles = ["Novice CoX", "Beginner CoX", "Intermediate CoX",
                  "Advanced CoX", "Teacher CoX"]

    if "learner-raids-" in channel_name:
        roles = ctx.author.roles
        print(roles)
        cox_rank = ""
        if global_raids_list[int(channel_name[-1]) - 1].scan_queue(rsn):
            output_string = "{} is already in the queue".format(rsn)
        else:
            for role in roles:
                if role.name in raid_roles and role.name != "Teacher CoX":
                    cox_rank = role.name
                if role.name == "Teacher CoX":
                    Flag = True
            print(cox_rank)
            discord_name = ctx.author
            discord_name = str(discord_name)
            print(discord_name)
            # global_raids_list[0].add_to_session
            output_string = ""
            if Flag == True:
                output_string = "You are a teacher! To join the raid party use the teacher command -> !teach 'rsn' "

            elif cox_rank != "":
                if global_raids_list[
                    int(channel_name[-1]) - 1].get_status() == True:
                    global_raids_list[int(channel_name[-1]) - 1].add_to_queue(
                        discord_name, rsn, cox_rank, 0)
                    output_string = rsn + " has been added to the queue."
                else:
                    output_string = "This queue is currently not open."


            else:
                output_string = "You are not currently assigned a CoX role."

        await ctx.channel.send(output_string)


# allows a teacher to start a raid
@bot.command(name='startraid')
@commands.has_role('Teacher CoX')
async def start_raid(ctx):
    channel_name = ctx.channel.name
    party_string = "You are not in a learner raids channel"
    if "learner-raids-" in channel_name:
        if len(global_raids_list[
                   int(channel_name[-1]) - 1].get_teachers()) != 0:
            global_raids_list[int(channel_name[-1]) - 1].generate_next_party()
            party_members = global_raids_list[
                int(channel_name[-1]) - 1].get_raid_party()
            party_string = ""
            for member in party_members:
                cox_rank = member.cox_rank
                if cox_rank == "Teacher CoX":
                    party_string = party_string + member.rsn + " [TEACHER]\n"

            party_string = party_string + "\n"

            for member in party_members:
                cox_rank = member.cox_rank
                if cox_rank != "Teacher CoX":
                    party_string = party_string + member.rsn + ": " + str(
                        member.consecutive_raids) + "/" + str(
                        member.get_max_raids()) + " Consecutive Raids\n"
        else:
            party_string = "There are no teachers currently in this raid party"

    await ctx.channel.send(FORMAT_SYMBOLS + party_string + FORMAT_SYMBOLS)


@bot.command(name='showraid')
async def show_raid(ctx):
    channel_name = ctx.channel.name
    party_string = "You are not in a learner raids channel"
    if "learner-raids-" in channel_name:
        if len(global_raids_list[
                   int(channel_name[-1]) - 1].get_teachers()) != 0:
            party_members = global_raids_list[
                int(channel_name[-1]) - 1].get_raid_party()
            party_string = ""
            for member in party_members:
                cox_rank = member.cox_rank
                if cox_rank == "Teacher CoX":
                    party_string = party_string + member.rsn + " [TEACHER]\n"

            party_string = party_string + "\n"

            for member in party_members:
                cox_rank = member.cox_rank
                if cox_rank != "Teacher CoX":
                    party_string = party_string + member.rsn + ": " + str(
                        member.consecutive_raids) + "/" + str(
                        member.get_max_raids()) + " Consecutive Raids\n"
        else:
            party_string = "There is no raid in progress."

    await ctx.channel.send(FORMAT_SYMBOLS + party_string + FORMAT_SYMBOLS)


@bot.command(name='endraid')
@commands.has_role('Teacher CoX')
async def end_raid(ctx):
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].end_raid()

    await ctx.channel.send("Raid has ended")


@bot.command(name='teachers')
async def show_teachers(ctx):
    channel_name = ctx.channel.name
    output_string = "You are not in a learner raids channel."
    if "learner-raids-" in channel_name:
        teachers = global_raids_list[int(channel_name[-1]) - 1].get_teachers()
        output_string = "Current Teachers for This Channel: \n"
        if len(teachers) > 0:
            for teacher in teachers:
                output_string = output_string + teacher.rsn + "\n"
        else:
            output_string = output_string + "None."

    await ctx.channel.send(output_string)


@bot.command(name='cancelraid')
@commands.has_role('Teacher CoX')
async def cancel_raid(ctx):
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        global_raids_list[int(channel_name[-1]) - 1].cancel_raid()

    await ctx.channel.send("Raid has been cancelled")


@bot.command(name='remove')
@commands.has_role('Teacher CoX')
async def remove_user(ctx, rsn):
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        remove_result = global_raids_list[
            int(channel_name[-1]) - 1].remove_user(rsn)
        if remove_result[0] == True:
            if remove_result[1] == "party":
                output_string = rsn + " was removed from the raid party"
            if remove_result[1] == "queue":
                output_string = rsn + " was removed from the queue"
        else:
            output_string = "Could not find the user: " + rsn

    await ctx.channel.send(output_string)


@bot.command(name='leave')
async def leave_queue(ctx, rsn):
    if verify_rsn(rsn) == False:
        return
    channel_name = ctx.channel.name
    teacher_role = "Teacher CoX"
    return_string = "You are not in a learner raids channel."
    if "learner-raids-" in channel_name:
        channel_name = ctx.channel.name
        discord_name = str(ctx.author)
        roles = ctx.author.roles
        print(roles)
        is_teacher = False
        for role in roles:
            if role.name == teacher_role:
                is_teacher = True
        if is_teacher:
            if global_raids_list[int(channel_name[-1]) - 1].leave_teacher(rsn,
                                                                          discord_name):
                return_string = rsn + " has been removed as a teacher."
            else:
                return_string = rsn + " is not currently teaching."
        else:
            if global_raids_list[int(channel_name[-1]) - 1].leave_queue(rsn,
                                                                        discord_name):
                return_string = rsn + " has been removed from the queue."
            else:
                if global_raids_list[int(channel_name[-1]) - 1].scan_queue(
                        rsn):
                    return_string = rsn + " was not added by " + str(
                        discord_name)
                else:
                    return_string = rsn + " was not found in the queue."

    await ctx.channel.send(return_string)


@bot.command(name='showqueue')
async def show_queue(ctx):
    channel_name = ctx.channel.name
    if "learner-raids-" in channel_name:
        # current_raid_queue is a queue of raid member objects
        current_raid_queue = global_raids_list[
            int(channel_name[-1]) - 1].get_raid_queue()
        queue_output = ""
        queue_position = 1
        for element in current_raid_queue:
            queue_output = queue_output + str(
                queue_position) + ". " + element.rsn + ": "
            if element.get_max_raids() == 1:
                queue_output += "Qualifies for " + str(
                    element.get_max_raids()) + " Consecutive Raid" + "\n"
            else:
                queue_output += "Qualifies for " + str(
                    element.get_max_raids()) + " Consecutive Raids" + "\n"
            queue_position += 1

        if len(current_raid_queue) > 0:
            queue_output = FORMAT_SYMBOLS + queue_output + FORMAT_SYMBOLS
        else:
            queue_output = "The queue is empty"

        await ctx.channel.send(queue_output)


@bot.command(name='apply')
async def save_application(ctx, rsn, type=None, about_me="", force=None):
    channel = await bot.fetch_channel(797956922703347764)
    channel_test = await bot.fetch_channel(1062028387385888851)
    if (channel != ctx.channel) and (channel_test != ctx.channel):
        return
    application_received = ""
    account_type = "ironman"

    if type != "ironman":
        account_type = "main"

    if force == "force":
        force = True
    else:
        force = False

    user_data = get_user_data(rsn, account_type, force)

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
        bossing_points = calc_bossing(hiscore_list)

        raid_list = calc_raids(hiscore_list)
        # print(raid_list)
        raid_points = 0
        for raid in raid_list:
            if raid > 0:
                raid_points += raid

        cox_points = raid_list[0] + raid_list[1]
        tob_points = raid_list[2] + raid_list[3]
        toa_points = raid_list[4] + raid_list[5]

        total_pvm_points = raid_points + bossing_points

        total_xp = int(hiscore_list[0][2])
        total_xp_points = (total_xp // 250000)

        total_points = skill_points + clue_points + raid_points + \
                       bossing_points + total_xp_points

        date_today = datetime.datetime.today()
        if total_points >= TOTAL_POINTS_MIN:
            fileName = 'applications/' + rsn + ".txt"
            # print(fileName)
            myFile = open(fileName, 'w')
            fileContents = \
                '''RSN: %s
                About Me: %s
                Discord Name: %s
                Raids Points: %s
                CoX Points: %s
                ToB Points: %s
                ToA Points: %s
                Other bossing Points: %s
                Total PvM Points: %s
                Level Points: %s
                Exp Points: %s
                Total Points: %d
                    ''' % (
                    rsn, about_me, discord_name, raid_points,
                    str(cox_points), str(tob_points), str(toa_points),
                    bossing_points, str(total_pvm_points),
                    skill_points, total_xp_points, total_points) + str(
                    date_today)
            # print(discord_name)
            myFile.write(fileContents)
            myFile.close()

            # sends the file in the app review channel
            filePath = 'applications/' + rsn + ".txt"
            fileName = rsn + "_application.txt"
            discordFile = discord.File(filePath, filename=fileName)
            # application_received = "Your application has been submitted for review!"
            channel = bot.get_channel(798013179195162654)
            application_received = "Your application has been submitted for review!"

            # Get all CC role-related ranks
            Trialist = discord.utils.get(ctx.guild.roles, name='Trialist')
            Battlemage = discord.utils.get(ctx.guild.roles, name='Battlemage')
            Artillery = discord.utils.get(ctx.guild.roles, name='Artillery')
            Infantry = discord.utils.get(ctx.guild.roles, name='Infantry')
            Crusader = discord.utils.get(ctx.guild.roles, name='Crusader')
            Sniper = discord.utils.get(ctx.guild.roles, name='Sniper')
            Carry = discord.utils.get(ctx.guild.roles, name='Carry')
            Guthixian = discord.utils.get(ctx.guild.roles, name='Guthixian')
            Skiller = discord.utils.get(ctx.guild.roles, name='Skiller')
            Maxed = discord.utils.get(ctx.guild.roles, name='Maxed')

            # List that contains all role ranks
            role_list = [Trialist, Battlemage, Artillery, Infantry, Crusader,
                         Sniper, Carry, Guthixian, Skiller, Maxed]

            # Find if user has current rank in CC (and if so, what rank it is)
            for current_role in ctx.author.roles:
                if current_role in role_list:
                    # Send rank to app review channel
                    await channel.send(current_role)
            # Send application file to app review channel
            await channel.send(file=discordFile)


        elif total_points < TOTAL_POINTS_MIN:
            discord_name = ctx.author
            discord.AllowedMentions(everyone=True)
            discord_name = ctx.author
            ping_user = ctx.author.mention
            test = ("'*** test ***'")

            application_received = "Unfortunately, " + ping_user + " the OSRS account " + '**' + rsn + '**' + " does not meet the " \
                                                                                                              "minimum requirement of " + '**' + "100 total points" + '**' + " to apply to the Pinkopia CC. " \
                                   + "\n" + "Please resubmit your application once you fulfill this requirement! "
    await ctx.send(application_received)


@bot.command(name='accept')
@commands.has_role('Pinkopia Admin')
async def accept_application(ctx, rsn, new_role, old_role='None'):
    try:
        # Get new role from discord roles. Use these to add/remove roles
        new_role_disc = discord.utils.get(ctx.guild.roles, name=new_role)
        old_role_disc = "None"
        if old_role != "None":
            old_role_disc = discord.utils.get(ctx.guild.roles, name=old_role)

        # File path if user is new applicant
        if old_role == 'None':
            filePath = 'applications/' + rsn + '.txt'
        # File path is user is current applicant
        else:
            filePath = 'applications/' + old_role + '/' + rsn + '.txt'
            # print(filePath)

        # Get user's discord name from application file
        myFile = open(filePath, 'r')
        discord_name = myFile.readlines()[2].split(":")[1].strip()
        # print(discord_name)
        myFile.close()

        # Append date when user is eligible for increasing rank to file
        date_after_month = datetime.datetime.today() + relativedelta(months=1)
        formatted_date = date_after_month.strftime('%m/%d/%Y')

        # Read in all lines of application file
        # list to store file lines
        lines = []
        # read file
        myFile = open(filePath, 'r')
        # read an store all lines into list
        lines = myFile.readlines()
        myFile.close()

        # Delete last line of application (date) and replace with date one
        # month from acceptance
        myFile = open(filePath, 'w')
        for number, line in enumerate(lines):
            # delete line 5 and 8. or pass any Nth line you want to remove
            # note list index starts from 0
            if number not in [12]:
                myFile.write(line)
            else:
                myFile.write(formatted_date)
        myFile.close()

        # Get member object for the user applying
        discord_member = ctx.guild.get_member_named(discord_name)

        # Move application file depending on current role
        os.replace(filePath, 'applications/' + new_role + '/' + rsn + ".txt")

        # Remove old application
        # if old_role != "None":
        #    os.remove('applications/' + old_role + '/' + rsn + '.txt')

        # Add new role
        await discord_member.add_roles(new_role_disc)
        # Remove old role
        if old_role != "None":
            await discord_member.remove_roles(old_role_disc)

        # Notify user of new rank
        ping_user = discord_member.mention
        accept_msg = "Congrats " + ping_user + "! The osrs account " + '**' + rsn \
                     + '**' + " has just been ranked " + new_role + "!"
        channel = await bot.fetch_channel(797957000788180992)

    except Exception as e:
        print(e)
        raise e
    await channel.send(accept_msg)


@bot.command(pass_context=True)
@commands.has_role('Pinkopia Admin')
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []

    async for message in ctx.message.channel.history(limit=int(amount)):
        messages.append(message)
    await ctx.channel.delete_messages(messages)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("Missing Role")


# update the information in "how to rank up" channel and delete all previous messages
@bot.command(name='applychannelupdate')
@commands.has_role('Pinkopia Admin')
async def write_all_info(ctx, amount=None):
    # purge previous messages
    if amount is None:
        await ctx.channel.purge(limit=5)
    elif amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount))

    # updates the channel with information from how_to_rank_up.py
    await ctx.send(how_to_rank_up.general_info())
    # bossing points image
    f = open("how_to_rank_up_images/bossing.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    # skilling points image
    f = open("how_to_rank_up_images/skilling.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    # other points image
    f = open("how_to_rank_up_images/other.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    await ctx.send(how_to_rank_up.each_rank_reqs())
    # cc ranks image
    f = open("how_to_rank_up_images/rank_requirements.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    await ctx.send(how_to_rank_up.my_points())
    # example !points image
    f = open("how_to_rank_up_images/example_points.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    # full points example
    await ctx.channel.send(how_to_rank_up.my_full_points())
    f = open("how_to_rank_up_images/example_full_points.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()


if __name__ == '__main__':
    bot.run(TOKEN)
