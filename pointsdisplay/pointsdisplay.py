import PIL
from PIL import Image, ImageDraw, ImageFont
import math
import os
curdir = os.path.dirname(os.path.realpath(__file__))

class PointsImage:
    size = 15
    gap = 1
    def __init__(self):
        #obtain image dimensions
        self.image = PIL.Image.open(os.path.join(curdir, "pinkpoints.png"))
        self.width,self.height = self.image.size

        #get grid image
        self.base = Image.open(os.path.join(curdir, "pinkpoints.png")).convert("RGBA")

        #create transparent image for text
        self.txt = Image.new("RGBA", self.base.size, (255,255,255,0))


        
        
        self.size = 15
        self.gap = 1
                

        #get a font and select size
        self.fnt = ImageFont.truetype(os.path.join(curdir, "consola.ttf"), self.size)
        #get a drawing context
        self.d = ImageDraw.Draw(self.txt)



    #calculate half of string length in pixels
    @staticmethod
    def get_half_length(mystr):
        length = len(mystr)
        char_len = PointsImage.size/2
        half_length_size = math.ceil((length * (char_len)) / 2) + (char_len%2)/2
        return half_length_size
    @staticmethod
    def get_letter_length():
        char_len = PointsImage.size/2
        return char_len + PointsImage.gap

    #functions for what/where to draw text

    def draw_rsn(self, rsn):
        #draw text; specifying location, content, font, and color
        self.d.text(((self.width/2 - self.get_half_length(rsn)),self.height*.03), rsn, font =self.fnt, fill=((46,49,49,255)))
        
    #pvm_points = (cm, tob, raids, other)
    def draw_pvm_points_co1(self, pvm_points, ppstr = "PvM Points"):
        #specify location, content, font, and color of text
        #Header - PvM Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.18), ppstr, font =self.fnt, fill=((46,49,49,255)))
        #Raids Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.33), "Raids: {0:6d}".format(pvm_points[0]), font =self.fnt, fill=((46,49,49,255)))
        #CM Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr) + self.get_letter_length()),self.height*.43), "CM: {0:8d}".format(pvm_points[1]), font =self.fnt, fill=((46,49,49,255)))
        #ToB Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr) +self.get_letter_length()),self.height*.53), "ToB: {0:7d}".format(pvm_points[2]), font =self.fnt, fill=((46,49,49,255)))
        #Other Bossing Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.63), "Other: {0:6d}".format(pvm_points[3]), font =self.fnt, fill=((46,49,49,255)))
        
        #Check if total of all 4 GWD boss KCs >= 50
        #if pvm_points[4]:
         #   d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.73), "GWD KC:    Y", font =self.fnt, fill=((46,49,49,255)))
        #else:
         #   d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.73), "GWD KC:    N", font =self.fnt, fill=((46,49,49,255)))

        allpps = int(pvm_points[0])+int(pvm_points[3])
          
        #Total PvM Points        
        self.d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.73), "All: {0:8d}".format(allpps), font =self.fnt, fill=((46,49,49,255)))
        
    #skilling_points=[tlbonus=0, tepoints=0, allsps=0]    
    def draw_skilling_co2(self, skilling_points, spstr="Skill Points"):
        #specify location, content, font, and color of text
        #Header - Skilling Points
        self.d.text((self.width/2 - (self.get_half_length(spstr) - (self.get_half_length(spstr)/20)),self.height*.18), spstr, font =self.fnt, fill=((46,49,49,255)))
        #Total Level Points
        self.d.text(((self.width/2 - (self.get_half_length(spstr) - (self.get_half_length(spstr)/20))),self.height*.33), "Level: {0:5d}".format(skilling_points[0]), font =self.fnt, fill=((46,49,49,255)))
        #Total Exp Points
        self.d.text(((self.width/2 - (self.get_half_length(spstr) - (self.get_half_length(spstr)/20))),self.height*.43), "Exp: {0:7d}".format(skilling_points[1]), font =self.fnt, fill=((46,49,49,255)))
        #Total Skilling Points
        self.d.text(((self.width/2 - (self.get_half_length(spstr) - (self.get_half_length(spstr)/20))),self.height*.53), "All: {0:7d}".format(skilling_points[2]), font =self.fnt, fill=((46,49,49,255)))


    def draw_totalpoints_co3(self, allpoints, tpstr = "Total Points"):
        #specify location, content, font, and color of text
        #Header - Total Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/6)) - self.get_half_length(tpstr)),self.height*.18), tpstr, font =self.fnt, fill=((46,49,49,255)))
        #All Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/6)) - self.get_half_length(tpstr)),self.height*.33), "All: {0:7d}".format(allpoints), font =self.fnt, fill=((46,49,49,255)))    
        

    #draw text
    def draw_all_text(self, rsn="", allpoints=0, pvm_points=[0, 0, 0, 0], skilling_points=[0, 0, 0]):
        self.draw_rsn(rsn)
        self.draw_pvm_points_co1(pvm_points)
        self.draw_skilling_co2(skilling_points)
        self.draw_totalpoints_co3(allpoints)
        out = Image.alpha_composite(self.base, self.txt)

        out.save("saved_points.png", format=None)
        out.close()
        self.image.close()
        return "saved_points.png"
    
    
    

#draw line in the center of image
#shape = [(self.width/2, 0), (self.width/2,self.height)] 
#d.line(shape, fill ="red", width = 0) 
def test_drawing():
    buddy1 = PointsImage()
    buddy1.draw_all_text("poopmaster", allpoints=77777, pvm_points=[33, 22, 54, 11], skilling_points=[23243, 1243, 42])
    print(dir(buddy1))

    buddy2 = PointsImage()
    buddy2.draw_all_text("skinny    man", allpoints=11111, pvm_points=[121, 23432, 222, 4343], skilling_points=[123, 43, 42])