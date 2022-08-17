import math
import random

from config_loader import ConfigLoader, MethodType
from data_loader import ClassLoader
from data_cleaner import DataCleaner
from data_saver import DataSaver
from none_loader import NoneLoader

def main():
    # load meta info
    config_loader = ConfigLoader("config.yaml")
    classes_info = config_loader.load()

    # load data
    classes_data = []
    for class_info in classes_info:
        classes_data.append(ClassLoader(class_info).load())

    sources = []
    sinks = []
    sanitisers = []
    data_cleaner = DataCleaner()
    for class_data in classes_data:
        for method_data in class_data.methods_data:
            clean_method_data = data_cleaner.clean_method_data(method_data)
            if clean_method_data.method_type == MethodType.SOURCE:
                sources.append(clean_method_data)
            if clean_method_data.method_type == MethodType.SINK:
                sinks.append(clean_method_data)
            if clean_method_data.method_type == MethodType.SANITISER:
                sanitisers.append(clean_method_data)

    num_none_examples = math.floor((len(sources) + len(sinks) + len(sanitisers)) / 3)

    # load some random none functions
    none_loader = NoneLoader("projects/")

    nones = []
    nones_not_clean = none_loader.get_none_examples()
    count = 0
    for i in range(num_none_examples):
        none_example = random.choice(nones_not_clean)
        clean_none_example = data_cleaner.clean_method_data(none_example)
        nones.append(clean_none_example)

        count += 1
        if count >= num_none_examples:
            break

    data_saver = DataSaver("data")
    data_saver.save_all_as_json(sources, sinks, sanitisers, nones)

if __name__ == "__main__":
    main()