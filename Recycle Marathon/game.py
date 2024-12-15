import pygame
import random
from pygame.locals import *
import time
pygame.init()


#create the gaming screen
#assign screen's width, height and caption
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Recycle Marathon")

def bg_change(image):
    #load the image in a variable
    bg = pygame.image.load(image)
    #resize it to screen size
    bg_size = pygame.transform.scale(bg, (screen_width, screen_height))
    #put it on the screen background
    screen.blit(bg_size,(0,0))

class Bin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,60))
        self.rect = self.image.get_rect()

class Recyclable(pygame.sprite.Sprite):
    def __init__(self,img):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()

class Non_Recyclable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('plastic.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()


images = ["item1.png","item2.png","item3.png"]

rec_list = pygame.sprite.Group()
plastic_list = pygame.sprite.Group()
allitems_list = pygame.sprite.Group()

for i in range(50):
    rec = Recyclable(random.choice(images))
    rec.rect.x = random.randrange(screen_width)
    rec.rect.y = random.randrange(screen_height)
    rec_list.add(rec)
    allitems_list.add(rec)

for i in range(25):
    plastic = Non_Recyclable()
    plastic.rect.x = random.randrange(screen_width)
    plastic.rect.y =random.randrange(screen_height)
    plastic_list.add(plastic)
    allitems_list.add(plastic)

bin = Bin()
allitems_list.add(bin)

WHITE = (255,255,255)
RED = (255,0,0)
playing = True
score = 0
clock = pygame.time.Clock()
start_time = time.time()
font = pygame.font.SysFont("Times New Roman", 25)
time_font = pygame.font.SysFont("Arial", 20)

text = font.render("Score: "+ str(score),True, RED)

while playing:
    clock.tick(30)
    time_Elapsed = time.time() - start_time
    if time_Elapsed >= 60:
        if score >= 40:
            bg_change("win_bg.png")
        else:
            bg_change("lose_bg.png")
            
        pygame.display.update()
        time.sleep(3)
        break

    else:
        bg_change("bg.png")
        countdown = time_font.render("Time left: " + str(60 - int(time_Elapsed)),True,RED)
        screen.blit(countdown,(20,10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if bin.rect.y > 0:
                bin.rect.y -= 5
        if keys[pygame.K_DOWN]:
            if bin.rect.y < 640:
                bin.rect.y += 5
        if keys[pygame.K_RIGHT]:
            if bin.rect.x < 860:
                bin.rect.x += 5
        if keys[pygame.K_LEFT]:
            if bin.rect.x > 0:
                bin.rect.x -= 5

        RecyclableHitList = pygame.sprite.spritecollide(bin,rec_list,True)
        PlasticHitList = pygame.sprite.spritecollide(bin,plastic_list,True)

        for item in RecyclableHitList:
            score += 1
            text = font.render("Score: "+ str(score),True, RED)
        for item in PlasticHitList:
            score -= 3
            text = font.render("Score: "+ str(score),True, RED)

        screen.blit(text, (800,10))
        allitems_list.draw(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
