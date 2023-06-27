import pygame, math, os, random
from settings import *
from particles import BulletTrail

class Bullet(pygame.sprite.Sprite):
	def __init__(self,groups, x, y, mouse_x, mouse_y, bullet_image, visible_sprites):
		super().__init__(groups)
		self.sprite_type = 'bullet'
		self.bullet_image=bullet_image
		self.visible_sprites = visible_sprites
		self.image=pygame.image.load(os.path.dirname(__file__)+'/'+'../graphics/guns/'+bullet_image).convert_alpha()
		self.x = x
		self.y = y
		self.rect = self.image.get_rect(center = (self.x, self.y))

		self.mouse_x = mouse_x
		self.mouse_y = mouse_y
		
		self.speed =25
		self.angle = math.atan2(y-mouse_y, x-mouse_x)
		self.x_vel = math.cos(self.angle) * self.speed
		self.y_vel = math.sin(self.angle) * self.speed


	
	def move(self, attackable_sprites):
		self.x -= int(self.x_vel)
		self.y -= int(self.y_vel)
		self.rect.x = self.x
		self.rect.y = self.y

		# BulletTrail(self.rect.centerx, self.rect.centery, 
		# 	random.randint(2,3),
		# 	random.randint(2,8),
		# 	(random.uniform(-1, 1), 
		# 	random.uniform(-1, 1)), self.visible_sprites)

		# if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
		# 	self.kill()

