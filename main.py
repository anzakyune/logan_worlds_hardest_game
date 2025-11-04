# input
# update
# draw

import pygame as pg #imports pygame and changes the variable name to just pg
from settings import * 
from sprites import *
from os import path
from utils import *
import random

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
        self.base_wall_img = pg.image.load(path.join(self.img_folder, "new_wall_32.png")).convert_alpha()
        self.player_hit_img = pg.image.load(path.join(self.img_folder, "player_hit_32x32.png")).convert_alpha()

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
                    Wall(self, col, row, " ", 1)
                elif tile == '2':
                    Wall(self, col, row, "breakable", 1)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
                elif tile == 'B':
                    Boost(self, col, row, 2)
                elif tile == 'S':
                    Boost(self, col, row, 0.5)
                elif tile == 'N':
                    Boost(self, col, row, 1)
                elif tile == "Z":
                    BCollect(self, col, row)
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
