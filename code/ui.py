import pygame
import os
from settings import *
from support import import_folder


class UI:
	def __init__(self, level):

		# general
		self.display_surface = pygame.display.get_surface()
		self.level=level
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		# bar setup
		self.health_bar_rect = pygame.Rect(10, 40, HEALTH_BAR_WIDTH, BAR_HEIGHT)
		self.ability_bar_rect = pygame.Rect(240, 40, HEALTH_BAR_WIDTH, BAR_HEIGHT)

		#coin animation
		self.frame_index=0
		self.animation_speed=0.1

		self.gun_graphics = []
		for gun in gun1_data.values():
			path = gun['graphic']
			gun = pygame.image.load(path).convert_alpha()
			self.gun_graphics.append(gun)

		pygame.mouse.set_visible(False)

	def show_health_bar(self, current, max_amount, bg_rect, color):
		# draw max stat bar
		pygame.draw.rect(self.display_surface, TEXT_COLOUR, bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# draw current stat bar
		pygame.draw.rect(self.display_surface, color, current_rect)
        # draw border bar
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

		self.draw_text('Health', 25, 10, 10, WHITE)
	
	def show_ability_bar(self, player, bg_rect, color):

		# draw max stat bar
		pygame.draw.rect(self.display_surface, TEXT_COLOUR, bg_rect)

		current_rect = bg_rect.copy()

		if player.is_ability_maxed==True:
			color=WHITE
			current_width=bg_rect.width
		else:
			ratio = player.current_ability /player.max_ability
			current_width = bg_rect.width * ratio

		current_rect.width = current_width
		# draw current stat bar
		pygame.draw.rect(self.display_surface, color, current_rect)
        # draw border bar
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

		self.draw_text('ABILITY', 25, 240, 10, WHITE)

	def draw_coin_ui(self,coin_count):
		coin_path=GRAPHICS_PATH+'coin'
		images=import_folder(coin_path)
		self.frame_index = (self.frame_index + self.animation_speed) % len(images)
		coin_image=images[int(self.frame_index)]

		self.display_surface.blit(coin_image,( 1300, 10))
		self.draw_text("x"+str(coin_count), 30, 1370, 30, WHITE)

	def draw_text(self, text, size, x, y, colour):
		text_surface = self.font.render(text, True, colour)
		text_rect = text_surface.get_rect()
		text_rect.topleft = (x,y)
		self.display_surface.blit(text_surface,text_rect)

	def setup_crosshairs(self):
		#Setup crosshairs
		# Load the image for the cursor
		crosshair_image = pygame.image.load(os.path.dirname(__file__)+'/'+'../graphics/guns/crosshair.png')
		crosshair_rect=crosshair_image.get_rect()
		crosshair_rect.center = pygame.mouse.get_pos()  # update position 
		self.display_surface.blit(crosshair_image, crosshair_rect) # draw the cursor

	def render_lighting(self):
		if self.level.lights_on==False:
		# lighting effect
			self.fog = pygame.Surface((WIDTH, HEIGHT))
			self.fog.fill(NIGHT_COLOR)
			self.light_mask = pygame.image.load(LIGHT_MASK).convert_alpha()
			self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
			self.light_rect = self.light_mask.get_rect()

		# draw the light mask (gradient) onto fog image
			self.fog.fill(NIGHT_COLOR)
			self.light_rect.center = (WIDTH/2, HEIGHT/2)
			self.fog.blit(self.light_mask, self.light_rect)
			self.display_surface.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

	def gun_overlay(self):
		bg_rect = pygame.Rect(WIDTH-130,HEIGHT-130,130,130)
		pygame.draw.rect(self.display_surface,BOX_COLOR,bg_rect)
		gun = pygame.image.load(os.path.dirname(__file__)+'/'+self.level.player.gun_graphic).convert_alpha()
		gun_rect = gun.get_rect(center = bg_rect.center)
		self.draw_gun_text(self.level.player.current_gun.upper(), 10, WIDTH-110, HEIGHT-125, WHITE)

		self.display_surface.blit(gun,gun_rect)

	def draw_gun_text(self, text, size, x, y, colour):
		self.gun_font = pygame.font.Font(UI_FONT, 10)
		text_surface = self.gun_font.render(text, True, colour)
		text_rect = text_surface.get_rect()
		text_rect.topleft = (x,y)
		self.display_surface.blit(text_surface,text_rect)

	def display(self,player):
		#lighting
		self.render_lighting()
		#draw crosshairs for cursor
		self.setup_crosshairs()
		# show health bar
		self.show_health_bar(player.current_health,player.max_health,self.health_bar_rect,HEALTH_COLOR)
		self.show_ability_bar(player,self.ability_bar_rect,ABILITY_COLOR)
		# show gun overlay
		self.gun_overlay()
		#draw coin ui
		self.draw_coin_ui(player.coins)
		

