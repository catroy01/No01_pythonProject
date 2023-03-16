import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 定义屏幕尺寸
screen_width = 480
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# 加载背景图像
background_image = pygame.image.load("background.png").convert()

# 加载游戏结束图像
game_over_image = pygame.image.load("gameover.png").convert_alpha()
game_over_rect = game_over_image.get_rect(center=(screen_width//2, screen_height//2))

# 定义玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")  # 加载玩家飞机图像
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # 更新玩家飞机位置
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 确保玩家飞机不会飞出屏幕外
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def shoot(self):
        # 创建一颗新的子弹对象
        new_bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(new_bullet)
        bullets.add(new_bullet)

# 定义子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png")  # 加载子弹图像
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10  # 子弹的垂直速度

    def update(self):
        # 更新子弹位置
        self.rect.y += self.speed_y

        # 如果子弹飞出屏幕外，就销毁它
        if self.rect.bottom < 0:
            self.kill()

# 定义敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")  # 加载敌机图像
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen_width)
        self.rect.bottom = 0
        self.speed_y = random.randint(5, 10)  # 敌机的垂直速度

    def update(self):
        # 更新敌机位置
        self.rect.y += self.speed_y

        # 如果敌机飞出屏幕外，就销毁它
        if self.rect.top > screen_height:
            self.kill()

# 创建游戏精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

clock = pygame.time.Clock()

while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

# 创建新的敌机
if random.randint(0, 100) < 3:
    new_enemy = Enemy()
    all_sprites.add(new_enemy)
    enemies.add(new_enemy)

# 检测玩家飞机与敌机的碰撞
if pygame.sprite.spritecollide(player, enemies, False):
    all_sprites.remove(player)
    screen.blit(game_over_image, game_over_rect)
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# 检测子弹与敌机的碰撞
hits = pygame.sprite.groupcollide(enemies, bullets, True, True)

# 更新游戏精灵组中所有对象的状态
all_sprites.update()

# 绘制背景和所有的游戏对象
screen.blit(background_image, (0, 0))
all_sprites.draw(screen)

# 更新屏幕
pygame.display.flip()

# 控制游戏帧率
clock.tick(60)

