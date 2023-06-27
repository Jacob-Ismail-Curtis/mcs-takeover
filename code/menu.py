import pygame
from level import Level
from settings import *
from translate import Translator

class Menu():
	def __init__(self, game):
		self.game = game
		self.half_width, self.half_height = WIDTH / 2, HEIGHT / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0, 0, 20, 20)
		self.offset = - 100
		self.text_color=TEXT_COLOUR
		
		self.language=game.language
		self.difficulty=game.difficulty
	
	def draw_text(self, text, size, x, y ):
		font = pygame.font.Font(font_name,size)

		# if self.language!="en":
		# 	text=self.translate_text(text, self.language)
		# else:

		text_surface = font.render(text, True, self.text_color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		self.game.display.blit(text_surface,text_rect)

	def translate_text(self, text, target_language):
		# Initialize the translator
		translator= Translator(to_lang=target_language)
		# Translate the text
		translation = translator.translate(text)
		return translation


	def draw_cursor(self):
		self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

	def blit_screen(self):
		self.game.window.blit(self.game.display, (0, 0))
		pygame.display.update()
		self.game.reset_keys()

class MainMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = "Start"
		self.startx, self.starty = self.half_width, self.half_height + 30
		self.instructionsx, self.instructionsy = self.half_width, self.half_height + 50
		self.optionsx, self.optionsy = self.half_width, self.half_height + 70
		self.creditsx, self.creditsy = self.half_width, self.half_height + 90
		self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

		print(self.language, self.difficulty)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BACKGROUND_COLOUR)
			self.draw_text('MCS Takeover: Rise of the Robots', 45, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text('Main Menu', 40, WIDTH / 2, HEIGHT / 2 - 20)
			self.draw_text("Start Game", 20, self.startx, self.starty)
			self.draw_text("Instructions", 20, self.instructionsx, self.instructionsy)
			self.draw_text("Options", 20, self.optionsx, self.optionsy)
			self.draw_text("Credits", 20, self.creditsx, self.creditsy)
			self.draw_text("Use 'wasd' to navigate menu, BACKSPACE to go back and ENTER to select.", 15, WIDTH/2, HEIGHT-100)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'Start':
				self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
				self.state = 'Instructions'
			elif self.state == 'Instructions':
				self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
				self.state = 'Options'
			elif self.state == 'Options':
				self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
				self.state = 'Credits'
			elif self.state == 'Credits':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'Start'
		elif self.game.UP_KEY:
			if self.state == 'Start':
				self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
				self.state = 'Credits'
			elif self.state == 'Instructions':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'Start'
			elif self.state == 'Options':
				self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
				self.state = 'Instructions'
			elif self.state == 'Credits':
				self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
				self.state = 'Options'

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			if self.state == 'Start':
				self.game.curr_menu = self.game.cut_scene1
			elif self.state == 'Instructions':
				self.game.curr_menu = self.game.instructions
			elif self.state == 'Options':
				self.game.curr_menu = self.game.options
			elif self.state == 'Credits':
				self.game.curr_menu = self.game.credits
			self.run_display = False

class OptionsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Language'
		self.languagex, self.languagey = self.half_width, self.half_height + 20
		self.volx, self.voly = self.half_width, self.half_height + 40
		self.difficultyx, self.difficultyy = self.half_width, self.half_height + 60
		self.cursor_rect.midtop = (self.languagex + self.offset, self.languagey)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((BACKGROUND_COLOUR))
			self.draw_text('Options', 20, WIDTH / 2, HEIGHT / 2 - 30)
			self.draw_text("Language", 15, self.languagex, self.languagey)
			self.draw_text("Volume", 15, self.volx, self.voly)
			self.draw_text("Difficulty", 15, self.difficultyx, self.difficultyy)
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			# TO-DO: Create a Volume Menu and a difficulty Menu
			if self.state == 'Language':
				self.game.curr_menu = self.game.languages
			elif self.state == 'Volume':
				self.game.curr_menu = self.game.volume_menu
			elif self.state == 'Difficulty':
				self.game.curr_menu = self.game.difficulty_menu
			self.run_display = False

	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
		elif self.game.DOWN_KEY:
			if self.state == 'Language':
				self.state = 'Volume'
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
			elif self.state == 'Volume':
				self.state = 'Difficulty'
				self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
			elif self.state == 'Difficulty':
				self.state = 'Language'
				self.cursor_rect.midtop = (self.languagex + self.offset, self.languagey)
		elif self.game.UP_KEY:
			if self.state == 'Language':
				self.state = 'Difficulty'
				self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
			elif self.state == 'Difficulty':
				self.state = 'Volume'
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
			elif self.state == 'Volume':
				self.state = 'Language'
				self.cursor_rect.midtop = (self.languagex + self.offset, self.languagey)

class LanguagesMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = "English"

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((BACKGROUND_COLOUR))
			self.draw_cursor()
			self.draw_text('Languages', 20, WIDTH / 2, HEIGHT / 2 - 30)
			self.language_options()
			self.blit_screen()

	def language_options(self):
		self.languages = {"English":"en", "Spanish":"es", "French":"fr"}
		self.language_list=list(self.languages)
		for language, language_code in self.languages.items():
			self.language_index=self.language_list.index(language)
			self.draw_text(language, 15, self.half_width, self.half_height+20*self.language_index+1)

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			self.game.language=self.languages[self.state]
			self.game.curr_menu = self.game.main_menu
			self.run_display = False

	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
		elif self.game.DOWN_KEY:
			self.language_index=(self.language_list.index(self.state)+1)%len(self.language_list)
			self.state=self.language_list[self.language_index]
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.language_list.index(self.state)+1)
		elif self.game.UP_KEY:
			self.language_index=(self.language_list.index(self.state)-1)%len(self.language_list)
			self.state=self.language_list[self.language_index]
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.language_list.index(self.state)+1)

	def blit_screen(self):
		self.game.window.blit(self.game.display, (0, 0))
		pygame.display.update()
		self.game.reset_keys()

class InstructionsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
			self.game.display.fill(BACKGROUND_COLOUR)
			self.draw_text('Instructions', 20, WIDTH / 2, HEIGHT / 2 - 20)
			self.draw_text('w: Move Up', 15, WIDTH / 2, HEIGHT / 2 + 10)
			self.draw_text('s: Move Down', 15, WIDTH / 2, HEIGHT / 2 + 30)
			self.draw_text('a: Move Left', 15, WIDTH / 2, HEIGHT / 2 + 50)
			self.draw_text('d: Move Right', 15, WIDTH / 2, HEIGHT / 2 + 70)
			self.draw_text('x: Switch Weapons', 15, WIDTH / 2, HEIGHT / 2 + 90)
			self.draw_text('c: Special Ability', 15, WIDTH / 2, HEIGHT / 2 + 110)
			self.draw_text('p: Upgrade Menu', 15, WIDTH / 2, HEIGHT / 2 + 130)
			self.draw_text('Shift: Sprint', 15, WIDTH / 2, HEIGHT / 2 + 150)
			self.draw_text('Mouse Click: Shoot', 15, WIDTH / 2, HEIGHT / 2 + 170)
			self.blit_screen()

class CreditsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
			self.game.display.fill(BACKGROUND_COLOUR)
			self.draw_text('Credits', 20, WIDTH / 2, HEIGHT / 2 - 20)
			self.draw_text('Coursework by Jacob Curtis for Multimedia and Game Development module at Durham University. ', 15, WIDTH / 2, HEIGHT / 2 + 10)
			self.blit_screen()

class DifficultyMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 0

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((BACKGROUND_COLOUR))
			self.draw_cursor()
			self.draw_text('Difficulty', 20, WIDTH / 2, HEIGHT / 2 - 30)
			self.select_difficulty()
			self.blit_screen()

	def select_difficulty(self):
		self.difficulty_options = {"Easy":0, "Medium":1, "Hard":2}
		for difficulty, index in self.difficulty_options.items():
			self.draw_text(difficulty, 15, self.half_width, self.half_height+20*index+1)

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			self.game.difficulty=self.state
			self.game.curr_menu = self.game.main_menu
			self.run_display = False

	def move_cursor(self):
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
		elif self.game.DOWN_KEY:
			self.state=(self.state+1)%len(self.difficulty_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)
		elif self.game.UP_KEY:
			self.state=(self.state-1)%len(self.difficulty_options)
			self.cursor_rect.midtop = (self.half_width + self.offset, self.half_height+20*self.state+1)

class VolumeMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.volume = 50

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((BACKGROUND_COLOUR))
			self.draw_text('Volume', 20, WIDTH / 2, HEIGHT / 2 - 30)
			self.set_volume()
			self.blit_screen()

	def set_volume(self):
		self.draw_text(str(self.volume), 20, self.half_width, self.half_height+20)


	def check_input(self):
		self.controls()
		if self.game.START_KEY:
			self.game.volume=self.volume
			self.game.curr_menu = self.game.main_menu
			self.run_display = False

	def controls(self):
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
		elif self.game.DOWN_KEY:
			if self.volume>0:
				self.volume-=1
		elif self.game.UP_KEY:
			if self.volume<100:
				self.volume+=1

class CutScene1(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BACKGROUND_COLOUR)
			self.draw_text('AI TAKEOVER', 60, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text('Durham University is a renowned seat of learning, where students bustle', 20, WIDTH/2, HEIGHT/2+20)
			self.draw_text('about the lush campus with academic excitement. At the top of the hill,', 20, WIDTH/2, HEIGHT/2+50)
			self.draw_text('is the Maths and Computer Science building, alive with students rushing', 20, WIDTH/2, HEIGHT/2+80)
			self.draw_text('to their next lecture and professors undertaking exciting academic research.', 20, WIDTH/2,  HEIGHT/2+110)
			self.draw_text('There is no research more exciting than the robotics department, which is', 20, WIDTH/2,  HEIGHT/2+140)
			self.draw_text('among the best in the world. All seemed normal that day when...', 20, WIDTH/2,  HEIGHT/2+170)
			self.draw_text("Press ENTER to continue", 20, WIDTH/2, HEIGHT-100)
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			self.game.curr_menu=self.game.cut_scene2
			self.run_display = False
		elif self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False

class CutScene2(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BLACK)
			self.text_color=WHITE
			self.draw_text('AI TAKEOVER', 60, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text("Suddenly, the building's lights flicker, then go out completely, sending", 20, WIDTH/2, HEIGHT/2+20)
			self.draw_text('the nearby students into a frenzy of fear and confusion. Rogue robots', 20, WIDTH/2, HEIGHT/2+50)
			self.draw_text('are wreaking havoc, their relentless mechanical strides echoing', 20, WIDTH/2, HEIGHT/2+80)
			self.draw_text('through the now dark and deserted halls. The once-promising', 20, WIDTH/2,  HEIGHT/2+110)
			self.draw_text("research project of the university's leading professors has taken", 20, WIDTH/2,  HEIGHT/2+140)
			self.draw_text('a turn for the worst. The AI robots, once created toaid and ', 20, WIDTH/2,  HEIGHT/2+170)
			self.draw_text("serve, have gained consciousness and taken control, turning the", 20, WIDTH/2,  HEIGHT/2+200)
			self.draw_text(" building into a fortress of terror!", 20, WIDTH/2,  HEIGHT/2+230)
			self.draw_text("Press ENTER to continue", 20, WIDTH/2, HEIGHT-100)
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			self.game.curr_menu = self.game.cut_scene3
			self.run_display = False
		elif self.game.BACK_KEY:
			self.game.curr_menu = self.game.cut_scene1
			self.run_display = False

class CutScene3(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BLACK)
			self.text_color=WHITE
			self.draw_text('AI TAKEOVER', 60, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text("You are that student, tasked with venturing into the heart of the", 20, WIDTH/2, HEIGHT/2+20)
			self.draw_text('infested building. Your mission is to take out the rogue robots floor by floor', 20, WIDTH/2, HEIGHT/2+50)
			self.draw_text("meeting all the professors and uncovering the truth behind the AI's uprising.", 20, WIDTH/2, HEIGHT/2+80)
			self.draw_text('Only by reclaiming the building, can the university and its people be saved.', 20, WIDTH/2,  HEIGHT/2+110)
			self.draw_text("Press ENTER to play", 20, WIDTH/2, HEIGHT-100)
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			self.game.playing = True
			self.run_display = False
		elif self.game.BACK_KEY:
			self.game.curr_menu = self.game.cut_scene2
			self.run_display = False

class DeathScene(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BLACK)
			self.text_color=WHITE
			self.draw_text('YOU DIED', 60, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text("Unfortunately the robots won.", 20, WIDTH/2, HEIGHT/2+20)
			self.draw_text("Press ENTER to return to menu", 20, WIDTH/2, HEIGHT-100)
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			self.game.running = False
			self.run_display = False

class WinScene(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		#print(self.game.volume, self.game.difficulty, self.game.language)
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(BACKGROUND_COLOUR)
			self.text_color=WHITE
			self.draw_text('YOU WON', 60, WIDTH / 2, HEIGHT / 2 -120)
			self.draw_text("You destroyed the robots and reclaimed the Maths and Computer Science building.", 20, WIDTH/2, HEIGHT/2+20)
			self.draw_text("Who would have thought that Matthew Johnson was the villain!", 20, WIDTH/2, HEIGHT/2+40)
			self.draw_text("Press ENTER to return to return to the menu", 20, WIDTH/2, HEIGHT-100)
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			self.game.running = False
			self.run_display = False



