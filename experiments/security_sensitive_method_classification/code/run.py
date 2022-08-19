import torch

from model import init_model, Model

# model stuff
tokeniser_name = "microsoft/unixcoder-base"
encoder_name = "microsoft/unixcoder-base"

# classification stuff
labels = ["source", "sink", "sanitiser", "none"]

task = "train"
# task = "eval"
# task = "test"

def main():
    # try to load some kind of gpu (cuda / mps); settle on cpu
    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))

    # initialise the model
    model = init_model(encoder_name, tokeniser_name)
    model.config.num_labels = len(labels)

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