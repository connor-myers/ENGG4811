import torch
import torch.nn as nn
import sys

from typing import Optional

from pooling import Pooling

from transformers import RobertaPreTrainedModel, RobertaModel

import numpy

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

    def forward(self, features, attention_mask):
        x = features[:, 0, :]  # take <s> token (equiv. to [CLS])

        # MAX POOLING
        #max_pooled = features.max(dim=1).values
        # this pooling should 100% be done by an external module before being passed onto this
        # x = features * attention_mask.unsqueeze(-1) # get rid of padding embeddings
        # max_pooled = torch.max(x, axis=1).values
        # mean_pooled = x.sum(axis=1) / attention_mask.sum(axis=-1).unsqueeze(-1) 

        # # print(features)

        # # print(features.sum(axis=1))
        # #print(features)
        # # print(max_pooled)

        # x = mean_pooled
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
    def forward(self, input_ids, config_args, attention_mask):
        outputs = self.roberta(input_ids, attention_mask=attention_mask)
        outputs_test = self.roberta(input_ids)

        sequence_output = outputs[0]

        logits = self.classifier(sequence_output, attention_mask)

        return logits

        #print(input_ids[0])
        #print(input_ids.size())

        # for token_id in input_ids[0]:
        #     output = self.roberta(token_id, attention_mask)
        #     print(token_id)

        # for idx in range(len(input_ids[0])):
        #     print(input_ids)

        # print(input_ids)
        # print(input_ids[:, 1:2])
        # print(input_ids[:, 1:2].size())
        # sys.exit(1)

        # token_embeddings = []
        # block_size = config_args.getint("eval", "block_size")
        # for idx in range(block_size):
        #     print(f"{idx} of {block_size}")
        #     ids = input_ids[:, idx:idx+1] # replace with torch.narrow
        #     attn = attention_mask[:, idx:idx+1]

        #     print(ids)
        #     print(attn)

        #     embedding = self.roberta(ids, attention_mask=attn)[0]
        #     token_embeddings.append(embedding)

        # print(token_embeddings)
        
        sys.exit(1)

class Model(nn.Module):
    def __init__(self, encoder, config, tokenizer, config_args):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config = config # roberta config information
        self.tokenizer = tokenizer
        self.config_args = config_args # config.ini file

    def forward(self, input_ids, labels):
        logits=self.encoder(input_ids, self.config_args, attention_mask=input_ids.ne(1))

        prob=torch.softmax(logits,-1)
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss(ignore_index=-1)
            loss = loss_fct(logits,labels)
            return loss,prob
        else:
            return prob