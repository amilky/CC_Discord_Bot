import PIL
from PIL import Image, ImageDraw, ImageFont

#General Rank Information
def general_info():
    message = '''__**General Rank Information**__
-Rank is determined by how many *points* a player has.
-Points are based on progress in *PvM, skilling,* and *other* categories.
-The categories include the following activities:

**PvM - based on kill count (kc)**
-Raids:
---Chambers of Xeric (CoX)
---Challenge Mode - Chambers of Xeric (CM)
---Theatre of Blood (ToB)
-All other bosses

**Skilling **
-Total level - you will receive a fixed point boost at total level milestones, with an additional boost upon maxing.
-Experience points

**Other**
-Clues (beginner through master)
-Last Man Standing (LMS) points
-Soul Wars

Here is a more detailed breakdown of how you gain points:'''
    return message


#Requirements for Each Rank    
def each_rank_reqs():
    message = '''
-----------------
__**Requirements for Each Rank**__
-Points are the *minimum* criteria you need to be eligible to be considered for a rank. Other factors, such as time since joining the CC and activity, will also play a role.

-Following is a list of requirements to obtain each rank.

-Starting with the Sergeant rank, you will have a total point requirement, as well as additional point requirements within that total.
__Example:__ To obtain a Bronze rank, you will need 1,000 points, with 200 of those points belonging to the PvM category.'''
    return message

#How to Find My Points    
def my_points():
    message = '''
-----------------
__**How to Find My Points**__
-Feel free to check your points in #apply-requests.
-In order to find out how many points you currrently have, use the following command, without the brackets:
!points <username>
__Example:__ !points milkopia

*For usernames that include spaces:*
-Place quotes around the username
__Example:__ !points "lynx titan"

*For ironmen:*
-Add the word "ironman" after your username.
__Example:__ !points tradememilk ironman

The above commands will bring up an image displaying your points. Below is an example:'''

    return message