import random
from model.model import LSTM
import torch.nn as nn
from torch.nn import functional as F
import torch
import numpy as np
import torch.optim as optim

_LEARNING_RATE = 0.1


class Dog:
    def __init__(self, moves, num_possible_commands):
        self.device = torch.device('cpu')
        self.moves = moves
        self.commands = set()
        self.max_commands = num_possible_commands
        self.itom = {i: m for i, m in enumerate(moves)}
        self.mtoi = {m: i for i, m in enumerate(moves)}
        self.model = LSTM(num_possible_commands, 20, len(moves)).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=_LEARNING_RATE)
        self.temperature = 1.0

    def update_vocabulary(self, word):
        if word in self.commands:
            return 0
        self.mtoi[word] = len(self.moves)
        self.itom[len(self.moves)] = word
        self.commands.add(word)

        return 1

    def predict(self, command):
        # self.model.eval()
        hidden = None
        x = torch.zeros(1, 1, self.max_commands).to(self.device)
        x[0, 0, self.mtoi[command]] = 1
        output, hidden = self.model(x, hidden)
        preds = nn.functional.softmax(output / self.temperature, dim=-1).squeeze().cpu().detach().numpy()
        next_move = np.random.choice(len(preds), p=preds)
        print(f"out={output}")
        print(f"preds={preds} -> {next_move} -> {np.sum(preds)}")
        return self.itom[next_move]

    def learn(self, output, reward):
        if int(reward) > 0 and self.temperature > 0.05:
            self.temperature = self.temperature/2
        action = torch.tensor(self.mtoi[output], dtype=torch.float)
        reward_t = torch.tensor(int(reward), dtype=torch.float)
        log_prob = torch.log_softmax(action, dim=0)
        log_prob.requires_grad = True
        policy_gradient = log_prob * reward_t
        self.optimizer.zero_grad()
        policy_gradient.backward()
        self.optimizer.step()
        print(f"dog learned: {action} - {reward_t} - {self.temperature} - {policy_gradient}")
