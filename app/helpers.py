import math

class Colour:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return "R:" + str(self.r) + "\nG:" + str(self.g) + "\nB:" + str(self.b)

    def getDarkerShade(self):
        '''
        This method will return a colour of a darker shade for the text
        so that text of the colour will be readable on the original BG colour
        '''
        return Colour(self.r*0.75, self.g*0.75, self.b*0.75)
    
    def getHex(self, n):
        chars = "0123456789ABCDEF"
        return chars[(n-n%16)//16] + chars[(n%16)]

    def convertRGBToHexString(self):
        r = math.ceil(self.r * 255)
        g = math.ceil(self.g * 255)
        b = math.ceil(self.b * 255)
        return "#" + self.getHex(r) + self.getHex(g) + self.getHex(b)