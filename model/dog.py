import random
from model.model import Net
import torch.nn as nn
from torch.nn import functional as F
import torch
import numpy as np
import torch.optim as optim
import json
from model.memory import Memory

_LIVE_LEARNING_RATE = 0.05
_MEMORY_LEARNING_RATE = 0.01


class Dog:
    def __init__(self, moves, num_possible_commands):
        self.device = torch.device('cpu')
        self.moves = moves
        self.commands = set()
        self.max_commands = num_possible_commands
        self.itom = {i: m for i, m in enumerate(moves)}
        self.mtoi = {m: i for i, m in self.itom.items()}
        self.model = Net(num_possible_commands, 20, len(moves)).to(self.device)
        self.memory = Memory(1000)
        
        print(self.itom)

    def update_vocabulary(self, word):
        if word in self.commands:
            return 0
        self.mtoi[word] = len(self.moves)+len(self.commands)   
        self.itom[len(self.moves)+len(self.commands)] = word
        self.commands.add(word)

        return 1

    def _get_input(self, command):
        x = torch.zeros(self.max_commands, dtype=torch.float).to(self.device)
        x[self.mtoi[command]-len(self.moves)] = 1
        return x

    def predict(self, command):
        with torch.no_grad():
            output = self.model(self._get_input(command))
            next_move = torch.multinomial(output, 1)
            return self.itom[next_move.item()]

    def learn(self, command, action, reward):    
        optimizer = optim.Adam(self.model.parameters(), lr=_LIVE_LEARNING_RATE)
        action_t = torch.tensor(self.mtoi[action], dtype=torch.long)
        reward_t = torch.tensor(int(reward), dtype=torch.float)

        self.memory.push(self._get_input(command), action_t, reward_t)
        output_prob = self.model(self._get_input(command))
        loss = -torch.log(output_prob[action_t])*reward_t
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    def replay_memory(self):
        optimizer = optim.Adam(self.model.parameters(), lr=_MEMORY_LEARNING_RATE)
        for command_t, action_t, reward_t in self.memory.sample(10):
            output_prob = self.model(command_t)
            loss = -torch.log(output_prob[action_t])*reward_t
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

