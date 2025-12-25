import os
import random
import pygame

# ================== 常量设置 ==================
FPS = 60
WIDTH = 500
HEIGHT = 600
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ================== 初始化 ==================
pygame.init()
pygame.mixer.init()  # 如果后续加音效可启用
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Survival")
clock = pygame.time.Clock()

# ================== 载入图片 ==================
# 检查图片是否存在，若不存在则用纯色 Surface 替代（避免崩溃）
def load_image(name, default_size=None):
    if os.path.isfile(name):
        img = pygame.image.load(name).convert()
        if default_size:
            img = pygame.transform.scale(img, default_size)
        return img
    else:
        print(f"警告：找不到图片 '{name}'，使用默认色块代替。")
        surf = pygame.Surface(default_size or (30, 30))
        surf.fill(RED)
        return surf

beiying_img = load_image("bank.png", (WIDTH, HEIGHT))      # 背景图
player_img = load_image("player.png", (15, 34))           # 玩家飞船
rock_img = load_image("rock.png", (30, 30))               # 陨石
bullet_img = load_image("bullet.png", (15, 25))           # 子弹

# 字体
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_init():
    screen.fill(BLACK)
    draw_text(screen, 'Space Survival!', 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, '< >moving Space and fire blanks', 24, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, 'Ang key to Start', 18, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                waiting = False

# ================== 游戏精灵类 ==================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)  # 假设黑色为透明色
        self.rect = self.image.get_rect()
        self.radius = 12
        self.health = 100
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        # 边界限制
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = rock_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # 若移出屏幕，重置位置
        if (self.rect.top > HEIGHT) or (self.rect.left > WIDTH) or (self.rect.right < 0):
            self.reset_position()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# ================== 主游戏循环 ==================
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# 初始状态
show_init = True
running = True

while running:
    if show_init:
        draw_init()
        # 初始化精灵组
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for _ in range(8):
            new_rock()
        score = 0
        show_init = False

    clock.tick(FPS)

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新游戏状态
    all_sprites.update()

    # 子弹击中陨石
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += 10
        new_rock()  # 生成新陨石

    # 玩家被陨石撞击
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        new_rock()
        if player.health <= 0:
            show_init = True  # 游戏结束，回到开始界面

    # 绘制画面
    screen.blit(beiying_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH // 2, 10)
    draw_health(screen, player.health, 5, 10)

    pygame.display.update()

pygame.quit()