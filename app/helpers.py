import math
from datetime import datetime


def time_to_string(timestamp):
    a_time = int(timestamp)
    return datetime.utcfromtimestamp(a_time).strftime('%d/%m')


class Colour:

    def __init__(self, r, g, b):
        """
        Use this constructor to create a colour from RGB values.
        :usage Colour(0, 1, 1)
        :param r:
        :param g:
        :param b:
        """
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_hex_string(cls, hex_string):
        """
        Use this constructor to create a colour from a hex string
        :usage Colour('#A4B328')
        :param hex_string:
        """
        parts = cls.get_rgb_from_hex(hex_string)
        return cls(parts[0]//255, parts[1]//255, parts[2]//255)

    def __str__(self):
        return "R:" + str(self.r) + "\nG:" + str(self.g) + "\nB:" + str(self.b)

    def get_darker_shade(self):
        """
        This method will return a colour of a darker shade for the text
        so that text of the colour will be readable on the original BG colour
        """
        return Colour(self.r*0.75, self.g*0.75, self.b*0.75)

    @staticmethod
    def get_rgb_from_hex(hex_string):
        h = hex_string.replace("#", '')
        return [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)]

    @staticmethod
    def get_hex(n):
        chars = "0123456789ABCDEF"
        return chars[(n-n % 16)//16] + chars[(n % 16)]

    def convert_rgb_to_hex_string(self):
        r = math.ceil(self.r * 255)
        g = math.ceil(self.g * 255)
        b = math.ceil(self.b * 255)
        return "#" + self.get_hex(r) + self.get_hex(g) + self.get_hex(b)
