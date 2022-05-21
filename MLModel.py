from sre_parse import _OpSubpatternType
import torch
import torch.nn as nn

class MLModel:
    def __init__(self, input_size, between_size, output_size):
        self.qnet = nn.Linear(input_size, between_size)
        self.qnet2 = nn.Linear(between_size, output_size)


    




