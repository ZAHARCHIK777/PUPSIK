from typing import Any
from pygame import *
from pygame import display
from pygame import sprite
window = display.set_mode((400, 500))
display.set_caption("CS:GO 3")

mixer.init()
mixer.music.load('Bam.mp3')
mixer.music.play()
mixer.music.set_volume(0.2)

class GameSprite(sprite.Sprite):
    def __init__(self,pl_image, pl_x, pl_y, size_x, size_y, pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image),(size_x, size_y))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 320:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 320:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 400:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-10, self.rect.top, 30, 80, -15)
        bullets.add(bullet)
from random import *
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(5, 320)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("asteroid.png", randint(0, 320), -40, 80,80,randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
background = transform.scale(image.load("burning_city.jpg"),(1280, 720))
ship = Player("rocket.png", 100, 400, 80, 100, 5)
k1_bullet = Bullet("bullet.png",280, 20, 30, 80, 0)
k2_bullet = Bullet("bullet.png",300, 20, 30, 80, 0) 
k3_bullet = Bullet("bullet.png",320, 20, 30, 80, 0) 
k4_bullet = Bullet("bullet.png",340, 20, 30, 80, 0) 
k5_bullet = Bullet("bullet.png",360, 20, 30, 80, 0) 
import sys

font.init()
mainfont = font.Font("Montserrat.ttf", 23)
win = mainfont.render("ВИ ПЕРЕСТРІЛЯЛИ РАШИСТАВ!",  True, (255,255,255))
lose = mainfont.render("ВАС ПЕРЕСТРІЛЯЛИ РАШИСТИ(!",  True, (255,0,0))
score = 0
lost = 0
fire_sound = mixer.Sound('fire.mp3')
dron_sound = mixer.Sound('porosyachiy-vizg.mp3')
max_lost = 2

rel_time = False
num_fire = 0
from time import time as timer
while True:
    k_fire=5-num_fire
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                    fire_sound.set_volume(0.2)
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish: #
        window.blit(background, (0,0))
        text_rakh = mainfont.render("Сбито дронов: "+ str(score), True, (255,255,255))
        text_skip = mainfont.render("Пробитие: "+ str(lost), True, (255,255,255))
        text_patron = mainfont.render("Ядерок: "+ str(k_fire), True, (255,255,255))
        window.blit(text_rakh, (10,10))
        window.blit(text_skip, (10,50))
        window.blit(text_patron, (270,10))
        ship.update()
        monsters.update()
        bullets.update()
        ship.draw()
        bullets.draw(window)
        monsters.draw(window)
        if k_fire>=0:
            if k_fire==1:
               k1_bullet.draw()
            if k_fire==2:
               k1_bullet.draw()
               k2_bullet.draw()
            if k_fire==3:
               k1_bullet.draw()
               k2_bullet.draw()
               k3_bullet.draw()
            if k_fire==4:
               k1_bullet.draw()
               k2_bullet.draw()
               k3_bullet.draw()
               k4_bullet.draw()
            if k_fire==5:
               k1_bullet.draw()
               k2_bullet.draw()
               k3_bullet.draw()
               k4_bullet.draw()
               k5_bullet.draw()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2.1:
                reload = mainfont.render("Зачекайте, Перезарядка..."+ str((now_time-last_time)//1) + "/2", True, (255, 255, 255))
                window.blit(reload, (20,350))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets,  True, True)
        for c in collides:
            score +=1
            monster = Enemy("asteroid.png", randint(0, 320), -40, 50,50, randint(1,3))
            dron_sound.play()
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost > max_lost:
            window.blit(background, (0,0))
            finish = True
            ship.draw()
            window.blit(lose,(10, 200))
        if score >= 25:
            window.blit(background, (0,0))
            finish = True
            ship.draw()
            window.blit(win,(10, 200))
    display.update()
    time.delay(25)