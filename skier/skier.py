import sys
import random
import pygame
import pygame.locals as pl

skier_images = [
    'skier_down.png',
    'skier_right1.png',
    'skier_right2.png',
    'skier_left1.png',
    'skier_left2.png',
]

class SkierClass(pygame.sprite.Sprite):
    '''滑雪者，继承自精灵类'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('skier_down.png')
        self.rect = self.image.get_rect()
        self.rect.center = [320,100]
        # 这个角度控制了滑雪者的方向，它本质上是索引
        # 范围是-2到2
        self.angle = 0

    def turn(self,direction):
        '''滑雪者转向，返回转向后滑雪者的方向和速度'''
        self.angle += direction
        # 负数代表左边
        if self.angle < -2 :
            self.angle = -2
        # 正数代表右边
        if self.angle > 2:
            self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 第一个元素是小人儿左右移动的速度
        # 第二个元素是场景向上滚动的速度
        speed = [self.angle, 6-abs(self.angle)*2]
        return speed
    
    def move(self,speed):
        '''滑雪者左右移动'''
        self.rect.centerx += speed[0]
        # 防止越界
        if self.rect.centerx < 20:
            self.rect.centerx = 20
        if self.rect.centerx > 620:
            self.rect.centerx = 620

class ObstacleClass(pygame.sprite.Sprite):
    '''树和小旗的类'''
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        # type有两种，一个是tree, 一个是flag
        self.type = type
        self.passed = False

    def update(self):
        '''让场景向上滚动'''
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()

def create_map():
    '''创建随机的树和小旗'''
    global obstacles
    locations = []
    for i in range(10):
        row = random.randint(0,9)
        col = random.randint(0,9)
        location = [col*64+20, row*64+20+640]
        if not location in locations:
            locations.append(location)
            type = random.choice(['tree','flag'])
            if type == 'tree':
                img = 'skier_tree.png'
            else:
                img = 'skier_flag.png'
            obstacle = ObstacleClass(img,location,type)
            obstacles.add(obstacle)

def animate():
    '''重绘屏幕'''
    # 填充白色背景
    screen.fill((255,255,255))
    obstacles.draw(screen)
    screen.blit(skier.image,skier.rect)
    screen.blit(score_text,[10,10])
    pygame.display.flip()
        


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640,640))
    clock = pygame.time.Clock()
    skier = SkierClass()
    speed = [0,6]
    # 障碍物放到一个精灵组里统一管理
    obstacles = pygame.sprite.Group()
    map_position = 0
    # 分数
    points = 0
    # 创建的小旗子和树的数量最多为10
    create_map()
    font = pygame.font.SysFont(None,50)
    running = True
    while running:
        # 每秒三十帧
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pl.QUIT:
                running = False
            if event.type == pl.KEYDOWN:
                if event.key == pl.K_LEFT:
                    speed = skier.turn(-1)
                elif event.key == pl.K_RIGHT:
                    speed = skier.turn(1)
        skier.move(speed)
        # 一个屏幕滑过去了，就要创建新的一屏幕障碍物
        map_position += speed[1]
        if map_position >= 640:
            create_map()
            map_position = 0
        # 第三个参数表示碰撞不需要让障碍消失
        hit = pygame.sprite.spritecollide(skier,obstacles,False)
        if hit:
            if hit[0].type == 'tree' and not hit[0].passed:
                points -= 100
                skier.image = pygame.image.load('skier_crash.png')
                animate()
                pygame.time.delay(1000)
                skier.image = pygame.image.load('skier_down.png')
                skier.angle = 0
                speed = [0,6]
                # 把已经撞过的数的passed参数改为True，这样就不会重复撞同一棵树了
                hit[0].passed = True
            elif hit[0].type == 'flag' and not hit[0].passed:
                points += 10
                # 撞到小旗就让小旗消失
                hit[0].kill()
        obstacles.update()
        score_text = font.render(f'Score: {points}',1,(0,0,0))
        animate()
    pygame.quit()
    sys.exit()


