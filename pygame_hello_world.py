import pygame, sys
# 这里面包含很多常量
from pygame.locals import *

## 初始化pygame
pygame.init()

## 设置窗口
# 第一个参数是一个元组，表示宽和高
# 第二个参数是选择展示的方式，默认是0
# 第三个参数是选择色彩深度，默认是0
window_surface = pygame.display.set_mode((500,400),0,32)
# 设置标题
pygame.display.set_caption('Hello World!')

## 设置颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

## 设置字体
# 第一个参数是字体，设置为None就是用默认字体
# 第二个参数是字体大小
basic_font = pygame.font.SysFont(None,48)

## 设置文字的内容和位置
# 第一个参数是文字内容
# 第二个参数设置为True，表示需要平滑效果
# 第三个参数是前景色
# 第四个参数是背景色
text = basic_font.render('Hello World',True,WHITE,BLUE)
# 获取字体对象周围的矩形
text_rect = text.get_rect()
# 设置字体矩形的中心点坐标为窗口的中心点坐标，这样文字就会居中
text_rect.centerx = window_surface.get_rect().centerx
text_rect.centery = window_surface.get_rect().centery

## 给窗口填充白色背景
# 这只是改变了窗口对象的属性，还没有展示给用户
window_surface.fill(WHITE)

## 画一个绿色多边形
# 第一个参数是窗口对象，我们要把图形画到它上面
# 第二个参数是颜色
# 第三个参数是各个顶点的坐标，最后一个点会自动连到第一个点上封口
# 最后一个参数是可选的线条宽度，如果没有，就会填充整个图形
pygame.draw.polygon(window_surface,GREEN,((146,0),(291,106),(236,277),(56,277),(0,106)))

## 画蓝色线条
# 第一个参数是窗口对象，我们要把图形画到它上面
# 第二个参数是线条的颜色
# 第三个参数是起点坐标
# 第四个参数是终点坐标
# 最后一个参数是可选的线条粗细，默认是1
pygame.draw.line(window_surface,BLUE,(60,60),(120,60),4)
pygame.draw.line(window_surface,BLUE,(120,60),(60,120))
pygame.draw.line(window_surface,BLUE,(60,120),(120,120),4)

## 画一个蓝色的圆
# 第一个参数是窗口对象，要画到它上面
# 第二个参数是线条颜色
# 第三个参数是圆心坐标
# 第四个参数是半径
# 最后一个参数是线条粗细，0表示填充整个圆
pygame.draw.circle(window_surface,BLUE,(300,50),20,0)

## 画一个红色的椭圆形
# 第一个参数是窗口对象，把图形画到它上面
# 第二个参数是线条颜色
# 第三个参数是元组，表示椭圆外接矩形的左上角坐标，椭圆的宽度和长度
# 最后一个参数是线条粗细，0表示填充整个椭圆
pygame.draw.ellipse(window_surface,RED,(300,250,40,80),1)

## 绘制文字的背景矩形
# 第一个参数是窗口对象
# 第二个参数是线条颜色
# 第三个参数是元组，分别表示矩形左上角的坐标，宽度，高度
# 我们绘制的这个矩形比字体本身的外接矩形大一圈
pygame.draw.rect(window_surface,RED,(text_rect.left-20,text_rect.top-20,text_rect.width+40,text_rect.height+40))

# 获取窗口的像素数组
pix_array = pygame.PixelArray(window_surface)
# 染黑一个像素点，第一个索引是横坐标，第二个索引是纵坐标
pix_array[480][380] = BLACK
# 像素数组对象会锁住窗口对象，为了让窗口对象能够调用blit方法，需要删除像素数组
del pix_array

## 绘制文字
# 文字和图形不一样，它是画到自己的平面上的
# 为了让文字画到窗口上，需要使用blit方法
# 第一个参数是字体对象
# 第二个参数是字体外接矩形，它保存了文字的位置信息
window_surface.blit(text,text_rect)

## 把窗口画到屏幕上
# 为了节约内存，把窗口上的内容都设置好了，最后才调用一次更细屏幕显示的方法
pygame.display.update()

# 游戏循环
while True:
    # 不停检查键鼠事件
    for event in pygame.event.get():
        if event.type == QUIT:
            # 如果在退出程序之前不退出pygame，idle会挂起一个pygame线程
            pygame.quit()
            sys.exit()