import torch.nn as nn

from pooling import Pooling

from transformers import RobertaConfig, RobertaTokenizer, RobertaModel

def init_model(model_name, tokenizer_name, pooling_type):
    config = RobertaConfig.from_pretrained(model_name)
    tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name)
    encoder = RobertaModel.from_pretrained(model_name,config=config)
    pooling = Pooling(pooling_type)

    return Model(encoder, config, tokenizer, pooling)

class Model(nn.Module):
    def __init__(self, encoder,config,tokenizer,pooling):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config=config
        self.tokenizer=tokenizer
        self.pooling = pooling
    def forward():
        x = 1