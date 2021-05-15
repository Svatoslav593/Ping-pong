# hello 

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

class Player(GameSprite):
    def update_r(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y >10:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 480:
            self.rect.y += self.speed
    def update_l(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y >10:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 480:
            self.rect.y += self.speed

background = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(background)

game = True
finish = False

clock = time.Clock()
FPS = 60

racket1 = Player("gold_border.png", 30, 200, 20, 50, 10)
racket2 = Player("gold_border.png", 520, 200, 20, 50, 10)
ball = GameSprite("ball.png", 200, 200, 50, 50, 50)

speedx = 3
speedy = 3

font.init()
font1 = font.Font(None, 35)
lose1 = font1.render("PLAYER 1 LOSE!", True, (180, 0, 0))
lose2 = font1.render("PLAYER 2 LOSE!", True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill(background)
        racket1.update_l()
        racket2.update_r()
        racket1.reset()
        racket2.reset()
        ball.reset()
        ball.rect.x += speedx
        ball.rect.y += speedy

        if ball.rect.y >= 400 or ball.rect.y <= 0:
            speedy *= -1

        if sprite.collide_rect(ball,racket1) or sprite.collide_rect(ball,racket2):
            speedx *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))

        if ball.rect.x > 600:
            finish = True
            window.blit(lose2, (200, 200))
    display.update()
    clock.tick(FPS)
