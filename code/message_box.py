import pygame, os
from settings import *


class Message_Box():
    def __init__(self, level):
        self.current_message = ''
        self.level=level
        self.display_surface = self.level.display_surface
        self.font = pygame.font.Font(font_name,14)
        self.end=False
        #font
    
    def draw_quest_box(self):
        pygame.draw.rect(self.display_surface, BOX_COLOR, pygame.Rect(10, 70, 430, 200))
        self.draw_message('Floor '+str(self.level.current_level)+' - MCS BUILDING', 40, 20, 90, WHITE)
        self.draw_message(str(len(self.level.attackable_sprites))+' robots remaining', 30, 20, 125, WHITE)
        self.draw_message(str(self.level.npcs_met)+'/'+str(self.level.level_data["npc_count"])+' lectures to meet', 30, 20, 140, WHITE)
        if self.level.note_found:
            self.draw_message('Note: ', 30, 20, 170, WHITE)
            self.draw_message('Password: DurHam123', 30, 20, 190, WHITE)

    def draw_message_box(self):
        pygame.draw.rect(self.display_surface, BOX_COLOR, pygame.Rect(10, HEIGHT-130, 430, 130))
        self.draw_message('Messages', 30, 20, HEIGHT-115, WHITE)
        #self.draw_message(self.current_message, 10, 10, HEIGHT-95, TEXT_COLOUR)
        #print(self.current_message())

    def update(self):
        self.draw_message_box()
        self.draw_quest_box()
        self.split_message=self.current_message.split(' ')
        self.lines=self.split_lines(self.split_message)

        # print(self.split_message)
        # print(self.lines)

        #Next message
        self.write_text(self.lines[self.level.message_count*5:(self.level.message_count+1)*5]) 
     

    #Issues here
    def split_lines(self, words):
        lines=[]

    # 2D array where each row is a list of words.
        max_width = 400
        x=20
        for word in words:
            if word!='':
                word_surface = self.font.render(str(word+' '), 0, WHITE)
                word_width, word_height = word_surface.get_size()
                #print(word_width)
                if x + word_width >= max_width:
                    x = 20
                    line=words[0:words.index(word)] 
                    lines.append(line)
                    words=(words[words.index(word)::])
                x += word_width
        line=words[0::] 
        lines.append(line)
        return lines

    def write_text(self,text):
        for x in range(0, len(text)):
            new_message=' '.join(text[x])

            text_surface = self.font.render(new_message,0, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (20, HEIGHT-(95-x*15))
            self.display_surface.blit(text_surface, text_rect)

    def draw_message(self, text, size, x, y, colour):
        text_surface = self.font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.display_surface.blit(text_surface,text_rect)
