import math
import random

from config_loader import ConfigLoader
from data_loader import ClassLoader
from data_cleaner import DataCleaner
from data_saver import DataSaver
from none_loader import NoneLoader

def main():
    # load meta info
    config_loader = ConfigLoader("config.yaml")
    classes_info = config_loader.load()

    # print stats on data loader
    config_loader.print()
    
    # load data
    classes_data = []
    for class_info in classes_info:
        classes_data.append(ClassLoader(class_info).load())


    # clean and save data
    data_cleaner = DataCleaner()
    data_saver = DataSaver("data")
    for class_data in classes_data:
        for method_data in class_data.methods_data:
            clean_method_data = data_cleaner.clean_method_data(method_data)
            data_saver.save_method_data_as_xml(clean_method_data)

    num_none_examples = math.floor((data_saver.num_sources + data_saver.num_sinks + data_saver.num_sanitisers) / 3)

    # load some random none functions
    none_loader = NoneLoader("projects/")
    none_examples = none_loader.get_none_examples()
    count = 0
    for i in range(num_none_examples):
        none_example = random.choice(none_examples)
        clean_none_example = data_cleaner.clean_method_data(none_example)
        data_saver.save_method_data_as_xml(clean_none_example)

        count += 1
        if count >= num_none_examples:
            break

    # print stats
    data_saver.print()


if __name__ == "__main__":
    main()