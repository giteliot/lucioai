from components.images import lucio_base, lucio_crouch, lucio_jump, lucio_sit, lucio_walk
import random

class LucioManager:
	def __init__(self):
		self.base = lucio_base
		self.animations = [lucio_crouch, lucio_jump, lucio_sit, lucio_walk]

	def get_animation(self):
		return self.animations[random.randint(0, 3)]

	def get_base(self):
		return self.base
