import pygame, sys, time, random, os
from pygame.locals import *

# 初始化
pygame.init()
main_clock = pygame.time.Clock()

# 设置窗口
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption('Sprites and Sounds')

# 颜色
WHITE = (255,255,255)

# 设置角色数据
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
player = pygame.Rect(300,100,40,40)
player_image = pygame.image.load(os.path.join(BASE_DIR,'player.png'))
player_stretched_image = pygame.transform.scale(player_image,(40,40))
food_image = pygame.image.load(os.path.join(BASE_DIR,'cherry.png'))
foods = [pygame.Rect(random.randrange(0,WINDOW_WIDTH-20+1),random.randrange(0,WINDOW_HEIGHT-20+1),20,20) for _ in range(20)]

food_counter = 0
NEW_FOOD = 40

# 设置运动相关的变量
move_left = False
move_right = False
move_up = False
move_down = False

MOVE_SPEED = 6

# 设置音乐
pick_up_sound = pygame.mixer.Sound(os.path.join(BASE_DIR,'pickup.wav'))
pygame.mixer.music.load(os.path.join(BASE_DIR,'background.mid'))
# 第一个参数设置为-1表示无限循环背景音乐
# 第二个参数的意思是从音乐的开头开始播放，它的单位是秒
pygame.mixer.music.play(-1,0.0)
music_playinig = True

# 游戏循环
while True:
    for event in pygame.event.get():
        # 检测退出
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
        if event.type ==KEYUP:
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
                player.left = random.randrange(0,WINDOW_WIDTH-player.width+1)
                player.top = random.randrange(0,WINDOW_HEIGHT-player.height+1)
            if event.key == K_m:
                if music_playinig:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1,0.0)
                music_playinig = not music_playinig
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0]-10,event.pos[1]-10,20,20))

    food_counter += 1
    if food_counter >= NEW_FOOD:
        food_counter = 0
        foods.append(pygame.Rect(random.randrange(0,WINDOW_WIDTH-20+1),random.randrange(0,WINDOW_HEIGHT-20+1),20,20))

    # 绘制白色背景
    window_surface.fill(WHITE)

    # 移动玩家
    if move_down and player.bottom < WINDOW_HEIGHT:
        player.top += MOVE_SPEED
    if move_up and player.top > 0:
        player.top -= MOVE_SPEED
    if move_left and player.left > 0:
        player.left -= MOVE_SPEED
    if move_right and player.right < WINDOW_WIDTH:
        player.left += MOVE_SPEED

    # 绘制玩家
    window_surface.blit(player_stretched_image,player)

    # 检测碰撞并吃掉樱桃
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left,player.top,player.width+2,player.height+2)
            player_stretched_image = pygame.transform.scale(player_image,(player.width,player.height))
            if music_playinig:
                pick_up_sound.play()

    # 绘制樱桃
    for food in foods:
        window_surface.blit(food_image,food)

    # 刷新屏幕
    pygame.display.update()
    main_clock.tick(40)    
