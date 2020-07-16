import pygame, sys, time
from pygame.locals import *

# 初始化pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption('Animation')

# 设置一些方向常量
DOWN_LEFT = 'downleft'
DOWN_RIGHT = 'downright'
UP_LEFT = 'upleft'
UP_RIGHT = 'upright'

# 速度
MOVE_SPEED = 4

# 颜色
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# 设置几个盒子
b1 = {'rect':pygame.Rect(300,80,50,100),'color':RED,'dir':UP_RIGHT}
b2 = {'rect':pygame.Rect(200,200,20,20),'color':GREEN,'dir':UP_LEFT}
b3 = {'rect':pygame.Rect(100,150,60,60),'color':BLUE,'dir':DOWN_LEFT}
boxes = [b1,b2,b3]

# 启动游戏循环
while True:
    # 检查退出事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # 绘制窗口白色背景,它起到了清屏的作用，否则我们将会看到盒子的轨迹
    window_surface.fill(WHITE)

    for b in boxes:
        # 每个盒子都要按照自己既定的方向运动
        if b['dir'] == DOWN_LEFT:
            b['rect'].left -= MOVE_SPEED
            b['rect'].top += MOVE_SPEED
        if b['dir'] == DOWN_RIGHT:
            b['rect'].left += MOVE_SPEED
            b['rect'].top += MOVE_SPEED
        if b['dir'] == UP_LEFT:
            b['rect'].left -= MOVE_SPEED
            b['rect'].top -= MOVE_SPEED
        if b['dir'] == UP_RIGHT:
            b['rect'].left += MOVE_SPEED
            b['rect'].top -= MOVE_SPEED

        # 检测是否运动到了边缘，到了边缘就换方向
        if b['rect'].top < 0:
            if b['dir'] == UP_LEFT:
                b['dir'] = DOWN_LEFT
            if b['dir'] == UP_RIGHT:
                b['dir'] = DOWN_RIGHT

        if b['rect'].bottom > WINDOW_HEIGHT:
            if b['dir'] == DOWN_LEFT:
                b['dir'] = UP_LEFT
            if b['dir'] == DOWN_RIGHT:
                b['dir'] = UP_RIGHT

        if b['rect'].left < 0:
            if b['dir'] == UP_LEFT:
                b['dir'] = UP_RIGHT
            if b['dir'] == DOWN_LEFT:
                b['dir'] = DOWN_RIGHT

        if b['rect'].right > WINDOW_WIDTH:
            if b['dir'] == UP_RIGHT:
                b['dir'] = UP_LEFT
            if b['dir'] == DOWN_RIGHT:
                b['dir'] = DOWN_LEFT
        # 第三个参数可以是元组，也可以是矩形对象
        pygame.draw.rect(window_surface,b['color'],b['rect'])
    
    pygame.display.update()
    time.sleep(0.02)
