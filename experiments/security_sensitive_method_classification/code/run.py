import sys

import torch
import configparser
import json
import math

from torch.utils.data import Dataset, SequentialSampler, DataLoader
from transformers import RobertaConfig, RobertaTokenizer, RobertaForSequenceClassification
from model import MyRobertaSequenceClassification, Model

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
            input_tokens = [tokenizer.cls_token] + nl_tokens + [tokenizer.sep_token] + code_tokens + [tokenizer.sep_token]
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
        train()
    elif task == "eval":
        eval_dataset = TextDataset(model.tokenizer, config, pooling_type, config.get("eval", "eval_data_file"))
        eval(model, eval_dataset, config, device)
    elif task == "test":
        test()
    else:
        print("bad task")

def train():
    print("we do a little training")

def eval(model, eval_dataset, config, device):
    saved_model_path = config.get("DEFAULT", "saved_model_path")
    batch_size = config.getint("eval", "batch_size")

    eval_sampler = SequentialSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=batch_size,num_workers=4,pin_memory=True)

    model.eval()

    for batch in eval_dataloader:
        inputs = batch[0].to(device)        
        label = batch[1].to(device)

        with torch.no_grad():
            lm_loss,logit = model(inputs,label)
        
        

    print("we do a little evaluating")

def test():
    print("we do a little testing")

if __name__ == "__main__":
    main()