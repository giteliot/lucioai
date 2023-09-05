from components.images import lucio_base, lucio_crouch, lucio_jump, lucio_sit, lucio_walk
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.functional import one_hot
from enum import Enum
import torch.nn.utils as torch_utils

MAX_CMDS = 4
POS_KEY = 113
NEG_KEY = 101

class Moves(Enum):
    CROUCH = 0
    JUMP = 1
    SIT = 2
    WALK = 3

class Net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.ln1 = nn.LayerNorm(hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.ln2 = nn.LayerNorm(hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        
        nn.init.kaiming_uniform_(self.fc1.weight, nonlinearity='relu')
        nn.init.kaiming_uniform_(self.fc2.weight, nonlinearity='relu')

    def forward(self, x):
        out = self.fc1(x)
        out = self.ln1(out)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.ln2(out)
        out = self.relu(out)    
        out = self.fc3(out)
        return nn.functional.softmax(out, dim=-1).squeeze()

class Memory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, command, action, reward):
        if len(self.memory) >= self.capacity:
               self.memory.pop(0)
        self.memory.append((command, action, reward))

    def sample(self, batch_size):
        return random.sample(self.memory, min(len(self.memory), batch_size))
        if len(self.memory) < 2:
            return []
        if len(self.memory) >= 2*batch_size:
            return random.sample(self.memory, batch_size)
        return random.sample(self.memory, int(len(self.memory)/2))

class MaxCommandsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LucioManager:
    def __init__(self):
        self.device = torch.device('cpu')
        self.model = Net(4, 4, 4).to(self.device)
        self.memory = Memory(100)

        self.base_animation = lucio_base
        self.animations = [lucio_crouch, lucio_jump, lucio_sit, lucio_walk]
        self.cmds = []

        self.optimizer = optim.RMSprop(self.model.parameters(), lr=0.001, alpha=0.9)

    def _update_cmds(self, command):
        if command in self.cmds:
            return
        if len(self.cmds) > 3:
            raise MaxCommandsError("maximum number of command already used; use a pre-existing command")
        self.cmds.append(command)

    def _key_to_cmd(self, key):
        return one_hot(torch.tensor(self.cmds.index(key)), 4).float()

    def _get_reward_and_lr(self, move, model_output, good):
        p = model_output[move]
        
        if p > 0.9 and good:
            return None, None

        min_c = 1e-6
        max_c = 0.05
        m = max_c-1*min_c
        q = min_c
        if good:
            m = -1*m
            q = max_c
        lr = m*p + q

        min_c = 1
        max_c = 100
        if not good:
            min_c = -10
            max_c = -1
        m = max_c-1*min_c
        q = min_c
        if good:
            m = -1*m
            q = max_c
        reward = m*p + q

        return reward.item(), lr.item()
        
    def get_move(self, command):
        self._update_cmds(command)
        with torch.no_grad():
            output = self.model(self._key_to_cmd(command))
            return torch.multinomial(output, 1)

    def _base_train(self, command, move, good, is_from_memory):
        command_t = self._key_to_cmd(command)
        output_prob = self.model(command_t)
        
        move_t = torch.tensor(move).long()
        if is_from_memory and output_prob[move_t] >= 0.6:
            return
        
        reward, lr = self._get_reward_and_lr(move, output_prob, good)
        if reward is None:
            return
        reward_t = torch.tensor(reward).float()
        
        
        loss = -torch.log(output_prob[move_t])*reward_t
        
        for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr
        
        self.optimizer.zero_grad()
        loss.backward()
        torch_utils.clip_grad_norm_(self.model.parameters(), max_norm=0.8)
        self.optimizer.step()

    def train(self, command, move, reward_key):
        assert reward_key in (POS_KEY, NEG_KEY), "reward key is not 'q' or 'e'"

        good = reward_key == POS_KEY
        self._base_train(command, move, good, False)
        self.replay_memory()
        self.memory.push(command, move, good)

    def replay_memory(self):
        for command, move, good in self.memory.sample(100):
            self._base_train(command, move, good, True)

    def get_animation(self, command_index):
        return self.animations[command_index]

    def get_base(self):
        return self.base_animation

class Lucio:
    def __init__(self):
        self.x = 40
        self.y = 600
        self.moving = False
        self.jumping = False

    def get_animation(self):
        return None
