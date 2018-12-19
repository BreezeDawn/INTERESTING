import os
import pygame
import random
from pygame.locals import *


class CreatLadders(object):
    """创造梯子类"""

    def __init__(self, screen):
        """梯子创造初始化"""
        self.screen = screen
        self.ladders = []

    def creat_ladder(self):
        """随机几率创造梯子,并将梯子对象添加到梯子列表"""
        num = random.randint(0, 100)
        if num == 50:
            # 如果梯子出生点刚刚创建了梯子,创造的梯子就要知道上一个刚刚创建的梯子坐标,以防重合
            if self.judge_coincide():
                ladder = Ladder(self.screen, self.judge_coincide())
                self.ladders.append(ladder)
                return
            # 如果出生点刚刚没有创建梯子,则直接随机x坐标创建梯子
            ladder = Ladder(self.screen)
            self.ladders.append(ladder)

    def display(self):
        """控制所有梯子的移动,并调用判断梯子是否越界"""
        for l in self.ladders:
            l.move()
            self.is_out(l)

    def is_out(self, l):
        """梯子越界时,从梯子列表中移除"""
        if l.y < 0:
            self.ladders.remove(l)

    def judge_coincide(self):
        """判断梯子出生点是否刚刚创建梯子"""
        # 如果梯子列表中有梯子则开始判断
        if self.ladders:
            # 遍历梯子列表
            for ladder in self.ladders:
                # 如果梯子列表中有梯子在梯子出生点,就返回出生点梯子的x临界值
                if ladder.y in range(693, 700):
                    return ladder.xboom


class Ladder(object):
    """单个静态梯子类"""

    def __init__(self, screen, x=0):
        """静态梯子初始化"""
        self.y = 700
        self.type = 'static'
        self.screen = screen
        self.image = pygame.image.load('./image/ladder_1.png')
        # 新梯子的x坐标不与上个梯子x坐标重合
        if x >= 440:
            self.x = random.randint(0, x - 54)
            return
        self.x = random.randint(x, 440)

    def move(self):
        """梯子的自然移动,并更新梯子的临界坐标"""
        self.y -= 1
        self.yboom = self.y + 7
        self.xboom = self.x + 54
        self.screen.blit(self.image, (self.x, self.y))


class Human(object):
    def __init__(self, screen):
        """人物初始化"""
        self.y = 0
        self.x = 220
        self.screen = screen
        self.image = pygame.image.load('./image/super1.png')

    def display(self, ladders):
        """调用人物是否越界死亡,并根据人物是否在梯子上返回跳跃标记"""
        self.is_out()
        space_judge = self.judge_y(ladders)
        self.screen.blit(self.image, (self.x, self.y))
        return space_judge

    def judge_y(self, ladders):
        """人物自然下落,在梯子上时则随梯子上升,并返回可跳跃标记"""
        all_list = [x for x in range(self.x, self.x + 48)]
        if ladders:
            for l in ladders:
                if self.y + 48 in range(l.y, l.yboom):
                    for i in all_list:
                        if i in range(l.x, l.xboom):
                            self.y -= 1
                            return 1
        self.y += 1

    def is_out(self):
        """如果人物越上/下界,程序退出"""
        if self.y > 700 or self.y < 0:
            os._exit(0)

    def move_down(self):
        self.y += 2

    # 人物控制/左
    def move_left(self):
        if self.x >= 0:
            self.x -= 2

    # 人物控制/右
    def move_right(self):
        if self.x <= 432:
            self.x += 2

    # 人物控制/跳跃
    def move_space(self):
        self.y -= 40


class Map(object):
    """动态地图的实现"""

    def __init__(self, screen):
        """地图初始化两张轮播图"""
        self.image1_y = 10
        self.image2_y = 700
        self.screen = screen
        self.image1 = pygame.image.load('./image/background.png')
        self.image2 = pygame.image.load('./image/background.png')

    def display(self):
        """调用地图移动,并调用地图移动是否越界"""
        self.move()
        self.is_out()
        self.screen.blit(self.image1, (0, self.image1_y))
        self.screen.blit(self.image1, (0, self.image2_y))

    def move(self):
        """两张图一起移动"""
        self.image1_y -= 1
        self.image2_y -= 1

    def is_out(self):
        """如果其中一张超出界面上限就刷新在界面下限"""
        if self.image1_y + 852 <= 0:
            self.image1_y = 700
        if self.image2_y + 852 <= 0:
            self.image2_y = 700


def main():
    # 创建窗体
    screen = pygame.display.set_mode((480, 700), 0, 32)
    # 创建动态背景图
    map = Map(screen)
    # 创建人物对象
    human = Human(screen)
    # 创建楼梯对象
    ladders = CreatLadders(screen)
    # 初始化键盘按键字典
    move = {K_a: 0, K_d: 0, K_s: 0, K_SPACE: 0}
    while True:
        # 地图显示
        map.display()
        # 随机创建梯子
        ladders.creat_ladder()
        # 梯子显示
        ladders.display()
        # 人物显示并返回是否可以跳跃标记
        space_judge = human.display(ladders.ladders)
        # 刷新界面
        pygame.display.update()
        # 判断键盘按键
        for event in pygame.event.get():
            # 退出键
            if event.type == QUIT:
                os._exit(0)
                # 键盘有键按下
            if event.type == KEYDOWN:
                # 从按键字典中寻找按键映射,若有,更改标记
                if event.key in move.keys():
                    move[event.key] = 1
            # 键盘有键松开
            if event.type == KEYUP:
                # 从按键字典中寻找按键映射,若有,更改标记
                if event.key in move.keys():
                    move[event.key] = 0
        # 根据字典标记值执行下/左/右/跳跃方法
        if move[K_s] == 1:
            human.move_down()
        if move[K_a] == 1:
            human.move_left()
        if move[K_d] == 1:
            human.move_right()
        if move[K_SPACE] == 1:
            # 当人物返回值标记允许跳跃时才可以跳跃
            if space_judge == 1:
                human.move_space()
                move[K_SPACE] = 0


if __name__ == '__main__':
    main()
