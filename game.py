# coding=utf-8
# /usr/bin/env python

"""学写简单的塔防游戏"""

# 1 - 导入需要的库
import math
import random
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
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194


# 3 - 加载图片
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1

# 4 - 保持循环通过
while 1:
	badtimer -= 1
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


	# 6.1 - 在屏幕上建立游戏人员图案
	position = pygame.mouse.get_pos()  # 获取鼠标位置
	angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))  # 计算鼠标与兔子位置角度
	playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)  # 超鼠标方向旋转兔子
	playerpos1 = (
	playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)  # 计算旋转后兔子的位置
	screen.blit(playerrot, playerpos1)
	# 6.2 - 在屏幕上建立箭头图案
	for bullet in arrows:
		index = 0
		velx = math.cos(bullet[0]) * 10
		vely = math.sin(bullet[0]) * 10
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
			arrows.pop(index)
		index += 1
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
			screen.blit(arrow1, (projectile[1], projectile[2]))
	# 6.3 - 在屏幕上建立獾图案
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 - (badtimer1 * 2)
		if badtimer1 >= 35:
			badtimer1 = 35
		else:
			badtimer1 += 5
	index = 0
	for badguy in badguys:
		if badguy[0] < -64:
			badguys.pop(index)
		badguy[0] -= 7
		# 6.3.1 检查獾是否碰到城堡
		badrect = pygame.Rect(badguyimg.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			healthvalue -= random.randint(5, 20)
			badguys.pop(index)
		# 6.3.2 检查箭头与獾
		index1 = 0
		for bullet in arrows:
			bullrect = pygame.Rect(arrow.get_rect())
			bullrect.left = bullet[1]
			bullrect.top = bullet[2]
			if badrect.colliderect(bullrect):
				acc[0] += 1
				badguys.pop(index)
				arrows.pop(index1)
			index1 += 1
		# 6.3.3-下一个獾
		index += 1
	for badguy in badguys:
		screen.blit(badguyimg, badguy)
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
		if event.type == pygame.MOUSEBUTTONDOWN:
			position = pygame.mouse.get_pos()  # 获取鼠标位置
			acc[1] += 1
			arrows.append(
				[math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32,
				 playerpos1[1] + 32])

	# 9 - 移动游戏人员
	if keys[0]:
		playerpos[1] -= 5
	elif keys[2]:
		playerpos[1] += 5
	if keys[1]:
		playerpos[0] -= 5
	elif keys[3]:
		playerpos[0] += 5