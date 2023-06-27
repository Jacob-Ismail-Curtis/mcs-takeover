import pygame
from settings import *
from support import import_folder

class Menu2():
	def __init__(self, game):
		self.game = game
		self.half_width, self.half_height = WIDTH / 2, HEIGHT / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0, 0, 20, 20)
		self.offset = - 100
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
		
	def draw_text(self, text, size, x, y, display_surface):
		font = pygame.font.Font(font_name,size)

		text_surface = font.render(text, True, WHITE)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		display_surface.blit(text_surface,text_rect)

	def draw_text_left(self, text, size, x, y, display_surface):
		font = pygame.font.Font(font_name,size)

		text_surface = font.render(text, True, WHITE)
		text_rect = text_surface.get_rect()
		text_rect.topleft = (x,y)
		display_surface.blit(text_surface,text_rect)


	def blit_screen(self, display_surface):
		display_surface.blit(display_surface, (0, 0))
		pygame.display.update()
		# self.game.reset_keys()

class ComputerScreen(Menu2):
	def __init__(self, game):
		Menu2.__init__(self, game)
		self.text_color=WHITE

	def display_menu(self, display_surface):

		self.game.check_events()
		self.menu_rect = pygame.Rect((0, 0), (900, 700))
		self.menu_rect.center=(self.half_width,self.half_height)
		pygame.draw.rect(display_surface, BLACK, self.menu_rect)
		self.check_input(display_surface)
		self.blit_screen(display_surface)
	
	def check_input(self, display_surface):

		self.draw_text_left("Password: "+self.game.user_input, 20, 350, 200, display_surface)

		if self.game.password_check:
			self.draw_text_left("PASSWORD CORRECT", 20, 350, 220, display_surface)
			self.draw_text_left("SYSTEM UNLOCKED", 20, 350, 240, display_surface)
			self.draw_text_left("C>USERS>MATTHEW JOHNSON", 20, 350, 260, display_surface)
			self.draw_text_left("NOW RUNNING: ROBOT_TAKEOVER.exe", 20, 350, 280, display_surface)
			self.draw_text('PRESS ESC TO KILL SCRIPT',20, WIDTH / 2, 700, display_surface)
		else:
			self.draw_text('SYSTEM LOCKED',30, WIDTH / 2, 150, display_surface)
			self.draw_text('PRESS ESC TO LEAVE COMPUTER',20, WIDTH / 2, 700, display_surface)

		if self.game.ESC_KEY:
			self.game.level.game_paused = False
			self.game.level.space_pressed = False
			self.game.level.player_interacting_computer=True
			if self.game.password_check:
				self.game.level.game_won=True
