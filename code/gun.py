import pygame 

class Gun(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'gun'
		direction = player.status.split('_')[0]

		# graphic
		full_path = f'../graphics/guns/{player.gun}.png'
		self.image = pygame.image.load(full_path).convert_alpha()