import pygame
import sys
from components.images import bg_image, mad_bat, evil_cat, end_pole
from components.texts import TextManager
from components.lucio import LucioManager, MaxCommandsError, POS_KEY, NEG_KEY, Moves


class Game:
    def __init__(self, game_name):
        pygame.init()
        pygame.display.set_caption(game_name)

        self.screen_width = 800
        self.world_width = 1200
        self.screen_height = 600
        self.floor = 400


        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.tm = TextManager(self.screen_width, self.screen_height, self.font)
        self.lm = LucioManager()

        self.state = 0
        self.training_state = [0, 1, 2]
        self.testing_state = [5]
        self.ending_state = [11, 13, 17]
        self.frame_index = 0
        self.frame_rate = 30
        self.max_frames = 8
        self.gravity = 0.8
        self.init_lucio_pos()

    def init_lucio_pos(self):
        self.lucio = self.lm.get_base()
        self.lucio_height = 150
        self.lucio_x = 40
        self.lucio_y = self.floor-self.lucio_height-30
        self.lucio_sp_x = 0
        self.lucio_sp_y = 0
        self.break_speed = 0
        self.jumping = False
        self.walking = False

        self.mad_bat_x = 800
        self.mad_bat_y = 70

        self.evil_cat_x = 450
        self.evil_cat_y = 350

        self.end_pole_x = 1300
        self.end_pole_y = 350


    def render_training(self):
            frame_index = int(self.frame_index/2)
            if frame_index >= self.max_frames:
                frame_index = 0
                self.lucio = self.lm.get_base()

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg_image, bg_image.get_rect(topleft=( (self.screen_width - bg_image.get_width())/2, 0)))
            self.screen.blit(\
                self.lucio[frame_index], self.lucio[frame_index].\
                get_rect(topleft=((self.screen_width - self.lucio[frame_index].get_width())/2+20, 120))\
            )              

            msgs = self.tm.get_msg_obj(self.state)
            for msg, msg_pos in msgs:
                self.screen.blit(msg, msg_pos)

    def render_testing(self, cmd):
        frame_index = int(self.frame_index/4)%self.max_frames
        bg_frame_index = int(self.frame_index/15)%2

        move = None
        
        if cmd is not None and self.jumping == False:
            try:
                move = self.lm.get_move(cmd).item()
            except MaxCommandsError as e:
                return
            if move == Moves.WALK.value:
                self.walking = True
                self.lucio_sp_x = 4
                self.break_speed = 0
            elif move == Moves.JUMP.value:
                self.lucio = self.lm.get_base()
                self.jumping = True
                self.frame_index = 0
                self.lucio_sp_y = -15 -self.gravity
            else:
                if move == Moves.SIT.value:
                    self.lucio_sp_x = 0
                if move == Moves.CROUCH.value:
                    if self.walking == True:
                        self.break_speed = 0.05
                self.lucio = self.lm.get_animation(move)
                self.walking = False

        if self.walking == True:
            self.lucio = self.lm.get_animation(Moves.WALK.value)

        if self.jumping == True:
            self.lucio_sp_y += self.gravity

        if self.break_speed > 0:
            self.lucio_sp_x -= self.break_speed
            if self.lucio_sp_x <= 0:
                self.lucio_sp_x = 0
                self.break_speed = 0
                self.lucio = self.lm.get_base()

        self.lucio_x += max(0, min(self.lucio_sp_x, self.world_width - self.screen_width))
        self.lucio_y += self.lucio_sp_y

        if self.lucio_y >= self.floor-self.lucio_height-30:
            self.lucio_y = self.floor-self.lucio_height-30
            self.jumping = False
            self.lucio_sp_y = 0

        if self.evil_cat_x-self.lucio_x > 210 and\
            self.evil_cat_x-self.lucio_x < 275 and\
             self.evil_cat_y-self.lucio_y < 180:
                print(f"CATE ATE YOU")
                self.state = 11

        if self.mad_bat_x-self.lucio_x > 350 and\
            self.mad_bat_x-self.lucio_x < 440 and\
             self.break_speed == 0 and bg_frame_index%2 == 1:
                print(f"MAD BAT HIT YOU")
                self.state = 13

        if self.end_pole_x-self.lucio_x < 700:
            print(f"FINISHED LEVEL!")
            self.state = 17

        pygame.draw.rect(self.screen, (37, 150, 190), (0, 0, self.screen_width, self.floor))
        pygame.draw.rect(self.screen, (73, 190, 37), (0, self.floor, self.screen_width, self.screen_height-self.floor))
        self.screen.blit(\
            evil_cat[bg_frame_index], 
            evil_cat[bg_frame_index].get_rect(topleft=( (self.evil_cat_x - self.lucio_x, self.evil_cat_y)))
            )
        self.screen.blit(\
            mad_bat[bg_frame_index], 
            mad_bat[bg_frame_index].get_rect(topleft=( (self.mad_bat_x - self.lucio_x, self.mad_bat_y)))
            )
        self.screen.blit(\
            end_pole[bg_frame_index], 
            end_pole[bg_frame_index].get_rect(topleft=( (self.end_pole_x - self.lucio_x, self.end_pole_y)))
            )
        self.screen.blit(\
            self.lucio[frame_index], self.lucio[frame_index].\
            get_rect(topleft=(self.lucio_x, self.lucio_y))\
        )

    def render_ending(self, cmd):
        self.screen.fill((0, 0, 0))
        msgs = self.tm.get_msg_obj(self.state)
        for msg, msg_pos in msgs:
            self.screen.blit(msg, msg_pos)

        if self.state == 11:
            self.screen.blit(\
                evil_cat[0], 
                evil_cat[0].get_rect(topleft=( (self.screen_width/2-50, self.screen_height/2-70)))
            )

        if self.state == 13:
            self.screen.blit(\
                mad_bat[1], 
                mad_bat[1].get_rect(topleft=( (self.screen_width/2-110, self.screen_height/2-300)))
            )

        if self.state == 17:
            self.screen.blit(\
                end_pole[0], 
                end_pole[0].get_rect(topleft=( (self.screen_width/2-30, self.screen_height/2-70)))
            )

        if cmd is None:
            return
        if self.state in (11, 13):
            self.state = 5
            self.init_lucio_pos()
            return
        if cmd == pygame.K_RETURN:
            self.state = 5
            self.init_lucio_pos()
            return
        pygame.quit()


    def start(self):

        while True:
            lvl_cmd = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if self.state in self.testing_state:
                        lvl_cmd = event.key
                        if event.key == pygame.K_RETURN:
                            self.init_lucio_pos()
                            lvl_cmd = None
                        if event.key == pygame.K_ESCAPE:
                            self.state = 0
                            lvl_cmd = None
                    elif self.state in self.training_state:
                        if event.key == pygame.K_RETURN:
                            self.state = 5
                        elif self.state in (0, 2):
                            self.frame_index = 0
                            current_cmd = event.key
                            try:
                                move = self.lm.get_move(current_cmd)
                                self.lucio = self.lm.get_animation(move)
                                self.state = 1
                            except MaxCommandsError as e:
                                self.state = 2
                        elif self.state == 1 and event.key in (POS_KEY, NEG_KEY):
                            self.lm.train(current_cmd, move, event.key)
                            self.state = 0
                        elif event.key == pygame.K_ESCAPE:
                            self.state = 0
                    elif self.state in self.ending_state:
                        lvl_cmd = event.key

            self.frame_index = (self.frame_index+1)%self.frame_rate

            if self.state in self.training_state:
                self.render_training()
            elif self.state in self.testing_state:
                self.render_testing(lvl_cmd)
            elif self.state in self.ending_state:
                self.render_ending(lvl_cmd)

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

        
Game("lucioai").start()





