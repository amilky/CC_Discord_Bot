# bot.py
#we import os so we can access environment variables
#class that allows you to interact with the operating system
FORMAT_SYMBOLS = "```"
TOTAL_POINTS_MIN = 100

import os
from os import path
import random
import datetime
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

from pointsdisplay import pointsdisplay
from threading import Lock
image_file_lock = Lock()

import how_to_rank_up

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
    cox_points = 0
    cm_points = 0
    tob_points = 0
    placeHolder = 0
    cox_kc = int(hiscore_list[42][1])
    cm_cox_kc = int(hiscore_list[43][1])
    tob_kc = int(hiscore_list[70][1])

    raid_list = []
    #print(cox_kc)
    #print(cm_cox_kc)
    #print(tob_kc)
    if cox_kc > 0:
        cox_points += cox_kc
        raid_list.append(cox_points)
    else:
        raid_list.append(placeHolder)
    if cm_cox_kc > 0:
        cm_points += cm_cox_kc * 3
        raid_list.append(cm_points)
    else:
        raid_list.append(placeHolder)
    if tob_kc > 0:
        tob_points += tob_kc * 2
        raid_list.append(tob_points)
    else:
        raid_list.append(placeHolder)

    #print(raid_list)
    return raid_list

def calc_lms(hiscore_list):
    points = 0
    lms_kc = int(hiscore_list[34][1])
    if lms_kc > 0:
        points = (lms_kc - 500) // 10

    return points

def calc_soulWars(hiscore_list):
    points = 0
    soulWars_kc = int(hiscore_list[35][1])
    if soulWars_kc > 0:
        points = (soulWars_kc - 500) // 10

    return points

def calc_bossing(hiscore_list):
    boss_points = 0

    gwd_dict = {"Commander Zilyana": int(hiscore_list[46][1]), "General Graardor": int(hiscore_list[53][1]),
                "Kree'Arra": int(hiscore_list[60][1]), "K'ril Tsutsaroth": int(hiscore_list[61][1])}

    gwd_points = 0
    for key in gwd_dict:
        #print(gwd_dict[key])
        if gwd_dict[key] > 0:
            #print(gwd_points)
            gwd_points += gwd_dict[key]

    boss_points += gwd_points // 10
    print(gwd_points)
    #print(boss_points)


    #GROUP A POINTS
    boss_A_dict = {"Abyssal Sire": int(hiscore_list[36][1]),"Alchemical Hydra": int(hiscore_list[37][1]),
                   "Callisto": int(hiscore_list[40][1]), "Cerberus": int(hiscore_list[41][1]), "Venenatis":
                    int(hiscore_list[74][1]), "Vet'ion": int(hiscore_list[75][1]), "Vorkath": int(hiscore_list[76][1]),
                   "Zulrah": int(hiscore_list[79][1])}

    boss_A_points = 0
    for key in boss_A_dict:
        #print(boss_A_dict, "kc", boss_A_dict[key])
        if boss_A_dict[key] > 0:
            boss_A_points += boss_A_dict[key]

    boss_points += boss_A_points // 20
    print(boss_A_points)

    #GROUP B POINTS
    boss_B_dict = {"Chaos Elemental": int(hiscore_list[44][1]), "Chaos Fanatic": int(hiscore_list[45][1]),
                     "Dagannoth Prime": int(hiscore_list[49][1]), "Dagannoth_Rex": int(hiscore_list[50][1]),
                     "Dagannoth Supreme": int(hiscore_list[51][1]), "Giant Mole": int(hiscore_list[54][1]),
                     "Grotesque Guardians": int(hiscore_list[55][1]), "Kalphite Queen": int(hiscore_list[57][1]),
                     "King Black Dragon": int(hiscore_list[58][1]), "Kraken": int(hiscore_list[59][1]), "Sarachnis":
                      int(hiscore_list[65][1]), "Scorpia": int(hiscore_list[66][1]), "Thermonuclear Smoke Devil":
                      int(hiscore_list[71][1]), "Zalcano": int(hiscore_list[78][1])}

    print("Sarachnis",int(hiscore_list[65][1]) )
    print("Scorpia", int(hiscore_list[66][1]))


    boss_B_points = 0
    for key in boss_B_dict:
        #print(boss_B_dict, "kc", boss_B_dict[key])
        if boss_B_dict[key] > 0:
            boss_B_points += boss_B_dict[key]

    boss_points += boss_B_points // 50
    print(boss_B_points)
    print(boss_B_dict)

    #GROUP C POINTS
    boss_C_dict = {"Barrows Chests": int(hiscore_list[38][1]),"Crazy Archaeologist": int(hiscore_list[48][1]),
                   "Deranged Archaeologist": int(hiscore_list[52][1]), "Wintertodt": int(hiscore_list[77][1])}

    boss_C_points = 0
    for key in boss_C_dict:
        #print(boss_C_dict, "kc", boss_C_dict[key])
        if boss_C_dict[key] > 0:
            boss_C_points += boss_C_dict[key]

    boss_points += boss_C_points // 80
    print(boss_C_points)
    #print(boss_C_dict["Deranged Archaeologist"])
    #print(boss_C_dict["Deranged Archaeologist"])
    #print(boss_points)

    skotizo_kc = int(hiscore_list[67][1])
    if skotizo_kc > 0:
        boss_points += skotizo_kc // 3
    print("skotizo", skotizo_kc)

    obor_kc = int(hiscore_list[64][1])
    if obor_kc > 0:
        boss_points += obor_kc // 10
    print("obor", obor_kc)


    bryophyta_kc = int(hiscore_list[39][1])
    if bryophyta_kc > 0:
        boss_points += bryophyta_kc // 10
    print("bryophyta_kc", bryophyta_kc)

    mimic_kc = int(hiscore_list[62][1])
    if mimic_kc > 0:
        boss_points += mimic_kc
    print("mimic_kc", mimic_kc)

    hespori_kc = int(hiscore_list[56][1])
    if hespori_kc > 0:
        boss_points += hespori_kc // 5
    print("hespori", hespori_kc)

    nightmare_kc = int(hiscore_list[63][1])
    if nightmare_kc > 0:
        boss_points += nightmare_kc // 5
    print("nightmare_kc", nightmare_kc)


    gauntlet_kc = int(hiscore_list[68][1])
    if gauntlet_kc > 0:
        boss_points += gauntlet_kc // 5
    print("gauntlet_kc", gauntlet_kc)

    corrupted_gauntlet_kc = int(hiscore_list[69][1])
    if corrupted_gauntlet_kc > 0:
        boss_points += corrupted_gauntlet_kc // 3
    print("corrupted_gauntlet_kc", corrupted_gauntlet_kc)

    jad_kc = int(hiscore_list[73][1])
    if jad_kc > 0:
        boss_points += jad_kc
    print("jad_kc", jad_kc)

    zuk_kc = int(hiscore_list[72][1])
    if zuk_kc > 0:
        boss_points += zuk_kc * 9
    print("zuk_kc", zuk_kc)
    print(boss_points)
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

        #print(int(hiscore_list[35][1]))
        #querying total xp from website
        total_xp = int(hiscore_list[0][2])
        #calculating total EXP points
        total_xp_points = (total_xp // 250000)
        #adds total xp points to total points
        total_points += total_xp_points
        total_xp_points_str = "Total EXP points: " + str(total_xp_points)

        #calculating skilling points
        skilling_points = calc_skilling(hiscore_list, account_type)
        #adds skilling points to total points
        total_points += skilling_points
        skilling_points_str = "Skilling points: " + str(skilling_points)

        #calculating clue points
        clue_points = calc_clue(hiscore_list)
        if clue_points > 0:
            #adds clue points to total points
            total_points += clue_points
        else:
            clue_points = 0
        clue_points_str = "Clue points: " + str(clue_points)

        #calculating lms points
        lms_points = calc_lms(hiscore_list)
        if lms_points > 0:
            total_points += lms_points
        else:
            lms_points = 0

        #calculating soul wars points
        #soulWars_points = calc_soulWars(hiscore_list)
        #if soulWars_points > 0:
            #total_points += soulWars_points
        #else:
            #soulWars_points = 0



        # calculating raid points
        raid_list = calc_raids(hiscore_list)
        #print(raid_list)
        raid_points = 0
        for raid in raid_list:
            if raid > 0:
                raid_points += raid
        total_points += raid_points
        raid_points_str = "Raid points: " + str(raid_points)
        cox_points = raid_list[0]
        cox_points_str = "  COX_points: " + str(cox_points)
        cm_points = raid_list[1]
        cm_points_str = "  CM_points: " + str(cm_points)
        tob_points = raid_list[2]
        tob_points_str = "  TOB_points: " + str(tob_points)



        #calculating bossing points
        bossing_points = calc_bossing(hiscore_list)
        total_points += bossing_points
        bossing_points_str = "Bossing points: " + str(bossing_points)

        total_points_str = "Total points: " + str(total_points)

        user = f"User: " + rsn

        big_string = FORMAT_SYMBOLS + user + "\n" + total_xp_points_str + "\n" + skilling_points_str + "\n" + clue_points_str + "\n" + \
                     raid_points_str + "\n" + cox_points_str + "\n" + cm_points_str + "\n" + tob_points_str + "\n" + bossing_points_str + "\n" + total_points_str + FORMAT_SYMBOLS

    
    
        raids_tuple = calc_raids(hiscore_list)

        print()

        cm_pts = raids_tuple[1]
        tob_pts = raids_tuple[2]
        raids_pts = raids_tuple[0]+cm_pts+tob_pts
        #await ctx.send(total_level)
        #pvm_points = (cm, tob, raids, other)
        #skilling_points=[tlbonus=0, tepoints=0, allsps=0] 
        image_file_lock.acquire()
        player = pointsdisplay.PointsImage()
        image_file = player.draw_all_text(rsn, 
            total_points, 
            pvm_points=[raid_points, cm_points, tob_points, bossing_points], 
            skilling_points=[skilling_points, total_xp_points, skilling_points+total_xp_points])
            
        await ctx.channel.send(file=discord.File(image_file))
        os.remove(image_file)
        image_file_lock.release()



@bot.command(name='apply')
async def save_application(ctx, rsn, type=None, about_me="", force=None):
    channel = await bot.fetch_channel(797956922703347764)
    if channel != ctx.channel:
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
        raid_points = calc_raids(hiscore_list)
        bossing_points = calc_bossing(hiscore_list)

        raid_list = calc_raids(hiscore_list)
        #print(raid_list)
        raid_points = 0
        for raid in raid_list:
            if raid > 0:
                raid_points += raid

        total_xp = int(hiscore_list[0][2])
        total_xp_points = (total_xp // 250000)

        total_points = skill_points + clue_points + raid_points + bossing_points + total_xp_points

        if total_points >= TOTAL_POINTS_MIN:
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
            #print(discord_name)
            myFile.write(fileContents)
            myFile.close()

            #sends the file in the app=review channel
            filePath = 'applications/' + rsn + ".txt"
            fileName = rsn + "_application.txt"
            discordFile = discord.File(filePath, filename=fileName)
            #application_received = "Your application has been submitted for review!"
            channel = bot.get_channel(798013179195162654)
            application_received = "Your application has been submitted for review!"
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
async def accept_application(ctx, rsn, role_name="Trial"):

    if role_name == "Trial":
        role_name = "Trial Member"

    #needs exact role name to get from discord
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role_name != "Trial Member":
        filePath = 'applications/Trial/' + rsn + ".txt"
    else:
        filePath = 'applications/' + rsn + ".txt"

    myFile = open(filePath, 'r')
    discord_name = myFile.readlines()[2].split(":")[1].strip()
    print(discord_name)
    myFile.close()

    #getting member object of the person with discord name in application file
    discord_member = ctx.guild.get_member_named(discord_name)
    ping_user = discord_member.mention
    await discord.Member.add_roles(discord_member, role)

    if role_name == "Trial Member":
        os.replace('applications/' + rsn + ".txt", 'applications/Trial/' + rsn + ".txt")

    if role_name == "Captain":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Captain/' + rsn + ".txt")

    elif role_name == "Corporal":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Corporal/' + rsn + ".txt")

    elif role_name == "General":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/General/' + rsn + ".txt")

    elif role_name == "Sergeant":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Sergeant/' + rsn + ".txt")

    elif role_name == "Friend":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Friend/' + rsn + ".txt")

    elif role_name == "Lieutenant":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Lieutenant/' + rsn + ".txt")

    elif role_name == "Recruit":
        os.replace('applications/Trial/' + rsn + ".txt", 'applications/Recruit/' + rsn + ".txt")

    accept_msg = "Congrats " + ping_user + "! The osrs account " + '**' + rsn + '**' + " has just been ranked " + role_name + "!"
    channel = await bot.fetch_channel(797957000788180992)
    print("Got Channel")
    await channel.send(accept_msg)

@bot.command(pass_context = True)
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



#update the information in "how to rank up" channel and delete all previous messages
@bot.command(name='applychannelupdate')
async def write_all_info(ctx, amount=None):
#purge previous messages
    if amount is None:
        await ctx.channel.purge(limit=5)
    elif amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount))
        
#updates the channel with information from how_to_rank_up.py
    await ctx.send(how_to_rank_up.general_info())
    #bossing points image
    f = open("how_to_rank_up_images/bossing.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    #skilling points image
    f = open("how_to_rank_up_images/skilling.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    #other points image
    f = open("how_to_rank_up_images/other.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    await ctx.send(how_to_rank_up.min_reqs_to_join())
    await ctx.send(how_to_rank_up.each_rank_reqs())
    #cc ranks image
    f = open("how_to_rank_up_images/rank_requirements.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()
    await ctx.send(how_to_rank_up.my_points())  
    #example !points image
    f = open("how_to_rank_up_images/example_points.png", "rb")
    await ctx.channel.send(file=discord.File(f))
    f.close()    
    await ctx.send(how_to_rank_up.initial_apply())  


bot.run(TOKEN)
