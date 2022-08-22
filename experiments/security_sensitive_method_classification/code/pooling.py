import torch
import torch.nn as nn

class Pooling(nn.Module):
    def __init__(self, pooling_type):
        super().__init__()
        self.pooling_type = pooling_type

    def forward(self, embeddings, attention_mask):
        if self.pooling_type == "cls":
            return embeddings[:, 0]
        if self.pooling_type == "mean":
            x = 1 # finish later
        if self.pooling_type == "max":
            x = 1 # finish later