import pygame, os, random
from settings import *
from support import import_folder

class AnimationPlayer:
	def __init__(self):
		self.path = os.path.dirname(__file__)+'/../graphics/particles/'
		self.frames = {
			# magic
			'robot_death': import_folder(self.path+'explosion'),
			'smoke':import_folder(self.path+'smoke')}

	def create_particles(self,animation_type,pos,groups):
		animation_frames = self.frames[animation_type]
		ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups):
		super().__init__(groups)
		self.sprite_type = 'particle'
		self.frame_index = 0
		self.animation_speed = 0.3
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()

class Dust(pygame.sprite.Sprite):
	def __init__(self, x, y, size, lifespan, velocity, groups):
		super().__init__(groups)
		self.sprite_type="dust"
		self.image = pygame.Surface([size, size])
		self.color = pygame.Color(121, 121, 121)
		self.image.fill(pygame.Color(self.color))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.lifespan = lifespan
		self.velocity = velocity

	def update(self):
		self.lifespan -= 1
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]
		if self.lifespan <= 0:
			self.kill()

class BulletTrail(pygame.sprite.Sprite):
	def __init__(self, x, y, size, lifespan, velocity, groups):
		super().__init__(groups)
		self.sprite_type="bullet_trail"
		self.image = pygame.Surface([size, size])
		self.color = pygame.Color(HEALTH_COLOR)
		self.image.fill(pygame.Color(self.color))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.lifespan = lifespan
		self.velocity = velocity

	def update(self):
		self.lifespan -= 1
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]
		if self.lifespan <= 0:
			self.kill()