# coding=utf-8
# 1 - 导入需要的库
import math
import pygame
from pygame.locals import *

# 2 - 初始化游戏
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]  # 上下左右方向键
playerpos = [100, 100]  # 兔子起始位置
acc = [0, 0]  # 跟踪玩家精度，分别记录射出的箭数和被击中的关的数量
arrows = []  # 跟踪箭头



# 3 - 加载图片
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")

# 4 - 保持循环通过
while 1:
	# 5 - 在建立屏幕之前清除屏幕（黑色）
	screen.fill(0)
	# 6 - 初始化屏幕
	# # - 循环铺设绿色草地背景图案
	for x in range(width / grass.get_width() + 1):
		for y in range(width / grass.get_height() + 1):
			screen.blit(grass, (x * 100, y * 100))

	# # - 在屏幕上建立4个城堡图案
	screen.blit(castle, (0, 30))
	screen.blit(castle, (0, 135))
	screen.blit(castle, (0, 240))
	screen.blit(castle, (0, 345))

	# # -在屏幕上建立游戏人员图案
	# screen.blit(player, (100, 100))
	# screen.blit(player, playerpos)
	position = pygame.mouse.get_pos()  # 获取鼠标位置
	angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))  # 计算鼠标与兔子位置角度
	playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)  # 超鼠标方向旋转兔子
	playerpos1 = (
	playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)  # 计算旋转后兔子的位置
	screen.blit(playerrot, playerpos1)

	# 7 - 更新屏幕
	pygame.display.flip()
	# 8 - 循环通过这个事件
	for event in pygame.event.get():
		# - 检查事件是否是退出按钮
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
		# -检查键盘上下左右按键情况
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
			elif event.key == K_a:
				keys[1] = False
			elif event.key == K_s:
				keys[2] = False
			elif event.key == K_d:
				keys[3] = False
	# 9 - 移动游戏人员
	if keys[0]:
		playerpos[1] -= 5
	elif keys[2]:
		playerpos[1] += 5
	if keys[1]:
		playerpos[0] -= 5
	elif keys[3]:
		playerpos[0] += 5