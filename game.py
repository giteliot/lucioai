import pygame
import sys
from components.images import bg_image
from components.texts import TextManager
from components.lucio import LucioManager


class Game:
    def __init__(self, game_name, screen_width, screen_height):
        pygame.init()
        pygame.display.set_caption(game_name)

        self.screen_width = screen_width
        self.scree_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.tm = TextManager(screen_width, screen_height, self.font)
        self.lm = LucioManager()
        self.state = 0
        self.frame_index = 0


    def start(self):
        lucio = self.lm.get_base()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if self.state == 0:
                        self.frame_index = 0
                        lucio = self.lm.get_animation()
                        self.state = 1
                    

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg_image, bg_image.get_rect(topleft=( (self.screen_width - bg_image.get_width())/2, 0)))
            self.screen.blit(\
                lucio[self.frame_index], lucio[self.frame_index].\
                get_rect(topleft=((self.screen_width - lucio[self.frame_index].get_width())/2+20, 120))\
            )

            self.frame_index = (self.frame_index+1)%8
            if self.frame_index == 0:
                lucio = self.lm.get_base()

            msg, msg_pos = self.tm.get_msg_obj(self.state)
            self.screen.blit(msg, msg_pos)
            pygame.display.flip()
            self.clock.tick(10)  
        
Game("lucioai", 800, 600).start()





