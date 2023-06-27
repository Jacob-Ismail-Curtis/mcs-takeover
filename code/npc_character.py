import pygame, random, os
import numpy as np
from settings import *
from character import Character
from support import *


class NPC_Character(Character):
	def __init__(self,character_name,pos,npc_number,groups,obstacle_sprites):
		# general setup
		super().__init__(groups)
		self.sprite_type = 'npc_character'

		# graphics setup
		self.import_graphics(character_name)
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.2
		self.image = pygame.image.load(os.path.dirname(__file__)+'/'+'../graphics/npc_characters1/'+character_name+'/down_idle/idle_down.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-15,-15)

		# movement
		self.direction = pygame.math.Vector2()
		self.last_time_moved=0
		self.obstacle_sprites = obstacle_sprites

		# stats
		self.character_name = "npc2"
		self.npc_number=npc_number
		self.character_info= character_data[self.npc_number]
		self.name=self.character_info["name"]

		# player interaction
		self.isInteracting = False
		self.met = False
		self.step_count=random.randint(5,20)

	def import_graphics(self,name):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
		'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

		character_path = os.path.dirname(__file__)+'/'+'../graphics/npc_characters1/'+name+'/'
		#print(character_path)
		for animation in self.animations.keys():
			full_path = character_path + animation
			#print(full_path)
			self.animations[animation] = import_folder(full_path)

	def get_player_distance_direction(self,player):
		npc_character_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - npc_character_vec).magnitude()

		if distance > 0:
			direction = (npc_character_vec - player_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def random_movement(self, player):
		if self.isInteracting==False:
			if self.step_count<1:
				directions=["left", "right", "up","down"]
				probability=[0.25,0.25, 0.25, 0.25]
				direction = np.random.choice(directions, p=probability)
				
				if direction=="right":
					self.direction=pygame.math.Vector2(1, 0)
					self.status="right"
				elif direction=="left":
					self.direction=pygame.math.Vector2(-1, 0)
					self.status="left"
				elif direction=="down":
					self.direction=pygame.math.Vector2(0, -1)
					self.status="up"
				else:
					self.direction=pygame.math.Vector2(0, 1)
					self.status="down"
				self.step_count=random.randint(5,20)
		else:
			self.direction = pygame.math.Vector2()

	def move_npc(self, player):
		current_time=pygame.time.get_ticks()
		if current_time-self.last_time_moved>=100:
			self.last_time_moved=current_time
			self.step_count-=1
			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			self.hitbox.x += self.direction.x*3
			self.hitbox.y += self.direction.y*3
			collision = False
			for obstacle in self.obstacle_sprites:
				if self.hitbox.colliderect(obstacle.rect):
					if obstacle.sprite_type != "npc_character":
						collision = True
						break
			if self.hitbox.colliderect(player):
				collision=True
				#make npc face player
				if "left" in player.status:
					self.status="right"
				elif "right" in player.status:
					self.status="left"
				elif "up" in player.status:
					self.status="down"
				else:
					self.status="up"
				
			if collision:
				self.hitbox.x -= self.direction.x * 3
				self.hitbox.y -= self.direction.y * 3
	
			self.rect.center = self.hitbox.center


	def get_status(self):
		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status:
				self.status = self.status + '_idle'


	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def cooldown(self):
		if not self.can_attack:
			current_time = pygame.time.get_ticks()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True
	
	def actions(self,player):
		distance= self.get_player_distance_direction(player)[0]
		if distance<=150 and distance>=100:
			self.direction = self.get_player_distance_direction(player)[1]
		else: 
			self.direction = pygame.math.Vector2()

	def update(self):
		pass
		#self.cooldown()

	def sprite_update(self, player):
		self.random_movement(player)
		self.move_npc(player)
		self.get_status()
		self.animate()
		#self.get_status()
		# self.actions(player)