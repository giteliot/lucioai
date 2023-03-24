import random
from model.model import LSTM
import torch.nn as nn
from torch.nn import functional as F
import torch
import numpy as np


class Dog:
    def __init__(self, moves, num_possible_commands):
        self.device = torch.device('cpu')
        self.moves = moves
        self.commands = set()
        self.max_commands = num_possible_commands
        self.itom = {i: m for i, m in enumerate(moves)}
        self.mtoi = {m: i for i, m in enumerate(moves)}
        self.model = LSTM(num_possible_commands, 2, len(moves)).to(self.device)

    def update_vocabulary(self, word):
        if word in self.commands:
            return 0
        self.mtoi[word] = len(self.moves)
        self.itom[len(self.moves)] = word
        self.commands.add(word)

        print(self.mtoi)
        print(self.itom)
        return 1

    def predict(self, command, temperature=0.8):
        self.model.eval()
        with torch.no_grad():
            hidden = None
            x = torch.zeros(1, 1, self.max_commands).to(self.device)
            x[0, 0, self.mtoi[command]] = 1
            output, hidden = self.model(x, hidden)
            preds = nn.functional.softmax(output / temperature, dim=-1).squeeze().cpu().numpy()
            next_char = np.random.choice(len(preds), p=preds)
            return self.itom[next_char]

