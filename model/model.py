import torch
import torch.nn as nn
import string


# Define the LSTM language model
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden=None):
        if hidden is None:
            h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
            c0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        else:
            h0, c0 = hidden
        output, (hn, cn) = self.lstm(x, (h0, c0))
        output = self.fc(output[:, -1, :])
        return output, (hn, cn)

