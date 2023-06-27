import pygame, math, os
from settings import *

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self,groups, x, y, player_x, player_y, bullet_image):
		super().__init__(groups)
		self.sprite_type = 'enemy_bullet'
		self.bullet_image=bullet_image
		self.image=pygame.image.load(os.path.dirname(__file__)+'/'+'../graphics/guns/'+bullet_image).convert_alpha()
		self.x = x
		self.y = y
		self.rect = self.image.get_rect(center = (self.x, self.y))

		self.player_x = player_x
		self.player_y = player_y

		self.speed =20
		self.angle = math.atan2(self.y-self.player_y, self.x-self.player_x)
		self.x_vel = math.cos(self.angle) * self.speed
		self.y_vel = math.sin(self.angle) * self.speed

    
	def move(self, attackable_sprites):
		self.x -= int(self.x_vel)
		self.y -= int(self.y_vel)
		self.rect.x = self.x
		self.rect.y = self.y

		if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
			self.kill()
