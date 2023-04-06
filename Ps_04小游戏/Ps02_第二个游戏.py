import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 设置显示
screen_width = 480
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置时钟
clock = pygame.time.Clock()

# 加载图片
background_img = pygame.image.load("assets/background.png").convert()
player_img = pygame.image.load("assets/player.png").convert_alpha()
bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()
enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()
gameover_img = pygame.image.load("assets/gameover.png").convert_alpha()
enemy_explosion_img = pygame.image.load("assets/enemy_explosion.png").convert_alpha()

# 设置字体
font_name = pygame.font.match_font("arial")

# 设置变量
player_speed = 3
bullet_speed = 5
enemy_speed = 3
enemy_spawn_delay = 500
last_enemy_spawn_time = 0
score = 0

# 定义类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = player_speed
        self.shoot_delay = 250
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        # 保持玩家在屏幕上
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = bullet_speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

        # 检查子弹与敌人的碰撞
        hits = pygame.sprite.spritecollide(self, enemies, True)
        for hit in hits:
            global score
            score += 10
            enemy_explosion = EnemyExplosion(hit.rect.center)
            all_sprites.add(enemy_explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randint(3, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = enemy_explosion_img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.animation_time = 50
        self.current_time = 0

    def update(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.kill()

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 生成敌人
    now = pygame.time.get_ticks()
    if now - last_enemy_spawn_time >= enemy_spawn_delay:
        last_enemy_spawn_time = now
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 更新精灵
    all_sprites.update()

    # 检查玩家与敌人的碰撞
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        screen.blit(gameover_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(1000)
        break

    # 绘制所有内容
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, screen_width // 2, 10)
    pygame.display.flip()

    # 设置帧率
    clock.tick(60)

    # 重新开始游戏
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        all_sprites.empty()
        enemies.empty()
        bullets.empty()
        player = Player()
        all_sprites.add(player)
        last_enemy_spawn_time = 0
        score = 0

# 退出pygame
pygame.quit()
sys.exit()
