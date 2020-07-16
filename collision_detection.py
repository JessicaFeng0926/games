import pygame, sys, random
from pygame.locals import *

# 初始化pygame
pygame.init()
main_clock = pygame.time.Clock()

# 设置窗口
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption('Collision Detection')

# 颜色
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

# 设置玩家和食物
food_counter = 0
NEW_FOOD = 40
FOOD_SIZE = 20
player = pygame.Rect(300,100,50,50)
foods = [pygame.Rect(random.randrange(0,WINDOW_WIDTH-FOOD_SIZE+1),random.randrange(0,WINDOW_HEIGHT-FOOD_SIZE+1),FOOD_SIZE,FOOD_SIZE) for _ in range(20)]

# 设置一些表示运动的变量
move_left = False
move_right = False
move_up = False
move_down = False

MOVE_SPEED = 6

while True:
    # 检测事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # 修改运动变量
            if event.key == K_LEFT or event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == K_d:
                move_left = False
                move_right = True
            if event.key == K_UP or event.key == K_w:
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == K_s:
                move_up = False
                move_down = True
        
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_x:
                # 让玩家随机出现
                player.left = random.randrange(0,WINDOW_WIDTH-player.width+1)
                player.top = random.randrange(0,WINDOW_HEIGHT-player.height+1)
        if event.type == MOUSEBUTTONDOWN:
            foods.append(pygame.Rect(event.pos[0],event.pos[1],FOOD_SIZE,FOOD_SIZE))
    
    # 循环四十次，添加一个食物，也就是每秒添加一个食物
    food_counter += 1
    if food_counter >= NEW_FOOD:
        food_counter = 0
        foods.append(pygame.Rect(random.randrange(0,WINDOW_WIDTH-FOOD_SIZE+1),random.randrange(0,WINDOW_HEIGHT-FOOD_SIZE+1),FOOD_SIZE,FOOD_SIZE))

    # 绘制白色背景
    window_surface.fill(WHITE)

    # 移动玩家
    if move_down and player.bottom<WINDOW_HEIGHT:
        player.top += MOVE_SPEED
    if move_up and player.top > 0:
        player.top -= MOVE_SPEED
    if move_left and player.left > 0:
        player.left -= MOVE_SPEED
    if move_right and player.right<WINDOW_WIDTH:
        player.left += MOVE_SPEED

    # 绘制玩家
    pygame.draw.rect(window_surface,BLACK,player)

    # 检测碰撞，碰到的食物就会被吃掉消失
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)

    # 绘制剩下的食物
    for food in foods:
        pygame.draw.rect(window_surface,GREEN,food)

    
    # 刷新窗口
    pygame.display.update()
    # 它可以根据电脑的运行速度自动调整时间
    # 保证在不同的电脑上都是一秒循环40次
    main_clock.tick(40)

