# 导入随机数模块
import random

# 导入pygame模块
import pygame

# 初始化pygame模块
pygame.init()

# 定义颜色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 定义窗口大小
dis_width = 600
dis_height = 400

# 创建窗口
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by @cursor_tutor')

# 创建时钟对象
clock = pygame.time.Clock()

# 定义蛇的大小和速度
snake_block = 10
snake_speed = 5

# 定义字体样式
font_style = pygame.font.SysFont(None, 30)


# 定义画蛇的函数
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


# 定义显示消息的函数
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# 定义游戏循环函数
def gameLoop():
    game_over = False
    game_close = False

    # 定义蛇的初始位置和移动方向
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    # 定义蛇的列表和长度
    snake_List = []
    Length_of_snake = 1

    # 定义食物的位置
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        # 如果游戏结束，显示游戏结束消息
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            # 检测用户按键
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 检测用户按键
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 如果蛇的头部超出窗口边界，游戏结束
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # 画出食物
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # 更新蛇的列表
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 如果蛇头和食物重合，更新食物位置并增加蛇的长度
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        # 如果蛇头和食物重合，更新食物位置并增加蛇的长度
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # 画出蛇
        our_snake(snake_block, snake_List)

        # 显示蛇的长度
        pygame.display.update()
        font_style = pygame.font.SysFont(None, 25)
        value = font_style.render("Your Score: " + str(Length_of_snake - 1), True, yellow)
        dis.blit(value, [0, 0])

        # 更新窗口
        pygame.display.update()

        # 控制蛇的速度
        clock.tick(snake_speed)

    # 退出pygame模块
    pygame.quit()

    # 退出python程序
    quit()


# 开始游戏
gameLoop()
