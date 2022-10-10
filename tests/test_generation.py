from code_translator import *


if __name__ == '__main__':
    # res = get_generation('Python 3 code for Dijkstra\'s Algorithm')
    # print(res)
    #
    # res = get_modification(res[0], 'Remove all comments')
    # print(res)

    code = '''import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self, input_dim=28*28, hidden_dim=256, output_dim=10):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = x.view(-1, 28*28)
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))
        return self.fc3(h)'''

    query = 'Convert PyTorch model to Tensorflow'

    res = get_modification(code, query)
    print(res)
