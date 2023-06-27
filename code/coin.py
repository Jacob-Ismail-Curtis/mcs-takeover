import pygame, os, random
from support import import_folder
from settings import *

class Coin(pygame.sprite.Sprite):
	def __init__(self, pos, player, groups):
		super().__init__(groups)
		self.sprite_type = 'coin'
		self.player=player
		self.groups=groups

		#animation
		self.frame_index = 0
		self.animation_speed = 0.15


		self.image=self.import_graphics()[self.frame_index]
		self.x, self.y =pos[0], pos[1]
		
		#Spawn in random positions
		self.x+=random.randint(-30,30)
		self.y+=random.randint(-30,30)
		self.rect = self.image.get_rect(center = (self.x, self.y))

		#bounce
		self.bouncing=True
		self.vy = -7  # Initial upward velocity
		self.ay = 1   # Acceleration due to gravity
		self.y_start = self.y  # Starting height of the bounce
		self.bounce_height = 25  # Maximum height of the bounce

						#magnet
		self.attract_distance = 150  # The distance at which the coin starts to be attracted
		self.attract_speed = 40  # The speed at which the coin is attracted


	def import_graphics(self):
		animation = GRAPHICS_PATH+'coin1'
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
				self.vy = -self.vy * random.uniform(0.87,0.97)  # Decrease velocity with each bounce
				self.y = self.y_start - self.bounce_height

			self.rect.center = (self.x, self.y)

	def magnet(self):
		# Calculate the distance between the coin and the player
		distance = ((self.player.rect.center[0] - self.rect.center[0]) ** 2 + 
					(self.player.rect.center[1] - self.rect.center[1]) ** 2) ** 0.5

		# If the distance is less than the attract distance, start attracting the coin
		if distance < self.attract_distance:
			# Calculate the direction of the attraction
			direction = [self.player.rect.center[0] - self.rect.center[0], 
						self.player.rect.center[1] - self.rect.center[1]]

			# Normalize the direction vector
			direction_length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
			direction = [direction[0] / direction_length, direction[1] / direction_length]

			# Scale the attract speed based on the distance
			scaled_speed = self.attract_speed * (1 - distance / self.attract_distance)

			# Move the coin towards the player
			self.x += direction[0] * scaled_speed
			self.y += direction[1] * scaled_speed
			self.rect.center = (self.x, self.y)


	def update(self):
		self.animate()
		self.bounce()
		self.magnet()
