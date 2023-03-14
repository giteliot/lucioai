import random
from model.model import LSTM
import torch

moves = {
    "STOP",
    "STAY",
    "UP",
    "LEFT",
    "RIGHT",
    "DOWN",
    "STAND",
    "SIT"
}

itom = {i: m for i, m in enumerate(moves)}
mtoi = {m: i for i, m in enumerate(moves)}


class Dog:
    def __init__(self):
        self.device = torch.device('cpu')
        self.model = LSTM(4, 2, len(moves)).to(self.device)

    def predict(self, text, temperature=0.8):
        model.eval()
        with torch.no_grad():
            hidden = None
            for char in text:
                x = torch.zeros(1, 1, input_size).to(device)
                x[0, 0, char_to_idx[char]] = 1
                output, hidden = self.model(x, hidden)
            preds = nn.functional.softmax(output / temperature, dim=-1).squeeze().cpu().numpy()
            next_char = np.random.choice(len(preds), p=preds)
            return idx_to_char[next_char]


def get_random_action():
    return itom[random.randint(0, len(moves)-1)]


def get_random_seq():
    r = get_random_action()
    print(r)
    if r == "STOP":
        return [r]
    return [r]+get_random_seq()
