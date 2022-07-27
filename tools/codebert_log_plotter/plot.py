import sys
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) != 3:
        print("usage: python3 plot.py train.log examples/batch_size")
        sys.exit(1)

    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]   

    epoch_size = int(sys.argv[2])

    x_values = []
    y_values = []    

    i = 0
    for line in lines:
        if not line.startswith("epoch"):
            continue

        loss = float(line.split(" ")[3][:-1])   

        x_values.append(i)
        y_values.append(loss)

        i = i + 1

    plt.plot(x_values, y_values)
    plt.savefig('plot.png')

if __name__ == "__main__":
    main()