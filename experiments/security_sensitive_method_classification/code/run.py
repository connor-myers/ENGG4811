import torch
import configparser

import sys

from model import init_model, Model

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
    model = init_model(config[model_name]['model'], config[model_name]['tokeniser'], pooling_type)

    # load gpu
    model.to(device)
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    # start doing the task
    if task == "train":
        train()
    elif task == "eval":
        eval()
    elif task == "test":
        test()
    else:
        print("bad task")

def train():
    print("we do a little training")

def eval():
    print("we do a little evaluating")

def test():
    print("we do a little testing")

if __name__ == "__main__":
    main()