import pygame

class TextManager:
	def __init__(self, screen_w, screen_h, font):
		self.screen_h = screen_h
		self.screen_w = screen_w
		self.messages = {
			0: "Press any key to start teaching Lucio",
			1: "Press 'Q' to reward Lucio, 'E' to beat him mercilessy (any other key to skip)"
		}
		self.font = font
		pygame.font.init()


	def get_msg_obj(self, state):
		text_surface = self.font.render(self.messages[state], True, (255, 255, 255))
		text_width = text_surface.get_width()
		text_height = text_surface.get_height()
		msg_pos_x = (self.screen_w - text_width) // 2
		msg_pos_y = self.screen_h - text_height - 80

		return text_surface, (msg_pos_x, msg_pos_y)