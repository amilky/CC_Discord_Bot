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
---Theatre of Blood Hard Mode
--Tombs of Amascut normal
--Tombs of Amascut expert
-All other bosses

**Skilling **
-Total level - you will receive a fixed point boost at total level milestones, with an additional boost upon maxing.
--Ironmen receive a 10% bonus to their total level points
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
-Points are the *minimum* criteria you need to be eligible to be considered for a rank.
-You can only rank up once per month, and you can't skip any ranks.
--A higher rank is associated with higher trust and more time spent in the 
CC, so these factors play a role as well.

-The ranks are not entirely linear. If you enjoy focusing more on skilling (
or just like the title better), you can choose one of the two skiller focused ranks (Skiller or Maxed), as long as you meet the requirements.

-Following is a list of requirements to obtain each rank.
__Example:__ To obtain the rank of Infantry, you need 4000 points, with at 
least 600 of those points being PvM points and at least 250 of those PvM 
points coming from raids.'''
    return message

#How to Find My Points    
def my_points():
    message = '''
-----------------
__**How to Find My Points**__
-Feel free to check your points in #check-my-points.
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