import pygame, os, random
from support import import_folder
from settings import *

class Heart(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.sprite_type = 'heart'
		self.groups=groups

		#animation
		self.frame_index = 0
		self.animation_speed = 0.15


		self.image=self.import_graphics()[self.frame_index]
		self.x, self.y =pos[0], pos[1]
		
		#Spawn in random positions
		self.x+=random.randint(-40,40)
		self.y+=random.randint(-40,40)
		self.rect = self.image.get_rect(center = (self.x, self.y))

				#bounce
		self.bouncing=True
		self.vy = -7  # Initial upward velocity
		self.ay = 1   # Acceleration due to gravity
		self.y_start = self.y  # Starting height of the bounce
		self.bounce_height = 25  # Maximum height of the bounce

	def import_graphics(self):
		animation = GRAPHICS_PATH+'heart'
		return import_folder(animation)

	def animate(self):
		self.frame_index = (self.frame_index + self.animation_speed) % len(self.import_graphics())
		self.image = self.import_graphics()[int(self.frame_index)]


	def bounce(self):
		if self.bouncing:
			self.vy += self.ay
			self.y += self.vy

			# Check if the coin has reached its maximum bounce height
			if self.y > self.y_start - self.bounce_height:
				self.vy = -self.vy * random.uniform(0.87, 0.97)  # Decrease velocity with each bounce
				self.y = self.y_start - self.bounce_height

			self.rect.center = (self.x, self.y)

	def update(self):
		self.animate()
		self.bounce()
