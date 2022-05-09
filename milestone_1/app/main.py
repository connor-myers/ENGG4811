# simple program which uses the model trained that determines if provided doc and code are related
# for demonstration purposes
# model state is NOT uploaded to github

import torch
from model import Model
from transformers import (RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)

config = RobertaConfig.from_pretrained("microsoft/codebert-base")
config.num_labels=2 

device = "cpu"
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaForSequenceClassification.from_pretrained("microsoft/codebert-base", config=config)
model = Model(model,config,tokenizer)
model.load_state_dict(torch.load("model.bin"))

nl = input("Enter documentation: ")
code = input("Enter code: ")

nl_tokens=tokenizer.tokenize(nl)
code_tokens=tokenizer.tokenize(code)
tokens=[tokenizer.cls_token]+nl_tokens+[tokenizer.sep_token]+code_tokens+[tokenizer.sep_token]
tokens_ids=tokenizer.convert_tokens_to_ids(tokens)

context_embeddings=model(torch.tensor(tokens_ids)[None,:])[0]

values = context_embeddings.cpu().detach().numpy()

index_max = max(range(len(values)), key=values.__getitem__)

if index_max == 0:
    print("Code and Documentation are NOT related")
else:
    print("Code and Documentation ARE related")