from settings import *
import pygame as pg

# creates a class that reads the text file and converts it into a list.
class Map():
    def __init__(self, filename):
        # creates empty list to append map data to
        self.data = []
        with open(filename, 'rt') as f: # opens a file as a text reader without the need to close it
            for line in f:
                self.data.append(line.strip())
        # creates properties of map
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE[0]
        self.height = self.tileheight * TILESIZE[1]   

class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.time:
            return True
        return False
    
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image