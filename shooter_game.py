from pygame import *
init()
from random import *
count = 0
window = display.set_mode((700, 500))
display.set_caption('Шутер')
clock = time.Clock()
game = True
finish = False
boss = False
loss = False
won = False 
babaha = 0
hp = 15
bullets = sprite.Group()
go = True
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(img),(self.w,self.h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def rendering(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def move(self):
        key_p = key.get_pressed()
        if key_p[K_a] and self.rect.x >0:
            self.rect.x -= 9
            
        if key_p[K_d] and self.rect.x < 630:
            self.rect.x += 9
    def update(self):
        global babaha
        global finish
        global loss
        self.rect.y +=2
        if self.rect.y >= 450:
            self.rect.y = randint(0,100)
            self.rect.x = randint(65,690)
            babaha += 1
        if babaha >= 3:
            finish = True
            loss = True
def restart():
    global finish, babaha
    key_p = key.get_pressed()
    if key_p[K_r] and finish == True:
        finish = False
        loss = False
        won = False
        babaha = 0
        count = 0
        print('Restart')
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class Ufo(GameSprite):
    def update(self):
        global babaha
        global finish
        global loss
        self.rect.y += self.speed
        self.rect.y +=1
        if self.rect.y >= 500:
            self.rect.y = randint(0,100)
            self.rect.x = randint(65,690)
            babaha += 1
        if babaha >= 3:
            finish = True
            loss = True
class Asteroid(GameSprite):
    def update(self):
        global babaha
        global finish
        global loss
        self.rect.y += self.speed
        self.rect.y +=2
        if self.rect.y >= 500:
            self.rect.y = randint(0,100)
            self.rect.x = randint(65,690)
            babaha += 1
        if babaha >= 3:
            finish = True
            loss = True
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()

font = font.SysFont(' Courier, monospaced', 70)
false1 = font.render('YOU ARE NOOB!', True, (255, 215, 0))
false2 = font.render('PRESS R TO RESSTART', True, (255, 215, 0))
won1 = font.render('YOU ARE WINNER!', True, (255, 215, 0))
won2 = font.render('PRESS R TO RESSTART!', True, (255, 215, 0))
rocket = GameSprite('rocket.png', 350, 420, 65, 65, 20)
ufo1 = GameSprite('ufo.png', 350, 100, 50, 25, 2)
ufo2 = GameSprite('ufo.png', 452, 70, 50, 25, 2)
ufo3 = GameSprite('ufo.png', 122, 10, 50, 25, 2)
ufo4 = GameSprite('ufo.png', 221, 50, 50, 25, 2)
ufo5 = GameSprite('ufo.png', 301, 30, 50, 25, 2)
asteroid1 = GameSprite('asteroid.png', 200, 20, 50, 50, 2)
asteroid2 = GameSprite('asteroid.png', 100, 50, 50, 50, 2)
asteroid3 = GameSprite('asteroid.png', 150, 32, 50, 50, 2)
bullets = sprite.Group()
bossik = GameSprite('bossik.png', 300, 70, 100, 100, 1)
bossiks = sprite.Group()
bossiks.add(bossik)
ufos = sprite.Group()
ufos.add(ufo1)
ufos.add(ufo2)
ufos.add(ufo3)
ufos.add(ufo4)
ufos.add(ufo5)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
while game:
    if count >= 25:
        boss = True
    counter = font.render(str(count), True, (255, 215, 0))
    key_p = key.get_pressed()
    restart()
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullets.add(Bullet('bullet.png', rocket.rect.centerx-7, rocket.rect.top, 30, 15, 30))
    rocket.rendering()
    window.blit(counter, (50, 50))
    if finish == False:
        rocket.move()
        if boss == False:
            ufos.update()
        if boss == True:
            bossiks.update()
        if boss == False:
            asteroids.update()
    if boss == False:
        if len(ufos) < 5:
            ufos.add(Ufo('ufo.png', randint(10, 630), 0, 50, 25, 1)) 
        if len(asteroids) < 3:
            asteroids.add(Asteroid('asteroid.png', randint(10, 630), 0, 50, 50, 2))     
    bullets.draw(window)
    bullets.update()
    rocket.rendering()
    if boss == False:
        ufos.draw(window)
    if boss == True:
        bossiks.draw(window)
    if boss == False:
        asteroids.draw(window)
    if sprite.groupcollide(bullets, ufos, True, True):
        count += 1
    sprite.spritecollide(rocket, ufos, True)
    sprite.groupcollide(bullets, asteroids, True, True)
    sprite.spritecollide(rocket, asteroids, True)
    if boss == True:
        if go == True:
            if sprite.groupcollide(bullets, bossiks, True, False):
                hp -= 1
                print('hp:', hp)
        if hp <= 1:
            go = False
            if sprite.groupcollide(bullets, bossiks, True, True):
                print('hp: 0')
                finish = True
                won = True
        sprite.spritecollide(rocket, bossiks, False)

    if finish == True:
        if loss == True:
            window.blit(false1, (120, 200))
            window.blit(false2, (0, 250))
        if won == True:
            window.blit(won1, (120, 200))
            window.blit(won2, (0, 250))
    clock.tick(60)
    display.update()