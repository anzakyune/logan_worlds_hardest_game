import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from random import choice
from utils import Cooldown as cd
from utils import Spritesheet
from os import path
vec = pg.math.Vector2

# sprites module, to keep everything separated and organized


class Bullet(Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE[0]/2, TILESIZE[1]/2))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.dir = direction
        self.vel = vec(0,0)
        self.pos = vec(x+(TILESIZE[0]/4), y+(TILESIZE[0]/4))
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.speed = 500
    def collide(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if hits[0].state == "breakable":
                hits[0].kill()
            self.kill()
    def update(self):
        if self.dir == "up":
            self.vel.y = -self.speed*self.game.dt
        elif self.dir == "down":
            self.vel.y = self.speed*self.game.dt
        elif self.dir == "left":
            self.vel.x = -self.speed*self.game.dt
        elif self.dir == "right":
            self.vel.x = self.speed*self.game.dt
        self.collide()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class DeathEffect(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.spritesheet = Spritesheet(path.join(self.game.img_folder, "spritesheet_anim.png"))
        self.load_images()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        self.current_frame = 0
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
    def animate(self):
        now = pg.time.get_ticks()
        self.current_frame = (self.current_frame+1) % len(self.standing_frames)
        bottom = self.rect.bottom
        self.image = self.standing_frames[self.current_frame]
        self.rect = self.image.get_rect
        self.rect.bottom = bottom
    def update(self):
        self.animate()

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.image = game.player_img
        self.rect = self.image.get_rect()
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE[0], y*TILESIZE[1])
        self.lastdir = "up"
        self.health = 100
        self.speed = 250
        self.score = 0
        self.cd = cd(1000)
        self.bcd = cd(250)
        self.speedmod = 1
        self.bulletstorage = 0
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt*self.speedmod
            self.lastdir = "up"
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt*self.speedmod
            self.lastdir = "left"
        if keys[pg.K_s]:
            self.vel.y = self.speed*self.game.dt*self.speedmod
            self.lastdir = "down"
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt*self.speedmod
            self.lastdir = "right"
        if keys [pg.K_SPACE]:
            if self.bulletstorage >= 1:
                if self.bcd.ready():
                    self.bcd.start()
                    Bullet(self.game, self.rect.x, self.rect.y, self.lastdir)
                    self.bulletstorage -= 1
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7
        
    def collide_with_walls(self, dir):
        if dir == "x": # checks direction variable
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False) # checks for collision with walls
            if hits:
                if self.vel.x > 0:
                    if hits[0].state == "pushable": # checks the state of the wall
                        hits[0].pos.x += self.vel.x # adds the velocity of the player to the wall's pos, moving it
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if hits[0].state == "pushable":
                        hits[0].pos.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    if hits[0].state == "pushable":
                        hits[0].pos.y += self.vel.y
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    if hits[0].state == "pushable":
                        hits[0].pos.y += self.vel.y
                    else:
                        self.pos.y = hits[0].rect.bottom 
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill) # checks for collision with the defined group
        if hits: #if collided
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
            if str(hits[0].__class__.__name__) == "Coin":
                self.score += 10
            if str(hits[0].__class__.__name__) == "BCollect":
                self.bulletstorage += 1
    def boostcheck(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            self.speedmod = hits[0].speed

    def update(self):
        self.get_keys()
        # checks for collision with walls, and sets position to appropriate values
        self.boostcheck(self.game.all_boosts, False)
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        self.collide(self.game.all_mobs, False)
        self.collide(self.game.all_coins, True)
        if not self.cd.ready():
            self.image = self.game.player_hit_img
        else:
            self.image = self.game.player_img

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        
        self.image = pg.Surface(TILESIZE)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        #self.rect.x = x * TILESIZE[0]
        #self.rect.y = y * TILESIZE[1]
        self.pos = vec(x*TILESIZE[0], y*TILESIZE[1])
        self.direction = False
        self.speed = 250
        self.vel = vec(choice([-1, 1]), choice([-1, 1]))
        print(self.vel.x)
    def collide_with_walls(self, dir): # same as player class
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= choice([-1, 1])
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom 
                self.rect.y = self.pos.y
                self.vel.y *= choice([-1, 1])
    def update(self):
        self.pos += self.vel*(self.speed*self.game.dt)
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        if self.game.player.vel.x > self.vel.x:
            pass
        else:
            pass
        #if self.rect.x >= WIDTH-32: # checks and changes direction
        #     self.direction = True
        #     self.rect.y += self.speed
        # if self.rect.x <= 0:
        #     self.direction = False
        #     self.rect.y += self.speed
        # if self.direction == False: # checks for direction, moves in appropriate way
        #     self.rect.x += self.speed
        # else:
        #     self.rect.x -= self.speed

class Boost(Sprite):
    def __init__(self, game, x, y, speed):
        self.game = game
        self.groups = game.all_sprites, game.all_boosts
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image.fill((255, 255, 87))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        self.speed = speed
    def update(self):
        pass

class Wall(Sprite):
    def __init__(self, game, x, y, state, weight, sprite):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image = sprite
        self.rect = self.image.get_rect()
        # self.rect.x = x*TILESIZE[0]
        # self.rect.y = y*TILESIZE[1]
        self.state = state
        self.weight = weight
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE[0], y*TILESIZE[1])
    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        if self.state == "moving":
            self.rect.x += 1

                    
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image.fill((255, 255, 87))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
    def update(self):
        pass

class BCollect(Sprite): #bullet collect
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image.fill((255, 255, 87))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
    def update(self):
        pass