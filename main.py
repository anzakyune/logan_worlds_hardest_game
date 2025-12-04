"""

the worlds hardest game - deluxe

i wanted to make worlds hardest game have more complex mechanics such as 
bullet storage and speed changing parts, adding new mechanics for the player
to use.

sources --
Chris Cozort
Stack Overflow [misc fixes]

"""

import pygame as pg #imports pygame and changes the variable name to just pg, imports other libraries and files as well
from settings import * 
from sprites import *
from os import path
from utils import *
import random

class Game(): # creates a class with a name
    def __init__(self): # creates a method to initialize
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock() # creates a timer used for many thingssssss
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # creates screen
        pg.display.set_caption("declan's awesome game :D!!!!") #changes window title
        self.playing = True
        
    def get(self, image): # creates a function to make the image importing lines shorter, so it doesnt create a variable or lines - called get to minimize characters used
        return pg.image.load(path.join(self.img_folder, image+"_32.png")).convert_alpha()
    
    def load_data(self): # gives the game class a map property to parse the text file - level1.txt
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images') # searches through game files with path to find one with parsed name, this being 'images'
        self.lvl_folder = path.join(self.game_folder, 'levels')
        self.map = Map(path.join(self.lvl_folder, "level2.txt")) # creates a map through a utils class
        #sprite initialization
        self.player_img = pg.image.load(path.join(self.img_folder, "player_32x32.png")).convert_alpha() # searches through a folder for a certain image, and stores it with load()
        self.player_hit_img = pg.image.load(path.join(self.img_folder, "player_hit_32x32.png")).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, "mob_32x32.png")).convert_alpha()
        self.bg_img = pg.image.load(path.join(self.img_folder, "background_32x24.png")).convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))

    def new(self):
        self.load_data() # calls load data and creates maps
        self.all_sprites = pg.sprite.Group() # the sprite group allows us to update and draw sprite in groups and batches
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_boosts = pg.sprite.Group()
        # initializes the classes and creates a sprite
        self.high_score = 0
        # lists required to optimize lines, a key used to determine which wall sprite is started
        self.tile_list = ["B", "T", "R", "L", "E", "W", "M", "Z", "3", "4", "5", "6", "7", "8", "9", "0", "X", ",", "/", "<", ">",
                          "!", "@", "#", "$"]
        self.sprite_list = [self.get("wall_b"), self.get("wall_t"), self.get("wall_tr"), self.get("wall_tl"), self.get("wall_br"), self.get("wall_bl"), self.get("wall_lr"), self.get("wall_bt"),
                            self.get("wall_be"), self.get("wall_te"), self.get("wall_tle"), self.get("wall_tre"), self.get("wall_ble"), self.get("wall_bre"), self.get("wall_le"), self.get("wall_re"),
                            self.get("wall_full"), self.get("wall_blc"), self.get("wall_brc"), self.get("wall_tlc"), self.get("wall_trc"), self.get("wall_td"), self.get("wall_bd"), self.get("wall_ld"), self.get("wall_bd")]

        for row, tiles, in enumerate(self.map.data): # goes through each element in the file and determines if something should be created, creates it at defined position and scale
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, " ", 1, self.base_wall) # adds a normal wall
                elif tile == '2':
                    Wall(self, col, row, "breakable", 1, self.base_wall) # adds a breakable wall, different through state
                elif tile == 'c':
                    Coin(self, col, row)
                elif tile == 'p':
                    self.player = Player(self, col, row) # creates player from set tile in file
                elif tile == 'm':
                    Mob(self, col, row, "lr", 1)
                elif tile == 'b':
                    Boost(self, col, row, 2)
                elif tile == 's':
                    Boost(self, col, row, 0.5)
                elif tile == 'n':
                    Boost(self, col, row, 1)
                elif tile == "z":
                    BCollect(self, col, row)
                #walls
                for i, v in enumerate(self.tile_list): # enumerates through the list of characters used for walls and goes to a corresponding value in the list of sprites
                    if tile == v:
                        Wall(self, col, row, " ", 1, self.sprite_list[i])

    def draw_text(self, surface, text, size, color, x, y): # draws text using imput, pygame method
        font_name = pg.font.match_font('montserrat') # uses built-in pygame values
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color) #pygame function to render text
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y) # moves text into correct areas
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
        self.screen.blit(self.bg_img, (0, 0)) 
        self.all_sprites.draw(self.screen) # draws each sprite group, updating visuals
        self.all_mobs.draw(self.screen)
        self.all_coins.draw(self.screen)
        self.draw_text(self.screen, "health: "+str(self.player.health), 30, (0, 0, 0), 55, 5) # adds text to show values
        self.draw_text(self.screen, "score: "+str(self.player.score), 30, (0, 0, 0), 45, 25)
        self.draw_text(self.screen, "time: "+str(self.time), 30, (0, 0, 0), 45, 45)
        if self.player.health == 0: # when dead, close window 
            self.playing = False
            pg.quit()
        if self.player.health > 0:
            pg.display.flip() # double buffering, graphics handler 
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # timer value used for control of speed based on fps, so with lag you dont lose speed
            #input function
            self.events()
            #process function
            self.update()
            #output function
            self.draw()
        pg.quit()

if __name__ == "__main__":
    g = Game() # creating an instance for starting the Game class
    g.new()
    g.run()
