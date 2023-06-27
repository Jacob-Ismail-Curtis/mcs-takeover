import pygame
from settings import *
from support import import_folder

class Menu1():
	def __init__(self, game):
		self.game = game
		self.half_width, self.half_height = WIDTH / 2, HEIGHT / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0, 0, 20, 20)
		self.offset = - 100
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

		#coin animation
		self.frame_index=0
		self.animation_speed=0.1
		
		
	def draw_text(self, text, size, x, y, display_surface):
		font = pygame.font.Font(font_name,size)

		text_surface = font.render(text, True, WHITE)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		display_surface.blit(text_surface,text_rect)

	def draw_cursor(self,display_surface):
		self.draw_text('*', 15, self.cursor_rect.x-50, self.cursor_rect.y, display_surface)

	# def show_coin(self, display_surface):
	# 	coin_path=GRAPHICS_PATH+'coin'
	# 	images=import_folder(coin_path)
	# 	self.frame_index = (self.frame_index + self.animation_speed) % len(images)
	# 	coin_image=images[int(self.frame_index)]
	# 	display_surface.blit(coin_image,( 900, 300))
	# 	self.draw_text("x"+str(self.game.level.player.coins), 25, 1390, 30, display_surface)

	def blit_screen(self, display_surface):
		display_surface.blit(display_surface, (0, 0))
		pygame.display.update()
		# self.game.reset_keys()

class UpgradeMenu(Menu1):
	def __init__(self, game):
		Menu1.__init__(self, game)
		self.state = "Abilities"
		self.abilitiesx, self.abilitiesy = self.half_width, self.half_height + 30
		self.gunsx, self.gunsy = self.half_width, self.half_height + 50
		self.cursor_rect.midtop = (self.abilitiesx + self.offset, self.abilitiesy)

	def display_menu(self, display_surface):

		self.game.check_events()
		self.move_cursor()
		self.menu_rect = pygame.Rect((0, 0), (650, 300))
		self.menu_rect.center=(self.half_width,self.half_height)
		pygame.draw.rect(display_surface, BOX_COLOR, self.menu_rect)
		self.draw_text('Upgrade Menu', 30, WIDTH / 2, HEIGHT / 2 - 40, display_surface)
		self.draw_text("Abilities", 20, self.abilitiesx, self.abilitiesy, display_surface)
		self.draw_text("Guns", 20, self.gunsx, self.gunsy, display_surface)
		self.draw_cursor(display_surface)
		self.blit_screen(display_surface)


	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.level.game_paused = False
		elif self.game.DOWN_KEY:
			print('down')
			if self.state == 'Abilities':
				self.cursor_rect.midtop = (self.gunsx + self.offset, self.gunsy)
				self.state = 'Guns'
			elif self.state == 'Guns':
				self.cursor_rect.midtop = (self.abilitiesx + self.offset, self.abilitiesy)
				self.state = 'Abilities'
		elif self.game.UP_KEY:
			if self.state == 'Abilities':
				self.cursor_rect.midtop = (self.gunsx + self.offset, self.gunsy)
				self.state = 'Guns'
			elif self.state == 'Guns':
				self.cursor_rect.midtop = (self.abilitiesx + self.offset, self.abilitiesy)
				self.state = 'Abilities'
		elif self.game.START_KEY:
			# TO-DO: Create a Volume Menu and a gun Menu
			if self.state == 'Abilities':
				self.game.curr_upgrade_menu = self.game.abilities_menu
			elif self.state == 'Guns':
				self.game.curr_upgrade_menu = self.game.gun_menu

class AbilitiesMenu(Menu1):
	def __init__(self, game):
		Menu1.__init__(self, game)
		self.state = 0
		self.abilitiesx, self.abilitiesy = self.half_width, self.half_height + 30
		self.gunsx, self.gunsy = self.half_width, self.half_height + 50
		self.cursor_rect.midtop = (self.abilitiesx + self.offset, self.abilitiesy)

	def display_menu(self, display_surface):
		self.game.check_events()
		self.move_cursor()
		self.menu_rect = pygame.Rect((0, 0), (650, 300))
		self.menu_rect.center=(self.half_width,self.half_height)
		pygame.draw.rect(display_surface, BOX_COLOR, self.menu_rect)
		self.select_ability(display_surface)
		self.draw_text('Abilities', 30, WIDTH / 2, HEIGHT / 2 - 40, display_surface)
		self.get_ability()
		self.draw_text(self.ability_description[self.get_ability()], 10, WIDTH/2, HEIGHT /2 +100, display_surface)
		self.draw_cursor(display_surface)
		self.blit_screen(display_surface)


	def select_ability(self, display_surface):
		self.ability_options = {"Speed":0, "Health":1, "Ability":2, "Damage":3}
		self.ability_price = {"Speed":20, "Health":20, "Ability":20, "Damage":20}
		self.ability_description = {"Speed":"This upgrade will increase your sprint speed.", "Health":"This upgrade will increase the health increase of hearts dropped by robots. ", "Ability":"This upgrade will decrease the rate of loss of ability.", "Damage":"This upgrade will increase your bullet damage."}
		self.ability_levels =  {"Speed":self.game.level.player.speed_level, "Health":self.game.level.player.health_level, "Ability":self.game.level.player.ability_level, "Damage":self.game.level.player.damage_level}
		for ability, index in self.ability_options.items():
			self.draw_text(ability+": "+str(self.ability_price[ability])+ " coins", 17, self.half_width, self.half_height+20*index+1, display_surface)
			self.draw_text("LVL"+str(self.ability_levels[ability])+"/4", 17, self.half_width+230, self.half_height+20*index+1, display_surface)
	def get_ability(self):
		return next((key for key, val in self.ability_options.items() if val == self.state), None)

	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.curr_upgrade_menu = self.game.upgrade_menu
		elif self.game.DOWN_KEY:
			self.state=(self.state+1)%len(self.ability_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)
		elif self.game.UP_KEY:
			self.state=(self.state-1)%len(self.ability_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)
		elif self.game.START_KEY:
			if self.get_ability().lower()=="speed":
				if self.game.level.player.speed_level<4:
					if self.game.level.player.coins>=20:
						self.game.level.player.speed_level+=1
						self.game.level.player.coins-=20
						self.game.level.player.regular_speed+=1
						self.game.level.player.sprint_speed+=1
						self.game.level.game_paused = False
			elif self.get_ability().lower()=="health":
				if self.game.level.player.health_level<4:
					if self.game.level.player.coins>=20:
						self.game.level.player.health_level+=1
						self.game.level.player.coins-=20
						self.game.level.player.health_boost+=5
						self.game.level.game_paused = False
			elif self.get_ability().lower()=="ability":
				if self.game.level.player.ability_level<4:
					if self.game.level.player.coins>=20:
						self.game.level.player.ability_level+=1
						self.game.level.player.coins-=20
						self.game.level.player.ability_loss_time+=50
						self.game.level.game_paused = False
			elif self.get_ability().lower()=="damage":
				if self.game.level.player.damage_level<4:
					if self.game.level.player.coins>=20:
						self.game.level.player.damage_level+=1
						self.game.level.player.coins-=20
						for x in range(self.game.level.player.damage_level-1):
							self.game.level.player.damage_level*1.2
						self.game.level.game_paused = False
			
			

class GunMenu(Menu1):
	def __init__(self, game):
		Menu1.__init__(self, game)
		self.state = 0
		self.abilitiesx, self.abilitiesy = self.half_width, self.half_height + 30
		self.gunsx, self.gunsy = self.half_width, self.half_height + 50
		self.cursor_rect.midtop = (self.abilitiesx + self.offset, self.abilitiesy)

	def display_menu(self, display_surface):
		self.game.check_events()
		self.move_cursor()
		self.menu_rect = pygame.Rect((0, 0), (650, 300))
		self.menu_rect.center=(self.half_width,self.half_height)
		pygame.draw.rect(display_surface, BOX_COLOR, self.menu_rect)
		self.select_gun(display_surface)
		self.draw_text('Guns', 30, WIDTH / 2, HEIGHT / 2 - 40, display_surface)
		self.draw_text(self.gun_description[self.get_gun()], 10, WIDTH / 2, HEIGHT / 2+100, display_surface)
		self.draw_cursor(display_surface)
		self.blit_screen(display_surface)

	def select_gun(self, display_surface):
		self.gun_options = {"Revolver":0, "Shotgun":1, "Machine Gun":2}
		self.gun_prices = {"Revolver":50, "Shotgun":50, "Machine Gun":50}
		self.gun_description =  {"Revolver":"The revolver does the most damage but has the slow fire rate.", "Shotgun":"The shotgun shoots 3 bullets and is powerful, but has the slowest fire rate ", "Machine Gun":"The machine gun has a low damage rate but has the highest fire rate."}
		for gun, index in self.gun_options.items():
			self.draw_text(gun+": "+str(self.gun_prices[gun])+ " coins", 17, self.half_width, self.half_height+20*index+1, display_surface)
			if gun.lower() in self.game.level.player.guns:
				self.draw_text("Bought", 17, self.half_width+230, self.half_height+20*index+1, display_surface)
	def get_gun(self):
		return next((key for key, val in self.gun_options.items() if val == self.state), None)

	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.curr_upgrade_menu = self.game.upgrade_menu
		elif self.game.DOWN_KEY:
			self.state=(self.state+1)%len(self.gun_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)
		elif self.game.UP_KEY:
			self.state=(self.state-1)%len(self.gun_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)
		elif self.game.START_KEY:
			if not self.get_gun() in self.game.level.player.guns:
				if self.game.level.player.coins>=50:
					self.game.level.player.coins-=50
					self.game.level.player.guns.append(self.get_gun())
					self.game.level.game_paused = False