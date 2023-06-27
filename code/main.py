import pygame, sys, os, queue
from player import Player
from settings import *
from menu import *
from upgrade_menu import *
from computer_screen import *

class Game:
	def __init__(self):
		os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
		# general setup
		pygame.init()
		
		self.running, self.playing = True, False
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
		self.difficulty, self.language, self.volume= 0, "en", 50
		self.clock = pygame.time.Clock()

		self.display = pygame.Surface((WIDTH, HEIGHT))
		self.window = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('MCS TAKEOVER: Rise of the Robots')

		self.language, self.volume, self.difficulty = "en", 50, 0
		self.current_level=1
		self.obstacle_sprites=[]
		self.visible_sprites=[]
		self.player = None
		self.level = Level(self.current_level, self.player)
		
		self.main_menu = MainMenu(self)
		self.instructions=InstructionsMenu(self)
		self.options = OptionsMenu(self)
		self.languages = LanguagesMenu(self)
		self.volume_menu = VolumeMenu(self)
		self.difficulty_menu = DifficultyMenu(self)
		self.credits = CreditsMenu(self)
		self.cut_scene1 = CutScene1(self)
		self.cut_scene2 = CutScene2(self)
		self.cut_scene3 = CutScene3(self)
		self.death_scene = DeathScene(self)
		self.win_scene = WinScene(self)
		self.curr_menu = self.main_menu

				#upgrade menu
		self.upgrade_menu = UpgradeMenu(self)
		self.abilities_menu= AbilitiesMenu(self)
		self.gun_menu = GunMenu(self)
		self.curr_upgrade_menu=self.upgrade_menu
		
		#Computer screen
		self.user_input=""
		self.computer_screen = ComputerScreen(self)
		self.password_check=False

	def run(self):
		while self.playing:
			
			self.check_events()

			self.window.fill(BACKGROUND_COLOUR)
			self.level.volume=self.volume*0.01
			self.level.run()
			
			if self.level.game_paused:
				if self.level.player_interacting_computer:
					self.computer_screen.display_menu(self.level.display_surface)
				else:
					self.curr_upgrade_menu.display_menu(self.level.display_surface)

			if self.level.player.check_death()==True:
				self.curr_menu=self.death_scene
				self.playing=False

			if self.level.game_won:
				self.curr_menu=self.win_scene
				self.playing=False

			if self.level.level_beaten and self.level.stairs_found:
				self.current_level += 1
				self.player = self.level.player
				self.level = Level(self.current_level, self.player)


			pygame.display.update()
			self.clock.tick(FPS)
			self.reset_keys()
	

	def check_events(self):
		events=pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.running, self.playing = False, False
				self.curr_menu.run_display = False
			if event.type == pygame.KEYDOWN:
				if self.level.player_on_computer:
					#computer inputs
					if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == " ":
						self.user_input += event.unicode
					if event.key == pygame.K_BACKSPACE:
						self.user_input = self.user_input[:-1]
					if event.key == pygame.K_RETURN:
						if self.user_input == "DurHam123":
							self.password_check = True
						else:
							self.user_input = "Password incorrect"
						if self.user_input == "Password incorrect":
							pygame.time.wait(1000)
							self.user_input  = ""
					if event.key== pygame.K_ESCAPE:
						self.ESC_KEY=True

				if event.key == pygame.K_RETURN:
					self.START_KEY = True
				if event.key == pygame.K_BACKSPACE:
					self.BACK_KEY = True
				if event.key == pygame.K_s:
					self.DOWN_KEY = True
				if event.key == pygame.K_w:
					self.UP_KEY = True
				if event.key == pygame.K_x:
					self.level.player.switch_gun()
					#print(self.level.player.current_gun)
				if event.key == pygame.K_c:
					if self.level.player.is_ability_maxed:
						self.level.ability_set_off=pygame.time.get_ticks()
						self.level.player.ability_on=True
						#resetting ability numbers
						self.level.player.current_ability=0
						self.level.player.is_ability_maxed=False

				if event.key == pygame.K_SPACE:
					if self.level.player_interacting_npc==True:
						self.level.message_count+=1
					if self.level.player_on_computer:
						self.level.space_pressed=True
				
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						self.level.toggle_menu()
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.level.mouse_click()

	def reset_keys(self):
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False

if __name__ == '__main__':
	game = Game()
	while game.running:

		game.curr_menu.display_menu()
		game.run()