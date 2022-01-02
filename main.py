import pygame as pg
import math
import random
import time
from utils import scale_image
from utils import blit_rotate_center

GRASS = scale_image(pg.image.load("Media/grass.jpg"),2.5)
TRACK = scale_image(pg.image.load("Media/track.png"),0.9)
TRACK_BORDER = scale_image(pg.image.load("Media/track-border.png"),0.9) 
TRACK_BORDER_MASK = pg.mask.from_surface(TRACK_BORDER) #getting a mask of the track border
FINISH = pg.image.load("Media/finish2.png")
FINISH_MASK = pg.mask.from_surface(FINISH)
FINISH_POSITION = (130,250)
RED_CAR = scale_image(pg.image.load("Media/red-car-imported.png"),0.6)
BLUE_CAR = scale_image(pg.image.load("Media/car2.png"),0.6)


WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Weeb Racing")

FPS=60

class AbstractCar:
    def __init__(self,max_vel,rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.img= self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self,left=False,right=False):
        if left:
            self.angle+=self.rotation_vel
        elif right:
            self.angle-=self.rotation_vel
    
    def draw(self,win):
        blit_rotate_center(win,self.img,(self.x,self.y),self.angle)

    def move_forward(self):
        self.vel = min(self.vel+self.acceleration,self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel-self.acceleration,-self.max_vel/2)
        self.move()
 
    def move(self):
        # self.x+=self.vel
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians)*self.vel
        self.y-=vertical
        self.x-=horizontal
    
    def collide(self,mask,x=0,y=0):
        car_mask = pg.mask.from_surface(self.img)
        offset = (abs(int(x-self.x)),abs(int(y-self.y)))
        poi = mask.overlap(car_mask,offset)
        return poi
    
    def reset(self):
        self.x,self.y=self.START_POS
        self.angle=0
        self.vel=0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS=(180,200)

    def reduce_speed(self):
    # if self.vel>0:
        self.vel=max(self.vel-(self.acceleration)*0.8, 0)
        self.move()
    # elif self.vel<0:
    #     self.vel=max(self.vel+(self.acceleration)*0.8, 0)
    #     self.move()
    # else:
    #     pass   

    def bounce(self):
        self.vel=-self.vel/2
        self.move()

player_car = PlayerCar(8,6)



#function to draw on the screen
def draw(win,images,player_car):
    for img,pos in images:
        win.blit(img,pos)

    player_car.draw(win)
    pg.display.update()

images = [(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,FINISH_POSITION),(TRACK_BORDER,(0,0))] #,(RED_CAR,(0,0)) : paste this if it does not work

def move_player(player_car):
    keys = pg.key.get_pressed()
    moving = False

    if keys[pg.K_a] or keys[pg.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pg.K_w] or keys[pg.K_UP]:
        moving=True
        player_car.move_forward()
    if keys[pg.K_s] or keys[pg.K_DOWN]:
        moving=True
        player_car.move_backward()

    if not moving:
        player_car.reduce_speed()


#SET UP THE EVENT LOOP
run = True
clock = pg.time.Clock()

while run:
    clock.tick(FPS)
    draw(WIN,images,player_car)    


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
    
    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK)!=None:
        player_car.bounce()
    
    finish_collision_poi=player_car.collide(FINISH_MASK,*FINISH_POSITION)
    if finish_collision_poi!=None:
        print(finish_collision_poi)
        if finish_collision_poi[1]==17:
            player_car.bounce()
        else:
            player_car.reset()
            print("finish")

pg.quit()