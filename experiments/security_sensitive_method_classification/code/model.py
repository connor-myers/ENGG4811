import torch
import torch.nn as nn
import sys

from pooling import Pooling

from transformers import RobertaConfig, RobertaTokenizer, RobertaModel

class ClassificationHead(nn.Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        classifier_dropout = (
            config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
        )
        self.dropout = nn.Dropout(classifier_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

    def forward(self, features, **kwargs):
        x = features[:, 0, :]  # take <s> token (equiv. to [CLS])
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x

def init_model(model_name, tokenizer_name, pooling_type):
    config = RobertaConfig.from_pretrained(model_name)
    config.num_labels = 4
    tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name)
    encoder = RobertaModel.from_pretrained(model_name,config=config)
    pooling = Pooling(pooling_type)
    

    return Model(encoder, config, tokenizer, pooling)

class Model(nn.Module):
    def __init__(self, encoder, config, tokenizer, pooling):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config=config
        self.tokenizer=tokenizer
        self.pooling = pooling
        # add dropout later
        #self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.classifier = ClassificationHead(config)

    def forward(self, input_ids, labels):
        embedding = self.encoder(input_ids, attention_mask=input_ids.ne(1))[0]
        logits = self.classifier(embedding)
        prob = torch.softmax(logits, -1)
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss(ignore_index=-1)
            print(labels.size())
            print(logits.size())
            #loss = loss_fct(logits,labels)
            loss = loss_fct(logits.view(-1, self.config.num_labels), labels.view(-1))
            return loss,prob
        else:
            return prob

        