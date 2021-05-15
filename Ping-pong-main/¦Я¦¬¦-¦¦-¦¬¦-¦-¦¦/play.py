from time import time as timer
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y,size_x,size_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x,size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#speed = 10
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >10:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        #kick = mixer.Sound("fire.ogg")
        #kick.play()
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y = 0
            lost += 1

finish = False
hero = Player('rocket3.png',25,420,65,65,10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range (5):
    monster = Enemy("ufo.png",randint(0,620),0,65,65,randint(1,5))
    monsters.add(monster)

window = display.set_mode((700, 500))
display.set_caption("Шутер")
bag = transform.scale(image.load("galaxy.jpg"), (700, 500))
clock = time.Clock()
FPS = 60
font.init()
font1 = font.SysFont('Arial', 36)
skore = 0

#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()

life = 3
rec_time = False
num_fire = 0
skore = 0
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rec_time == False:
                    num_fire = num_fire + 1
                    hero.fire()
                elif num_fire >= 9 and rec_time == False:
                    last_time = timer()
                    rec_time = True
    if finish != True:
        window.blit(bag,(0, 0))
        hero.update()
        hero.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        if rec_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                text_reload = font1.render("Перезарядка", 1, (255,0,0))
                window.blit(text_reload,(260, 450))
            else:
                rec_time = False
                num_fire = 0
        collides = sprite.groupcollide(bullets,monsters,True,True)
        for coll in collides:
            monster = Enemy("ufo.png",randint(0,620),0,65,65,randint(1,5))
            monsters.add(monster)
            skore += 1
        if sprite.spritecollide(hero,monsters,True):
            life = life - 1
            monster = Enemy("ufo.png",randint(0,620),0,65,65,randint(1,5))
            monsters.add(monster)
        if life == 0 or lost >= 5:
            finish = True
            text_lose = font1.render("YOU LOSE!",1,(255,255,255))
            window.blit(text_lose, (270, 250))
        if skore >= 10:
            finish = True
            text_lose = font1.render("YOU WIN!",1,(255,255,255))
            window.blit(text_lose, (270, 250))
        text_win = font1.render('Счет' + ":" + str(skore),1,(255,255,255))
        text_lose = font1.render('Пропущено' + ":" + str(lost),1,(255,255,255))
        window.blit(text_lose, (10,10))
        window.blit(text_win, (10,40))
        text_lose = font1.render(str(life),1,(255,255,255))
        window.blit(text_lose, (670, 10))
        clock.tick(FPS)
        display.update()
    else:
        finish = False
        skore = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for i in range (5):
            monster = Enemy("ufo.png",randint(0,620),0,65,65,randint(1,5))
            monsters.add(monster)