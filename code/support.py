from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			if image.endswith(".png") or image.endswith(".jpg"):
				full_path = path + '/' + image
				image_surf = pygame.image.load(full_path).convert_alpha()
				surface_list.append(image_surf)
				#(image)

	return surface_list

def import_folder2(path):
	surface_list = {}

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			#print(full_path)
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list[image]=image_surf

	return surface_list
