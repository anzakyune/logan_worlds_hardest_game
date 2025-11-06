"""

the worlds hardest game - deluxe
inspired by worlds hardest game.. duh

sources --
Chris Cozort

"""
# input
# update
# draw

import pygame as pg #imports pygame and changes the variable name to just pg
from settings import * 
from sprites import *
from os import path
from utils import *
import random

def imageimport(eximage, img_folder): # creates a function to make the image importing lines shorter
    return pg.image.load(path.join(img_folder, eximage)).convert_alpha()

class Game(): # creates a class with a name
    def __init__(self): # creates a method to initialize
        pg.init()
        self.clock = pg.time.Clock() # creates a timer used for many thingssssss
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # creates screen
        pg.display.set_caption("declan's awesome game :D!!!!") #changes window title
        self.playing = True
    
    def load_data(self): # gives the game class a map property to parse the text file - level1.txt
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.map = Map(path.join(self.game_folder, "level1.txt"))
        #sprite initialization
        self.player_img = pg.image.load(path.join(self.img_folder, "player_32x32.png")).convert_alpha()
        self.player_hit_img = pg.image.load(path.join(self.img_folder, "player_hit_32x32.png")).convert_alpha()
        # WALLS
        self.base_wall = imageimport("wall_base_32.png", self.img_folder) # creates all the sprites from the folder. used to make different tiles so it looks nicer
        self.wall_b = imageimport("wall_b_32.png", self.img_folder)
        self.wall_t = imageimport("wall_t_32.png", self.img_folder)
        self.wall_bl = imageimport("wall_bl_32.png", self.img_folder)
        self.wall_br = imageimport("wall_br_32.png", self.img_folder)
        self.wall_tl = imageimport("wall_tl_32.png", self.img_folder)
        self.wall_tr = imageimport("wall_tr_32.png", self.img_folder)
        self.wall_lr = imageimport("wall_lr_32.png", self.img_folder)
        self.wall_bt = imageimport("wall_bt_32.png", self.img_folder)
        self.wall_be = imageimport("wall_be_32.png", self.img_folder)
        self.wall_te = imageimport("wall_te_32.png", self.img_folder)
        self.wall_tre = imageimport("wall_tre_32.png", self.img_folder)
        self.wall_tle = imageimport("wall_tle_32.png", self.img_folder)
        self.wall_bre = imageimport("wall_bre_32.png", self.img_folder)
        self.wall_ble = imageimport("wall_ble_32.png", self.img_folder)
        self.wall_le = imageimport("wall_le_32.png", self.img_folder)
        self.wall_re = imageimport("wall_re_32.png", self.img_folder)
        self.wall_full = imageimport("wall_full_32.png", self.img_folder)
        self.wall_trc = imageimport("wall_blc_32.png", self.img_folder)
        self.wall_tlc = imageimport("wall_brc_32.png", self.img_folder)
        self.wall_blc = imageimport("wall_trc_32.png", self.img_folder)
        self.wall_brc = imageimport("wall_tlc_32.png", self.img_folder)

    def new(self):
        self.load_data() # calls load data and creates maps
        self.all_sprites = pg.sprite.Group() # the sprite Group allows us to update and draw sprite in groups and batches
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_boosts = pg.sprite.Group()
        # initializes the classes and creates a sprite
        self.high_score = 0
        
        for row, tiles, in enumerate(self.map.data): # goes through each element in the file and determines if something should be created
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, " ", 1, self.base_wall)
                elif tile == '2':
                    Wall(self, col, row, "breakable", 1, self.base_wall)
                elif tile == 'c':
                    Coin(self, col, row)
                elif tile == 'p':
                    self.player = Player(self, col, row)
                elif tile == 'm':
                    Mob(self, col, row)
                elif tile == 'b':
                    Boost(self, col, row, 2)
                elif tile == 's':
                    Boost(self, col, row, 0.5)
                elif tile == 'n':
                    Boost(self, col, row, 1)
                elif tile == "z":
                    BCollect(self, col, row)
                #walls
                elif tile == "B": # repition of the different wall types, really stupid and annoying
                    Wall(self, col, row, " ", 1, self.wall_b)
                elif tile == "T":
                    Wall(self, col, row, " ", 1, self.wall_t)
                elif tile == "R":
                    Wall(self, col, row, " ", 1, self.wall_tr)
                elif tile == "L":
                    Wall(self, col, row, " ", 1, self.wall_tl)
                elif tile == "E":
                    Wall(self, col, row, " ", 1, self.wall_br)
                elif tile == "W":
                    Wall(self, col, row, " ", 1, self.wall_bl)
                elif tile == "M":
                    Wall(self, col, row, " ", 1, self.wall_lr)
                elif tile == "Z":
                    Wall(self, col, row, " ", 1, self.wall_bt)
                elif tile == "3":
                    Wall(self, col, row, " ", 1, self.wall_be)
                elif tile == "4":
                    Wall(self, col, row, " ", 1, self.wall_te)
                elif tile == "5":
                    Wall(self, col, row, " ", 1, self.wall_tle)
                elif tile == "6":
                    Wall(self, col, row, " ", 1, self.wall_tre)
                elif tile == "7":
                    Wall(self, col, row, " ", 1, self.wall_ble)
                elif tile == "8":
                    Wall(self, col, row, " ", 1, self.wall_bre)
                elif tile == "9":
                    Wall(self, col, row, " ", 1, self.wall_le)
                elif tile == "0":
                    Wall(self, col, row, " ", 1, self.wall_re)
                elif tile == "X":
                    Wall(self, col, row, " ", 1, self.wall_full)
                elif tile == ",":
                    Wall(self, col, row, " ", 1, self.wall_blc)
                elif tile == "/":
                    Wall(self, col, row, " ", 1, self.wall_brc)
                elif tile == "<":
                    Wall(self, col, row, " ", 1, self.wall_tlc)
                elif tile == ">":
                    Wall(self, col, row, " ", 1, self.wall_trc)
                

    def draw_text(self, surface, text, size, color, x, y): # draws text using imput, pygame method
        font_name = pg.font.match_font('montserrat')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    def events(self):
        # when quit, close window
        for event in pg.event.get(): # event listener, checks a list
            if event.type == pg.QUIT: # when window is closed, listens for the quit event
                print("this is happening")
                self.playing = False
    def input(self):
        pass
    def update(self):
        # updates the positions for the sprites
        self.all_sprites.update()
        seconds = pg.time.get_ticks()//1000
        countdown = 10
        self.time = countdown - seconds
    def draw(self):
        # draws the sprites
        self.screen.fill((255, 255, 255)) # fills screen color
        self.all_sprites.draw(self.screen)
        self.all_mobs.draw(self.screen)
        self.all_coins.draw(self.screen)
        self.draw_text(self.screen, "health: "+str(self.player.health), 30, (0, 0, 0), 55, 5)
        self.draw_text(self.screen, "score: "+str(self.player.score), 30, (0, 0, 0), 45, 25)
        self.draw_text(self.screen, "time: "+str(self.time), 30, (0, 0, 0), 45, 45)
        if self.player.health == 0:
            self.playing = False
            pg.quit()
        if self.player.health > 0:
            pg.display.flip() # double buffering, graphics handler 
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            #input
            self.events()
            #process
            self.update()
            #output
            self.draw()
        pg.quit()

if __name__ == "__main__":
    g = Game() # creating an instance for starting the Game class
    g.new()
    g.run()
