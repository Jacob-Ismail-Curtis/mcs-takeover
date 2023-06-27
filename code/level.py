import pygame, os, random, math
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from npc_character import NPC_Character
from robot import Robot
from particles import AnimationPlayer
from coin import Coin
from heart import Heart
from object import Object
from message_box import Message_Box
from bullet import Bullet
from gun import Gun
from upgrade_menu import *
from ui import UI
from random import *

class Level:
	def __init__(self, current_level, player):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.player=player
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.interactable_sprites =  pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.computer_sprites = pygame.sprite.Group()

		#level data
		self.current_level=current_level
		self.level_data=level_data[self.current_level]
		self.robot_count=self.level_data["robot_count"]
		self.npc_count=self.level_data["npc_count"]
		self.map=self.level_data["map"]
		self.robot_spawns=self.level_data["robot_spawns"]
		self.npc_spawns=self.level_data["npc_spawns"]
		self.computer_dialogue=self.level_data["computer_dialogue"]

		#level status
		self.all_enemies_beaten=False
		self.npcs_met=0
		self.all_npcs_met=False
		self.level_beaten=False
		self.lights_on=False
		self.stairs_found=False

		#events
		self.player_interacting_computer=False
		self.player_interacting_npc=False
		self.player_on_computer=False
		self.note_found=False
		self.npc_number=(self.current_level-1)*4
		self.game_won=False
		
		# UI

		self.game_paused = False
		self.ui = UI(self)

		# message_box
		self.message_box = Message_Box(self)
		self.message_count=0
		self.space_pressed=False

		#clock
		self.clock = pygame.time.Clock()
		self.ability_set_off=0
		
		# sprite setup
		self.create_map()

		#particles
		self.animation_player = AnimationPlayer()

		#game music
		if self.current_level==1:
			self.volume=0.5
			main_sound = pygame.mixer.Sound(AUDIO_PATH+'game_music.wav')
			main_sound.set_volume(self.volume)
			main_sound.play(loops = -1)

		self.last_shot_time=0

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout(os.path.dirname(__file__)+'/'+'../new_map/'+self.map),
			'npc_characters': import_csv_layout(os.path.dirname(__file__)+'/'+'../new_map/'+self.npc_spawns),
			'robots': import_csv_layout(os.path.dirname(__file__)+'/'+'../new_map/'+self.robot_spawns),
			'stair_collision': import_csv_layout(os.path.dirname(__file__)+'/'+'../new_map/map2_stairs.csv'),
			'computer_collision': import_csv_layout(os.path.dirname(__file__)+'/'+'../new_map/map2_computers.csv')
		
		}
		graphics = {
		  	#'npc_character': import_folder(os.path.dirname(__file__)+'/'+'../graphics/npc_characters1/npc_character1')	
		#'object': import_folder2(os.path.dirname(__file__)+'/'+'../graphics/objects1')
		}


		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')

						if style == 'npc_characters':
							self.npc_number+=1
							character_name='npc2'
							NPC_Character(character_name,(x,y),self.npc_number,[self.visible_sprites, self.obstacle_sprites, self.interactable_sprites],self.obstacle_sprites)	
						
						if style == 'robots':

							Robot(self.current_level,(x,y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.visible_sprites, self.attackable_sprites, self.damage_player, self.trigger_death_particles, self.drop_coins, self.drop_heart)	

						if style == 'stair_collision':
							Tile((x,y),[self.obstacle_sprites],'stairs')

						if style== 'computer_collision':
							Tile((x,y),[self.obstacle_sprites, self.computer_sprites],'computers')

			self.create_player()
	
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)

		if self.game_paused:
			pass
		else:
			self.visible_sprites.update()
			self.visible_sprites.character_sprite_update(self.player)
			self.level_status()
			self.npc_interactions()
			self.object_interactions()
			self.handle_gun()
			self.special_ability()
			self.move_bullets()
			self.check_bullet_collisions()
			self.message_box_setup()
			self.blit_screen()

	def create_player(self):
		if self.player==None:
			self.player = Player((1120,2300),[self.visible_sprites], self.obstacle_sprites, self.visible_sprites)
		else:
			self.visible_sprites.add(self.player)

	def level_status(self):
		if len(self.attackable_sprites)==0:
			self.all_enemies_beaten=True
		if self.npcs_met==self.npc_count:
			self.all_npcs_met=True
		if self.all_enemies_beaten==True and self.all_npcs_met==True:
			self.level_beaten=True

		if self.level_beaten:
			self.lights_on=True
			if not self.player_interacting_npc:
				self.message_box.current_message='Well done! You have cleared this floor and got the power back on. Next go to the stairs to go to the next floor.'
		
	def check_bullet_collisions(self):
		#Collisions between robots
		for bullet in self.player.bullet_sprites:
			if bullet.sprite_type=="bullet":
			#Collision between robots
				for attackable_sprite in self.attackable_sprites:
					#Account for offset in camer on rect
					offset_rect_x=attackable_sprite.rect.x-(self.player.rect.centerx - WIDTH/2)
					offset_rect_y=attackable_sprite.rect.y-(self.player.rect.centery - HEIGHT/2)
					if bullet.rect.colliderect((offset_rect_x,offset_rect_y,attackable_sprite.rect.width,attackable_sprite.rect.height)):
						attackable_sprite.get_damage(self.player)
						attackable_sprite.notice_radius=10000

						#Every hit ability increases
						self.player.current_ability+=10
						if self.player.current_ability>=100:
							self.player.is_ability_maxed=True
						bullet.kill()
			#Collisions between obstacles
			for obstacle_sprite in self.obstacle_sprites:
				#Account for offset in camer on rect
				offset_rect_x=obstacle_sprite.rect.x-(self.player.rect.centerx - WIDTH/2)
				offset_rect_y=obstacle_sprite.rect.y-(self.player.rect.centery - HEIGHT/2)
				if bullet.rect.colliderect((offset_rect_x,offset_rect_y,32,32)):
					#smoke particles
					self.animation_player.create_particles("smoke",(obstacle_sprite.rect.centerx,obstacle_sprite.rect.centery),self.visible_sprites)
					
					bullet.kill()

	def handle_gun(self):

		self.player_gun = pygame.image.load(os.path.dirname(__file__)+'/'+gun_data[self.player.current_gun]['graphic']).convert_alpha()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		#Rotates gun and flips when on left side to track mouse
		rel_x, rel_y = mouse_x - WIDTH/2, mouse_y - HEIGHT/2+10
		angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
		self.player_gun_rect = self.player_gun.get_rect()
		self.player_gun_rect.center = (WIDTH/2, HEIGHT/2+10)
		if mouse_x < WIDTH/2:
			self.player_gun = pygame.transform.flip(self.player_gun, True, False)
			angle += 180
		self.player_gun_copy = pygame.transform.rotate(self.player_gun, angle)
		self.player_gun_copy_rect = self.player_gun_copy.get_rect(center=self.player_gun_rect.center)
		# Draws gun to screen
		self.display_surface.blit(self.player_gun_copy, self.player_gun_copy_rect)

	def mouse_click(self):
		#Gets mouse position
		current_time = pygame.time.get_ticks()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if current_time-self.last_shot_time>=gun_data[self.player.current_gun]['cooldown']:
			self.last_shot_time=current_time
			if self.player.current_gun=="shotgun":
				spread = 30 # the spread angle in degrees
				speed=25
				angle = math.atan2(mouse_y - HEIGHT/2, mouse_x - WIDTH/2) # the angle in radians between the center of the bullets and the mouse position
				angle1 = angle - math.radians(spread) # the angle for the first bullet
				angle2 = angle # the angle for the second bullet
				angle3 = angle + math.radians(spread) # the angle for the third bullet

				# calculate the horizontal and vertical offset for each bullet based on the angle and a spread factor
				offset1_x = math.cos(angle1) * speed
				offset1_y = math.sin(angle1) * speed
				offset2_x = math.cos(angle2) * speed
				offset2_y = math.sin(angle2) * speed
				offset3_x = math.cos(angle3) * speed
				offset3_y = math.sin(angle3) * speed

				# create the three bullets with the adjusted mouse_x and mouse_y values
				Bullet([self.visible_sprites,self.player.bullet_sprites],WIDTH/2, HEIGHT/2, mouse_x + offset1_x, mouse_y + offset1_y,"bullet.png", self.visible_sprites)
				Bullet([self.visible_sprites,self.player.bullet_sprites],WIDTH/2, HEIGHT/2, mouse_x + offset2_x, mouse_y + offset2_y, "bullet.png", self.visible_sprites)
				Bullet([self.visible_sprites,self.player.bullet_sprites],WIDTH/2, HEIGHT/2, mouse_x + offset3_x, mouse_y + offset3_y,"bullet.png", self.visible_sprites)

			else:
				Bullet([self.visible_sprites,self.player.bullet_sprites],WIDTH/2, HEIGHT/2, mouse_x, mouse_y, "bullet.png", self.visible_sprites)
			self.player.bullet_sound.play()

	def special_ability(self):
		if self.player.ability_on==True:
			current_time=pygame.time.get_ticks()
			if current_time-self.ability_set_off<=self.player.ability_duration:
				cursor_x, cursor_y=pygame.mouse.get_pos()
				Bullet([self.visible_sprites,self.player.bullet_sprites],WIDTH/2, HEIGHT/2, cursor_x, cursor_y, "bullet.png", self.visible_sprites)
				self.player.bullet_sound.play()
			else:
				self.player.ability_on=False


	def move_bullets(self):
		for bullet in self.player.bullet_sprites:
			bullet.move(self.attackable_sprites)

	def message_box_setup(self):

		if self.message_box.end==True:
			self.message_count=0
		else:
			self.message_box.update()

	def toggle_menu(self):
		self.game_paused = not self.game_paused 
	
	def damage_player(self,amount):
		if self.player.vulnerable:
			self.player.current_health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			#self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	def drop_coins(self, pos):
		self.coin = Coin(pos, self.player,[self.visible_sprites])
		
	def drop_heart(self, pos):
		self.heart=Object(pos, "heart", [self.visible_sprites])

	def npc_interactions(self):
		#At the moment this stops all sprites when interacting
		#collision_sprites = pygame.sprite.spritecollide(self.player,self.interactable_sprites,False)
		#npc interactions
		for interactable_sprite in self.interactable_sprites:
			if pygame.sprite.spritecollide(self.player, self.interactable_sprites, False):
				self.message_box.current_message="Press SPACE to interact"
				self.player.sprites_colliding = True
	
				if self.player.space_pressed == True:
					self.player_interacting_npc = True
					interactable_sprite.isInteracting = True
		

					if self.all_enemies_beaten:
						specific_npc=self.find_npc()
						self.message_box.current_message=specific_npc.character_info["dialogue"]["en"]
						
						#increment npc met
					else:
						self.message_box.current_message="There are still drones left! Please help to destroy them so I can get back to teaching my lectures!"
					#self.player.space_pressed = False
	
			else:
				self.message_box.current_message=""
				self.player_interacting_npc = False
				interactable_sprite.isInteracting = False
				self.player.sprites_colliding = False
				self.player.space_pressed = False

				if not self.player_interacting_computer:
					self.message_count=0

		if self.all_enemies_beaten:
			for npc in self.interactable_sprites:
				if pygame.sprite.collide_rect(self.player, npc):
					if self.player.space_pressed == True:
						if npc.met==False:
							#change to 3
							if self.current_level==3 and npc.name=="Steven Bradley":
								self.heart=Object((npc.rect.x+10, npc.rect.y+10), "note", [self.visible_sprites])
							self.npcs_met+=1
							npc.met=True

	def find_npc(self):
		for sprite in self.interactable_sprites:
			if pygame.sprite.collide_rect(self.player, sprite):
				return sprite

	def object_interactions(self):
		#coin interactions
		for sprite in self.visible_sprites:
			if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'coin':
				if pygame.sprite.collide_rect(self.player,sprite):
					sprite.kill()
					self.player.coins+=1
					coin_sound = pygame.mixer.Sound(AUDIO_PATH+'collect_coin.wav')
					coin_sound.set_volume(0.7)
					coin_sound.play()
			#heart interaction
			elif hasattr(sprite,'sprite_type') and sprite.sprite_type == 'heart':
				if pygame.sprite.collide_rect(self.player,sprite):
					sprite.kill()
					coin_sound = pygame.mixer.Sound(AUDIO_PATH+'collect_coin.wav')
					coin_sound.set_volume(0.7)
					coin_sound.play()
					self.player.current_health+=self.player.health_boost
					if self.player.current_health>100:
						self.player.current_health=100
			
			#note
			elif hasattr(sprite,'sprite_type') and sprite.sprite_type == 'note':
				if pygame.sprite.collide_rect(self.player,sprite):
					sprite.kill()
					self.note_found=True
					get_item_sound = pygame.mixer.Sound(AUDIO_PATH+'get_item.wav')
					get_item_sound.set_volume(0.7)
					get_item_sound.play()

		for sprite in self.computer_sprites:
			if pygame.sprite.spritecollide(self.player, self.computer_sprites, False):
					self.player_on_computer = True
					self.message_box.current_message='Press space to interacting with computer'
					if self.space_pressed:
						self.player_interacting_computer=True
						self.game_paused=True
						# self.message_box.current_message=self.computer_dialogue
			else:
				self.player_on_computer=False
				if not self.player_interacting_npc:
					self.message_count=0

		if self.level_beaten:
			for sprite in self.obstacle_sprites:
				if sprite.sprite_type=="stairs":
					if pygame.sprite.collide_rect(self.player,sprite):
						self.stairs_found=True
					# self.current_level+=1:
	def blit_screen(self):
		self.display_surface.blit(self.display_surface, (0, 0))
		pygame.display.update()
				

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load(os.path.dirname(__file__)+'/'+'../new_map/ground.png').convert_alpha()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)


		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			if hasattr(sprite,'sprite_type') and sprite.sprite_type in["bullet", "bullet_trail"]:
				self.display_surface.blit(sprite.image,sprite.rect.topleft)
			else:
				offset_pos = sprite.rect.topleft - self.offset
				self.draw_sprite(sprite, offset_pos)

	def draw_shadow(self, sprite, offset_pos):
		shadow_image = sprite.image.copy()
		shadow_image.fill((0, 0, 0, 80), special_flags=pygame.BLEND_RGBA_MULT)
		shadow_rect = shadow_image.get_rect(x=offset_pos.x, y=offset_pos.y+3)
		self.display_surface.blit(shadow_image, shadow_rect)

	def draw_sprite(self, sprite, offset_pos):
		self.draw_shadow(sprite, offset_pos)
		self.display_surface.blit(sprite.image, offset_pos)

	def character_sprite_update(self,player):
		character_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type in ['robot', 'npc_character']]
		for sprite in character_sprites:
			sprite.sprite_update(player)
