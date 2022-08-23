import torch
import torch.nn as nn
import sys

from typing import Optional

from pooling import Pooling

from transformers import RobertaPreTrainedModel, RobertaModel

# not a public class so we need to copy and paste some code!
# class MyRobertaClassificationHead(nn.Module):
#     def __init__(self, config):
#         super().__init__()
#         self.dense = nn.Linear(config.hidden_size, config.hidden_size)
#         classifier_dropout = (
#             config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
#         )
#         self.dropout = nn.Dropout(classifier_dropout)
#         self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

#     def forward(self, features, **kwargs):
#         x = features[:, 0, :]  # take <s> token (equiv. to [CLS]) 3 UPDATE THIS LATER!
#         x = self.dropout(x)
#         x = self.dense(x)
#         x = torch.tanh(x)
#         x = self.dropout(x)
#         x = self.out_proj(x)
#         return x

class MyRobertaClassificationHead(nn.Module):
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

class MyRobertaSequenceClassification(RobertaPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.config = config

        self.roberta = RobertaModel(config, add_pooling_layer=False)
        self.classifier = MyRobertaClassificationHead(config)

        self.post_init()

    # we need to override forward so it doesn't do CLS pooling
    def forward(self, input_ids, attention_mask):
        # temporarily do normal 

        outputs = self.roberta(input_ids, attention_mask=attention_mask)

        sequence_output = outputs[0]

        logits = self.classifier(sequence_output)

        return logits

class Model(nn.Module):
    def __init__(self, encoder, config, tokenizer, config_args):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config = config # roberta config information
        self.tokenizer = tokenizer
        self.config_args = config_args # config.ini file

    def forward(self, input_ids, labels):
        logits=self.encoder(input_ids,attention_mask=input_ids.ne(1))

        prob=torch.softmax(logits,-1)
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss(ignore_index=-1)
            loss = loss_fct(logits,labels)
            return loss,prob
        else:
            return prob
            

# class ClassificationHead(nn.Module):
#     """Head for sentence-level classification tasks."""

#     def __init__(self, config):
#         super().__init__()
#         self.dense = nn.Linear(config.hidden_size, config.hidden_size)
#         classifier_dropout = (
#             config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
#         )
#         self.dropout = nn.Dropout(classifier_dropout)
#         self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

#     def forward(self, features, **kwargs):
#         x = features[:, 0, :]  # take <s> token (equiv. to [CLS]) # here motherfucker i knew i would find you here
#         x = self.dropout(x)
#         x = self.dense(x)
#         x = torch.tanh(x)
#         x = self.dropout(x)
#         x = self.out_proj(x)
#         return x

# def init_model(model_name, tokenizer_name, pooling_type):
#     config = RobertaConfig.from_pretrained(model_name)
#     config.num_labels = 4
#     tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name)
#     encoder = RobertaModel.from_pretrained(model_name,config=config)
#     pooling = Pooling(pooling_type)
    

#     return Model(encoder, config, tokenizer, pooling)

# class Model(nn.Module):
#     def __init__(self, encoder, config, tokenizer, pooling):
#         super(Model, self).__init__()
#         self.encoder = encoder
#         self.config=config
#         self.tokenizer=tokenizer
#         self.pooling = pooling
#         # add dropout later
#         #self.classifier = nn.Linear(config.hidden_size, config.num_labels)
#         self.classifier = ClassificationHead(config)

    # def forward(self, input_ids, labels):
    #     embedding = self.encoder(input_ids, attention_mask=input_ids.ne(1))[0]
    #     logits = self.classifier(embedding)
    #     prob = torch.softmax(logits, -1)
    #     if labels is not None:
    #         loss_fct = nn.CrossEntropyLoss(ignore_index=-1)
    #         print(labels.size())
    #         print(logits.size())
    #         #loss = loss_fct(logits,labels)
    #         loss = loss_fct(logits.view(-1, self.config.num_labels), labels.view(-1))
    #         return loss,prob
    #     else:
    #         return prob

        