import os.path
import random

import pygame
from PIL.FontFile import WIDTH
from pygame.examples.moveit import HEIGHT
from pygments.styles.rainbow_dash import WHITE
from sympy.printing.pretty.pretty_symbology import center

FPS = 60
RED = (255,0,0)
#游戏的初始化
pygame.init()
screen = pygame.display.set_mode((500,600))
pygame.display.set_caption("游戏")
clock = pygame.time.Clock()

#载入图片
beiying_img =pygame.image.load("bank.png").convert()
player_img =pygame.image.load("player.png").convert()
rock_img =pygame.image.load("rock.png").convert()
bullet_img =pygame.image.load("bullet.png.").convert()

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,(0,255,0),fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_init():
    draw_text(screen,'     space survival!',64,WIDTH/4,HEIGHT/4)
    draw_text(screen, '          < >moving Space and fire blanks', 30, WIDTH/4, HEIGHT / 2)
    draw_text(screen, '  Ang key to Start', 18, WIDTH / 4, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(15,34))
        #self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.radius = 25
        self.health =100
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 600 - 10
        self.speedx = 8

    def update(self, *args, **kwargs):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx


        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullets.add(bullet)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(rock_img,(30,30))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        self.rect.x = random.randrange(0,500 - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)

    def update(self, *args, **kwargs):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 600 or self.rect.left > 500 or self.rect.right < 0:
            self.rect.x = random.randrange(0, 500 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(15,25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self, *args, **kwargs):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

score = 0


show_init = True
running = True

while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    #取得输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #更新游戏
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        r = Rock ()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        running = False


    #画面演示
    #画面颜色，黑色
    screen.fill((0,0,0))
    screen.blit(beiying_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,10)
    pygame.display.update()
pygame.quit()


