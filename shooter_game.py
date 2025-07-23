from random import randint
from pygame import *
from time import time as timer
font.init()
font2 = font.SysFont('Comic Sans MS',35)
font1 = font.SysFont('Comic Sans MS',35)
score = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
window = display.set_mode((700,500))
display.set_caption('шутер')
galaxy = transform.scale(image.load('galaxy.jpg'),(700,500))
xp = 3
lost = 0
rew = 0
lose = font1.render('YOU LOST',True, (240,200,4))
win = font1.render('YOU VIN',True, (250,250,4))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15, 20, 15)
        Bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global xp
        global lost
        if self.rect.y > 700:
            self.rect.x = randint (80,420)
            self.rect.y = 0
            lost =  lost + 1
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint (80,420)
            self.rect.y = 0


class Bullet(GameSprite):
    global rew
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

Bullets = sprite.Group()
player = Player('rocket.png',100, 300, 75, 100, 10)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(80,420),-40,80,50,randint(1,5))

    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80,420),-40, 80,50,  randint(1,5))
    monsters.add(monster)


game = True
finish = False
rel_time = False 
num_fire = 0
while game:
    
    for e in event.get():
        
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
            
    if not finish:
        window.blit(galaxy,(0,0))
        asteroids.draw(window)
        monsters.draw(window)
        Bullets.draw(window)
        asteroids.update()
        Bullets.update()
        monsters.update()
        player.reset()
        player.update()
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reloand = font2.render('перезарядка', True,(150,0,0))
                window.blite(reloand,(250, 400))
            else:
                num_fire = 0
                rel_time = False
                
        text_lose = font2.render('Пропущено:' + str(lost), True, (255,255,255))
        window.blit(text_lose,(10,20))
        text_lose2 = font2.render('Повержено:' + str(rew), True, (255,255,255))
        window.blit(text_lose2,(10,50))
        text_lose3 = font2.render('Количество Жизний:' + str(xp), True, (255,255,255))
        window.blit(text_lose3,(10,80))
        if sprite.groupcollide(monsters,Bullets,True,True)  :
            rew += 1
            monster = Enemy('ufo.png',randint(80,420),-40, 80,50,  randint(1,5))
            monsters.add(monster)           
        if rew > 100:
            window.blit(win,(250,250))
            finish = True
        if sprite.spritecollide(player,monsters,False) or lost >   3:
            window.blit(lose, (250,250))
            finish = True
        if sprite.spritecollide(player,asteroids,True) :
            xp -= 1
        if xp == 0:

            window.blit(lose, (250,250))
            finish = True            





    display.update()
    time.delay(30)
    