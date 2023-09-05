class Memory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.memory = []

	def push(self, command, action, reward):
		if len(self.memory) >= self.capacity:
		   	self.memory.pop(0)
		self.memory.append((command, action, reward))

	def sample(self, batch_size):
		return random.sample(self.memory, batch_size)
