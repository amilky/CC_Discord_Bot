import bot
import asyncio
from PIL import Image
import sys, importlib
import shutil
import random
import string

class Channel():
    async def send(str=None, file=None):
        if str is not None:
            print(str)
        if file is not None:
            #ew_file=''.join(random.choice(string.ascii_letters) for x in
            #                 range(10))+".png"
            #print(new_file)
            #input("WAIT4")
            #shutil.copyfile(file.filename, new_file)
            im = Image.open(file.filename)
            im.show()
            im.close()
            #input("WAIT2")
        return

class Context():
    def __init__(self):
        self.channel = Channel()
async def mainloop():
    while True:
        commandy = input("> ")
        if "p" == commandy:
            print("Reloaded!")
            importlib.reload(sys.modules['bot'])
            importlib.reload(sys.modules['pointsdisplay.pointsdisplay'])
            print("Equivalent of \"!points whm\"")
            ctx = Context()
            rsn = "whm"
            await bot.points(ctx, rsn)
        elif "!points" in commandy:
            ctx = Context()
            cl = commandy.split(" ")
            rsn = cl[1]
            await bot.points(ctx, rsn)
        elif "r" == commandy or "!reload" in commandy:
            print("Reloaded!")
            importlib.reload(sys.modules['bot'])
            importlib.reload(sys.modules['pointsdisplay.pointsdisplay'])
        elif "!exit" in commandy:
            print ("Quitting!")
            break
        else:
            print("Unrecognized command")
            
asyncio.run(mainloop())

'''
from CC_Discord_Bot directory: 'python harness.py'
"p" => shortcut for "!reload" and "!points whm"
"!points" => usage: !points *rsn*
"!reload" => reloads image and bot code
"r" => shortcut for "!reload"
"!exit" => exit harness
'''