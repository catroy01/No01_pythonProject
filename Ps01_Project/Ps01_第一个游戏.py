import pygame
import random

pygame.init()

# 定义常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
MOVE_INTERVAL = 600 # 蛇每 MOVE_INTERVAL 毫秒移动一次

# 创建游戏窗口
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


# 定义蛇类
class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "stop"
        self.alive = True
        self.last_move_time = pygame.time.get_ticks()

    def move(self):
        if self.direction == "stop":
            return

        # 检查是否应该移动
        now = pygame.time.get_ticks()
        if now - self.last_move_time < MOVE_INTERVAL:
            return
        self.last_move_time = now

        # 移动蛇头
        if self.direction == "up":
            new_head = (self.body[0][0], self.body[0][1] - BLOCK_SIZE)
        elif self.direction == "down":
            new_head = (self.body[0][0], self.body[0][1] + BLOCK_SIZE)
        elif self.direction == "left":
            new_head = (self.body[0][0] - BLOCK_SIZE, self.body[0][1])
        elif self.direction == "right":
            new_head = (self.body[0][0] + BLOCK_SIZE, self.body[0][1])

        # 检查是否撞墙或撞到自己
        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or \
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or \
                new_head in self.body[1:]:
            self.alive = False
            return

        # 检查是否吃到食物
        if new_head == food:
            self.body.insert(0, new_head)
            generate_food()
        else:
            self.body.pop()
            self.body.insert(0, new_head)

    def draw(self):
        for block in self.body:
            pygame.draw.rect(window, (255, 255, 255), (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    def change_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"


# 定义生成食物的函数
def generate_food():
    global food
    x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
    y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
    food = (x, y)


# 创建蛇和食物对象
snake = Snake()
generate_food()

# 游戏循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("down")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("left")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("right")

        # 更新蛇的位置和状态
    snake.move()
    if not snake.alive:
        pygame.quit()
        quit()

    # 绘制游戏场景
    window.fill((0, 0, 0))
    snake.draw()
    pygame.draw.rect(window, (255, 0, 0), (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()

