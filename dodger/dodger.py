import pygame, sys, random, os
from pygame.locals import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 设置窗口
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (0,0,0)
BACKGROUND_COLOR = (255,255,255)
FPS = 60
BADDIE_MINSIZE = 10
BADDIE_MAXSIZE = 40
BADDIE_MINSPEED = 1
BADDIE_MAXSPEED = 8
ADD_NEW_BADDIE_RATE = 6
PLAYER_MOVE_RATE = 5

def terminate():
    '''退出游戏'''
    pygame.quit()
    sys.exit()

def wait_for_player_to_press_key() -> None:
    '''处理玩家的按键事件'''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def player_has_hit_baddie(player_rect,baddies) -> bool:
    '''检测是否撞到了坏人'''
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False

def draw_text(text,font,surface,x,y):
    '''把文字绘制到指定平面的指定位置'''
    text_obj = font.render(text,True,TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x,y)
    surface.blit(text_obj,text_rect)

def play_game():
    '''一次游戏的主体'''
    global top_score
    # 设置这次游戏的一些初始状态
    baddies = []
    score = 0
    player_rect.topleft = (WINDOW_WIDTH//2,WINDOW_HEIGHT-50)
    move_left = move_right = move_up = move_down = False
    reverse_cheat = slow_cheat = False
    baddie_add_counter = 0

    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                # 按住z键，坏蛋反着走
                if event.key == K_z:
                    reverse_cheat = True
                # 按住z键，坏蛋减速
                if event.key == K_x:
                    slow_cheat = True
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
                if event.key == K_z:
                    reverse_cheat = False
                    score = 0
                if event.key == K_x:
                    slow_cheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                
                if event.key == K_LEFT or event.key == K_a:
                    move_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False
                if event.key == K_UP or event.key == K_w:
                    move_up = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down = False

            if event.type == MOUSEMOTION:
                # 玩家跟随鼠标移动
                player_rect.centerx = event.pos[0]
                player_rect.centery = event.pos[1]
        
        # 在必要的时候增加坏蛋
        if not reverse_cheat and not slow_cheat:
            baddie_add_counter += 1
        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter = 0
            baddie_size = random.randrange(BADDIE_MINSIZE,BADDIE_MAXSIZE+1)
            new_baddie = {
                'rect':pygame.Rect(random.randrange(WINDOW_WIDTH-baddie_size+1),0-baddie_size,baddie_size,baddie_size),
                'speed':random.randrange(BADDIE_MINSPEED,BADDIE_MAXSPEED+1),
                'surface':pygame.transform.scale(baddie_image,(baddie_size,baddie_size)),
            }
            baddies.append(new_baddie)
        
        # 移动玩家
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1*PLAYER_MOVE_RATE,0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE,0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0,-1*PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0,PLAYER_MOVE_RATE)

        # 移动坏蛋
        for b in baddies:
            if not reverse_cheat and not slow_cheat:
                b['rect'].move_ip(0,b['speed'])
            elif reverse_cheat:
                b['rect'].move_ip(0,-5)
            elif slow_cheat:
                b['rect'].move_ip(0,1)

        # 删除落到底的坏蛋
        for b in baddies[:]:
            if b['rect'].top > WINDOW_HEIGHT:
                baddies.remove(b)
        
        # 绘制背景
        window_surface.fill(BACKGROUND_COLOR)

        # 绘制分数
        draw_text(f'Score: {score}',font,window_surface,10,0)
        draw_text(f'Top Score: {top_score}',font,window_surface,10,40)

        # 绘制玩家
        window_surface.blit(player_image,player_rect)

        # 绘制坏蛋
        for b in baddies:
            window_surface.blit(b['surface'],b['rect'])
        
        # 刷新屏幕
        pygame.display.update()
        
        # 检测碰撞
        if player_has_hit_baddie(player_rect,baddies):
            if score > top_score:
                top_score = score
            break

        main_clock.tick(FPS)




# 初始化,设置窗口和鼠标
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# 设置字体
font = pygame.font.SysFont(None,48)

# 设置声音
game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR,'gameover.wav'))
pygame.mixer.music.load(os.path.join(BASE_DIR,'background.mid'))

# 设置图片
player_image = pygame.image.load(os.path.join(BASE_DIR,'player.png'))
player_rect = player_image.get_rect()
baddie_image = pygame.image.load(os.path.join(BASE_DIR,'baddie.png'))

# 开始画面
window_surface.fill(BACKGROUND_COLOR)
draw_text('Dodger',font,window_surface,WINDOW_WIDTH//3,WINDOW_HEIGHT//3)
draw_text('Press a key to start',font,window_surface,WINDOW_WIDTH//3-30,WINDOW_HEIGHT//3+50)
pygame.display.update()
wait_for_player_to_press_key()

top_score = 0
while True:
    pygame.mixer.music.play(-1,0.0)
    play_game()
    pygame.mixer.music.stop()
    game_over_sound.play()
    draw_text('GAME OVER',font,window_surface,WINDOW_WIDTH//3,WINDOW_HEIGHT//3)
    draw_text('Press a key to play again.',font,window_surface,WINDOW_WIDTH//3-80,WINDOW_HEIGHT//3+50)
    pygame.display.update()
    wait_for_player_to_press_key()
    game_over_sound.stop()




