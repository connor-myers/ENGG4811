import math
import random
import sys

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
    nones = []
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
            if clean_method_data.method_type == MethodType.NONE:
                nones.append(clean_method_data)

    random.shuffle(sources)
    random.shuffle(sinks)
    random.shuffle(sanitisers)
    random.shuffle(nones)

    data_saver = DataSaver("output")
    data_saver.save_all_as_json(sources, sinks, sanitisers, nones)
    data_saver.save_all_as_xml("data.xml", sources, sinks, sanitisers, nones)

if __name__ == "__main__":
    main()