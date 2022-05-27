import os
import torch
import torch.nn as nn
import torch.nn.functional as F


class Linear_QNet(nn.Module):
    def __init__(self, input_size, number_of_layers, layer_sizes, output_size):
        super().__init__()
        if number_of_layers == 1:
            self.qnet = nn.Linear(input_size, layer_sizes[0])
            self.qnet2 = nn.Linear(layer_sizes[0], output_size)


    def forward(self, x):
        x = F.relu(self.qnet(x))
        x = self.qnet2(x)
        return x


    # model.pth
    def save_to_file(self, folder_path, file_name):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)
        torch.save(self.state_dict(), file_path)