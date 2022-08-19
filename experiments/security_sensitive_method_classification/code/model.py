import torch.nn as nn

from transformers import RobertaConfig, RobertaTokenizer, RobertaModel

def init_model(model_name, tokenizer_name):
    config = RobertaConfig.from_pretrained(model_name)
    tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name)
    encoder = RobertaModel.from_pretrained(model_name,config=config)

    return Model(encoder, config, tokenizer)

class Model(nn.Module):
    def __init__(self, encoder,config,tokenizer):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config=config
        self.tokenizer=tokenizer