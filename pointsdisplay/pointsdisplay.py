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
        self.image = PIL.Image.open(os.path.join(curdir,
                                                 "points_display_basic.png"))
        self.width,self.height = self.image.size

        #get grid image
        self.base = Image.open(os.path.join(curdir,
                                            "points_display_basic.png")).convert("RGBA")

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
        self.d.text(((self.width/2 - self.get_half_length(rsn)),
                     self.height*.01), rsn, font =self.fnt, fill=((46,49,49,
                                                                   255)))
        
    #pvm_points = (cm, tob, toa, raids total, other)
    def draw_pvm_points_co1(self, pvm_points, ppstr = "PvM Points"):
        #specify location, content, font, and color of text
        #Header - PvM Points
        self.d.text(((self.width/6 - self.get_half_length(ppstr) +
                      self.get_letter_length() - 6),self.height*.135), ppstr,
                    font =self.fnt, fill=((46,49,49,255)))
        #Raids Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr)) - 4,
                     self.height*.25), "Raids: {0:6d}".format(pvm_points[0]),
                    font =self.fnt, fill=((46,49,49,255)))
        #CoX Points
        total_cox = pvm_points[1] + pvm_points[2]
        self.d.text(((self.width/7 - self.get_half_length(ppstr) +
                      self.get_letter_length()) - 4,self.height*.32),
                    "CoX: {0:7d}".format(total_cox), font =self.fnt,
                    fill=((46,49,49,255)))
        #ToB Points
        total_tob = pvm_points[3] + pvm_points[4]
        self.d.text(((self.width/7 - self.get_half_length(ppstr) +
                      self.get_letter_length()) - 4,self.height*.398),
                    "ToB: {0:7d}".format(total_tob), font =self.fnt,
                    fill=((46,49,49,255)))
        # ToA Points
        total_toa = pvm_points[5] + pvm_points[6]
        self.d.text(((self.width / 7 - self.get_half_length(
            ppstr) + self.get_letter_length()) - 4, self.height * .47),
                    "ToA: {0:7d}".format(total_toa), font=self.fnt,
                    fill=((46, 49, 49, 255)))
        #Other Bossing Points
        self.d.text(((self.width/7 - self.get_half_length(ppstr)) - 4,
                     self.height*.56), "Bosses: {0:5d}".format(pvm_points[7]),
                    font =self.fnt, fill=((46,49,49,255)))
        
        #Check if total of all 4 GWD boss KCs >= 50
        #if pvm_points[4]:
         #   d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.73), "GWD KC:    Y", font =self.fnt, fill=((46,49,49,255)))
        #else:
         #   d.text(((self.width/7 - self.get_half_length(ppstr)),self.height*.73), "GWD KC:    N", font =self.fnt, fill=((46,49,49,255)))

        # pvm_points[0] = raids points // pvm_pionts[7] = other bossing points
        allpps = int(pvm_points[0])+int(pvm_points[7])
          
        #Total PvM Points        
        self.d.text(((self.width/7 - self.get_half_length(ppstr)) - 4,
                     self.height*.687), "All: {0:8d}".format(allpps),
                    font =self.fnt, fill=((46,49,49,255)))

    #skilling_points=[tlbonus=0, tepoints=0, allsps=0]    
    def draw_skilling_co2(self, skilling_points, spstr="Skill Points"):
        #specify location, content, font, and color of text
        #Header - Skilling Points
        self.d.text((self.width/2 - (self.get_half_length(spstr) - (
                self.get_half_length(spstr) - (self.get_half_length(
            spstr)))),self.height*.135), spstr,
                    font =self.fnt, fill=((46,49,49,255)))
        #Total Level Points
        self.d.text((self.width/2 - (self.get_half_length(spstr) - (
                self.get_half_length(spstr) - (self.get_half_length(
            spstr)*1.1))),self.height*.25), "Level: {0:6d}".format(
            skilling_points[0]), font =self.fnt, fill=((46,49,49,255)))
        #Total Exp Points
        self.d.text((self.width/2 - (self.get_half_length(spstr) - (
                self.get_half_length(spstr) - (self.get_half_length(
            spstr)*1.1))),self.height*.32), "Exp: {0:8d}".format(
            skilling_points[1]), font =self.fnt, fill=((46,49,49,255)))
        #Total Skilling Points
        self.d.text((self.width/2 - (self.get_half_length(spstr) - (
                self.get_half_length(spstr) - (self.get_half_length(
            spstr)*1.1))),self.height*.47), "All: {0:8d}".format(
            skilling_points[2]), font =self.fnt, fill=((46,49,49,255)))
    
    #Other points
    def draw_other_points_co3(self, other_points, otherptstr = "Other Points"):
        #specify location, content, font, and color of text
        #Header - Other Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/8) - (
                self.get_letter_length() + 7)) - self.get_half_length(
            otherptstr)),self.height*.135), otherptstr, font =self.fnt,
                    fill=((46,49,49,255)))
        #Clue Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/8)) -
                      self.get_half_length(otherptstr)*1.5),
                     self.height*.25), "Clues: {0:5d}".format(other_points[
                                                                                      0]), font =self.fnt, fill=((46,49,49,255)))
        #LMS Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/8)) -
                      self.get_half_length(otherptstr)*1.5),
                     self.height*.32), "Misc: {0:6d}".format(other_points[1]),
                    font =self.fnt, fill=((46,49,49,255)))
        
        allotherpts = int(other_points[0])+int(other_points[1])
        
        #Total Other Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/8)) -
                      self.get_half_length(otherptstr)*1.5),
                     self.height*.47), "All: {0:7d}".format(allotherpts),
                    font =self.fnt, fill=((46,49,49,255)))

    #Total Points
    def draw_totalpoints_co3(self, allpoints, tpstr = "Total Points"):
        #specify location, content, font, and color of text
        #Header - Total Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/6) - (
                self.get_letter_length()/2)) - self.get_half_length(tpstr)),
                     self.height*.79), tpstr, font =self.fnt, fill=((46,49,49,
                                                                    255)))
        #All Points
        self.d.text((((self.width/2)+((self.width/2)-(self.width/6)) -
                      self.get_half_length(tpstr)),self.height*.87),
                    "{0:7d}".format(allpoints), font =self.fnt, fill=((46,49,49,255)))
        

    #draw text
    def draw_all_text(self, rsn="", allpoints=0, pvm_points=[0, 0, 0, 0], skilling_points=[0, 0, 0], other_points=[0, 0]):
        self.draw_rsn(rsn)
        self.draw_pvm_points_co1(pvm_points)
        self.draw_skilling_co2(skilling_points)
        self.draw_other_points_co3(other_points)
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