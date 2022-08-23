import sys

import torch
import configparser
import json
import math

import numpy as np

from torch.utils.data import Dataset, SequentialSampler, DataLoader, RandomSampler
from transformers import RobertaConfig, RobertaTokenizer, AdamW, get_linear_schedule_with_warmup
from model import MyRobertaSequenceClassification, Model
from tqdm import tqdm

class TextDataset(Dataset):
    class InputFeatures(object):
        def __init__(self, input_tokens, input_ids, label):
            self.input_tokens = input_tokens
            self.input_ids = input_ids
            self.label = label

    def __init__(self, tokenizer, config, pooling_type, file_path=None):
        self.examples = []
        with open(file_path) as f:
            for line in f:
                js=json.loads(line.strip())
                self.examples.append(self.__convert_example_to_features(js,tokenizer,config, pooling_type))

    def __convert_example_to_features(self, js, tokenizer, config, pooling_type):
        # grab raw input from json
        code = ' '.join(js['code'].split())
        nl = ' '.join(js['javadoc'].split())
        label = js['label']

        # break it into tokens
        code_tokens=tokenizer.tokenize(code)
        nl_tokens=tokenizer.tokenize(nl)

        if pooling_type == "cls":
            # we will truncate if using cls pooling: @todo allow additional truncating techniques specified in the config
            partition_size =  math.floor((config.getint("DEFAULT", "block_size") - 2) / 2)
            code_tokens = code_tokens[:partition_size]
            nl_tokens = nl_tokens[:partition_size]

        # combine code and nl together
        if pooling_type == "cls":
            input_tokens = [tokenizer.cls_token] + nl_tokens + [tokenizer.sep_token] + code_tokens + [tokenizer.sep_token] # sep on end?
        if pooling_type == "mean":
            # change later
            partition_size =  math.floor((config.getint("DEFAULT", "block_size") - 2) / 2)
            code_tokens = code_tokens[:partition_size]
            nl_tokens = nl_tokens[:partition_size]
            input_tokens = nl_tokens + [tokenizer.sep_token] + code_tokens
        if pooling_type == "max":
            # change later
            input_tokens = [tokenizer.cls_token] + nl_tokens + [tokenizer.sep_token] + code_tokens + [tokenizer.sep_token]
        
        # convert tokens to respective ids (i.e. numeric representation of token)
        input_ids = tokenizer.convert_tokens_to_ids(input_tokens)

        # add padding so all blocks are same size
        padding_length = config.getint("DEFAULT", "block_size") - len(input_ids)
        input_ids += [tokenizer.pad_token_id] * padding_length 

        return self.InputFeatures(input_tokens, input_ids, label)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):       
        return torch.tensor(self.examples[i].input_ids),torch.tensor(self.examples[i].label)


def main():
    # load config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # process args
    if len(sys.argv) != 4:
        print("usage: python3 run.py model_name task pooling_type")
        sys.exit(1)
    
    model_name = sys.argv[1]
    task = sys.argv[2]
    pooling_type = sys.argv[3]

    # try to load some kind of gpu (cuda / mps); settle on cpu
    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))

    # initialise the model
    #model = init_model(config[model_name]['model'], config[model_name]['tokeniser'], pooling_type)
    model_config = RobertaConfig.from_pretrained(config.get(model_name, "model"))
    model_config.num_labels = 4
    model_tokenizer = RobertaTokenizer.from_pretrained(config.get(model_name, "tokeniser"))
    model_encoder = MyRobertaSequenceClassification.from_pretrained(config.get(model_name, "model"), config=model_config)

    model = Model(model_encoder, model_config, model_tokenizer, config)

    # load gpu
    model.to(device)
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    # start doing the task
    if task == "train":
        train_dataset = TextDataset(model.tokenizer, config, pooling_type, config.get("train", "train_data_file"))
        train(train_dataset, config, model, device)
    elif task == "eval":
        eval_dataset = TextDataset(model.tokenizer, config, pooling_type, config.get("eval", "eval_data_file"))
        eval(model, eval_dataset, config, device)
    elif task == "test":
        test()
    else:
        print("bad task")

def train(train_dataset, config, model, device):
    learning_rate = 2e-5
    adam_epsilon = 1e-8
    weight_decay = 0.0
    num_epochs = config.getint("train", "num_epochs")

    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, 
                                  batch_size=config.getint("train", "batch_size"),
                                  num_workers=4,pin_memory=True)

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate,
     eps=adam_epsilon)
    max_steps = len(train_dataloader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=max_steps*0.1,
                                                num_training_steps=max_steps)

    for idx in range(num_epochs): 
        bar = tqdm(train_dataloader,total=len(train_dataloader))
        losses=[]
        for step, batch in enumerate(bar):
            inputs = batch[0].to(device)     
            #print(inputs)
            #print(type(inputs))   
            labels=batch[1].to(device) 
            model.train()
            #print(inputs.size())
            loss,logits = model(inputs,labels)
            #loss,logits = model.forward(inputs,labels)

            if 1 > 1:
                loss = loss.mean()  # mean() to average on multi-gpu parallel training


            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            losses.append(loss.item())
            bar.set_description("epoch {} loss {}".format(idx,round(np.mean(losses),3)))
            optimizer.step()
            optimizer.zero_grad()
            scheduler.step()  
                
    model_to_save = model.module if hasattr(model,'module') else model
    output_dir = "trained.bin"            
    torch.save(model_to_save.state_dict(), output_dir)

def eval(model, eval_dataset, config, device):
    saved_model_path = config.get("DEFAULT", "saved_model_path")
    batch_size = config.getint("eval", "batch_size")

    # load previous model
    model.load_state_dict(torch.load(saved_model_path)) 
    model.to(device)

    eval_sampler = SequentialSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=batch_size,num_workers=4,pin_memory=True)

    eval_loss = 0.0
    nb_eval_steps = 0

    model.eval()

    logits = []
    labels = []
    for batch in eval_dataloader:
        inputs = batch[0].to(device)        
        label = batch[1].to(device)

        with torch.no_grad():
            lm_loss, logit = model(inputs,label)
            eval_loss += lm_loss.mean().item()
            logits.append(logit.cpu().numpy())
            labels.append(label.cpu().numpy())

        nb_eval_steps += 1

    logits=np.concatenate(logits,0)
    labels=np.concatenate(labels,0)
    preds=logits.argmax(-1)
    eval_acc=np.mean(labels==preds)
    eval_loss = eval_loss / nb_eval_steps
    perplexity = torch.tensor(eval_loss)
            
    result = {
        "eval_loss": float(perplexity),
        "eval_acc":round(eval_acc,4),
    }

    print(result)

    return result

def test():
    print("we do a little testing")

if __name__ == "__main__":
    main()