import pygame, os, math, random
from settings import *
from support import import_folder
from character import Character
from upgrade_menu import *
from particles import Dust

class Player(Character):
	def __init__(self,pos,groups,obstacle_sprites, visible_sprites):
		super().__init__(groups)
		self.image = pygame.image.load(os.path.dirname(__file__)+'/'+'../graphics/player/down_idle/idle_down.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.inflate(-5,-5)

		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.4

		# movement 
		self.direction = pygame.math.Vector2()
		#self.speed = 4
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.last_time=0

		# player stats

		self.max_health = 100
		self.current_health = 100
		self.health_boost=10

		self.max_ability = 100
		self.current_ability = 50
		self.ability_loss_time=200
		self.is_ability_maxed=False
		self.ability_on=False
		self.ability_duration=3000

		self.regular_speed=8
		self.sprint_speed=9

		#coins
		self.coins = 20

		#guns
		self.current_gun="Pistol"
		self.gun_index=0
		self.guns=["Pistol"]
		self.gun_damage=gun_data[self.current_gun]['damage']
		self.gun_graphic=gun1_data[self.current_gun]['graphic']


		# damage timer
		self.speed_level, self.health_level, self.ability_level, self.damage_level = 1, 1, 1, 1
		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

		# interacting
		self.sprites_colliding = False
		self.space_pressed = False
		
		# sprite groups
		self.obstacle_sprites = obstacle_sprites
		self.visible_sprites = visible_sprites
		self.bullet_sprites = pygame.sprite.Group()
		#
		self.message_count=True

		#sounds
		self.bullet_sound = pygame.mixer.Sound(AUDIO_PATH+'bullet.wav')
		self.bullet_sound.set_volume(0.4)
		self.walk_sound = pygame.mixer.Sound(AUDIO_PATH+'walk.wav')
		self.walk_sound.set_volume(0.7)
		self.last_walk_sound=0


	def import_player_assets(self):
		character_path = os.path.dirname(__file__)+'/'+'../graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):

		if not self.attacking:
			self.keys = pygame.key.get_pressed()

			# movement input
			if self.keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
				for bullet in self.bullet_sprites:
					bullet.y+=1*self.speed

			elif self.keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'

				for bullet in self.bullet_sprites:
					bullet.y-=1*self.speed
			else:
				self.direction.y = 0

			if self.keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'

				for bullet in self.bullet_sprites:
					bullet.x-=1*self.speed
			elif self.keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'

				for bullet in self.bullet_sprites:
					bullet.x+=1*self.speed
			else:
				self.direction.x = 0

			if self.keys[pygame.K_SPACE]:
				if self.sprites_colliding == True:
					self.space_pressed = True
				else:
					self.space_pressed = False

			if self.keys[pygame.K_LSHIFT]:
				self.speed=self.sprint_speed
				self.animation_speed=0.6
			else:
				self.speed=self.regular_speed
				self.animation_speed=0.4

	def get_status(self):
		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		else:
			self.create_dust_particles()

		# attacking status
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def create_dust_particles(self):
		Dust(self.rect.centerx, self.rect.centery, 
								  random.randint(2,5),
								  random.randint(2,8),
								  (random.uniform(-1, 1), 
								  random.uniform(-1, 1)), self.visible_sprites)
		self.play_walk_sound()

	def play_walk_sound(self):
		current_time=pygame.time.get_ticks()
		if current_time-self.last_walk_sound>=500:
			self.walk_sound.play()
			self.last_walk_sound=current_time
	
	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if current_time-self.last_time>=self.ability_loss_time:
			if self.current_ability>=1 and self.is_ability_maxed==False:
				self.current_ability=int(self.current_ability-1)
			self.last_time=current_time

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + gun_data[self.current_gun]['cooldown']:
				self.attacking = False

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True
		
	def switch_gun(self):
		print(self.guns)
		self.gun_index=(self.gun_index+1)%len(self.guns)
		self.current_gun=self.guns[(self.gun_index)]
		self.gun_graphic=gun1_data[self.current_gun]['graphic']


	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)


	def check_death(self):
		if self.current_health <= 0:
			self.kill()
			return True

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.check_death()