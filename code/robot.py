import pygame, random, os, math, queue
from settings import *
from character import Character
from support import *
from player import Player
from enemy_bullet import EnemyBullet


class Robot(Character):
	def __init__(self,current_level,pos,groups, obstacle_sprites, visible_sprites, attackable_sprites, damage_player, trigger_death_particles, drop_coins, drop_heart):

		# general setup
		super().__init__(groups)
		self.sprite_type = 'robot'

		# graphics setup
		self.import_graphics("robots")
		self.status = 'down_idle'
		#print(self.frame_index)
		#print(self.animations)
		self.image = self.animations[self.status][self.frame_index]

		# movement
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.inflate(-5,-5)
		self.obstacle_sprites = obstacle_sprites
		self.visible_sprites = visible_sprites
		self.attackable_sprites = attackable_sprites

		# stats
		self.current_level = current_level
		robot_info = robot_data[self.current_level]
		self.health = robot_info['health']
		#self.coins = robot_info['coins']
		self.speed = robot_info['speed']
		self.attack_damage = robot_info['damage']
		self.resistance = robot_info['resistance']
		self.attack_radius = robot_info['attack_radius']
		self.notice_radius = robot_info['notice_radius']

		# player interaction
		self.can_attack = True
		self.attack_status="idle"
		self.last_attack_time = 0
		self.attack_cooldown = 1000
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.drop_coins = drop_coins
		self.drop_heart = drop_heart

		# invincibility timer
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		#sounds
		self.explosion_sound = pygame.mixer.Sound(AUDIO_PATH+'/../audio/death.wav')
		self.hit_sound = pygame.mixer.Sound(AUDIO_PATH+'/../audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(robot_info['attack_sound'])
		self.explosion_sound.set_volume(0.5)
		self.hit_sound.set_volume(0.6)
		self.attack_sound.set_volume(0.6)

	def import_graphics(self,name):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
		'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}
		main_path = os.path.dirname(__file__)+'/'+'../graphics/robots/'+name+'/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

# fix steering so that robots can go round walls
	def get_player_distance_direction(self,player):
		robot_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - robot_vec).magnitude()

		if distance > 0:
			direction = (player_vec - robot_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance, direction)


	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.attack_status != 'attack':
				self.attack_status="attack"
		elif distance <= self.notice_radius:
			self.attack_status = 'move'
		else:
			self.attack_status = 'idle'

		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status:
				self.status = self.status + '_idle'
		else:
			if abs(self.direction.x)>abs(self.direction.y):
				if self.direction.x>0:
					self.status="right"
				else:
					self.status="left"
			else:
				if self.direction.y>0:
					self.status="down"
				else:
					self.status="up"

	def actions(self,player):
		if self.attack_status=="attack":
			# current_time = pygame.time.get_ticks()
			# if current_time-self.last_attack_time>=self.attack_cooldown:
			# 	display_ratio_x=(WIDTH/MAP_WIDTH)
			# 	display_ratio_y=(HEIGHT/MAP_HEIGHT)
			# 	EnemyBullet([self.visible_sprites,player.bullet_sprites],self.rect.x*display_ratio_x, self.rect.y*display_ratio_y, WIDTH/2, HEIGHT/2, "enemy_bullet.png")
			# 	#EnemyBullet([self.visible_sprites,player.bullet_sprites],WIDTH/2+200, HEIGHT/2+200, WIDTH/2, HEIGHT/2, "enemy_bullet.png")
			# 	self.last_attack_time=current_time
			# # print(player.bullet_sprites)
			# player.bullet_sound.play()

			#collision logic
			self.damage_player(self.attack_damage)
			self.attack_sound.play()
		elif self.attack_status == 'move':

			#Old obstacle avoidance method
			self.direction = self.get_player_distance_direction(player)[1]
			#self.check_obstacle(self.obstacle_sprites)
		else:
			self.direction = pygame.math.Vector2()


	# def check_obstacle(self, obstacles):
	# 	next_pos = self.rect.move(self.direction)  # get the next position of the enemy
	# 	for obstacle in obstacles:
	# 		if next_pos.colliderect(obstacle):  # check if next position collides with obstacle
	# 			# change direction to move around obstacle
	# 			angle = math.atan2(self.direction.y, self.direction.x) + math.pi / 2
	# 			self.direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.attack_status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			self.health -= player.gun_damage
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center, 'robot_death')
			coin_number=random.randint(3,10)
			heart_number=random.randint(0,3)
			for x in range(coin_number):
				self.drop_coins(self.rect.center)
			if heart_number==1:
				self.drop_heart(self.rect.center)
			self.explosion_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldowns()
		self.check_death()

	def sprite_update(self,player):
		self.get_status(player)
		self.actions(player)