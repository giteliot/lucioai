import pygame

TESTING_OFFSET = 80
END_OFFSET = 200

class TextManager:
	def __init__(self, screen_w, screen_h, font):
		self.screen_h = screen_h
		self.screen_w = screen_w
		self.messages = {
			0: "Press any key to start teaching Lucio\nPress Enter to move to the next stage",
			1: "Press 'q' to reward Lucio\nPress 'e' to bonk him (please be gentle)\nPress ESC to cancel\nPress Enter to move to the next stage",
			2: "You already reached the maximum number of moves! (4)\nPress any key to start teaching Lucio",
			11: "An evil cat scratched poor little Lucio, press any key to restart",
			13: "A very mad sir bonked poor little Lucio, press any key to restart",
			17: "Little Lucio managed to reach the end! He clearly learned a lot!\nPress Enter to restart or any other key to quit the game."
		}
		self.font = font
		pygame.font.init()


	def get_msg_obj(self, state):
		current_offset = TESTING_OFFSET
		if state > 2:
			current_offset = END_OFFSET
		msg_array = self.messages[state].split("\n")
		text_height = sum(self.font.size(line)[1] for line in msg_array)
		msg_pos_y = self.screen_h - text_height - current_offset
		offset = min(len(s) for s in msg_array)

		out = []
		for msg in msg_array:
			text_surface = self.font.render(msg, True, (255, 255, 255))
			text_width = text_surface.get_width()
			msg_pos_x = self.screen_w/2-130-offset
			out.append((text_surface, text_surface.get_rect(topleft=(msg_pos_x, msg_pos_y))))
			msg_pos_y += text_surface.get_height()+10

		return out
