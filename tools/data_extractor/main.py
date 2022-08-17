import random
import os

from config_loader import ConfigLoader, MethodType
from data_loader import ClassLoader
from data_cleaner import DataCleaner
from data_saver import DataSaver

def main():
    # load meta info
    config_loader = ConfigLoader(os.path.join("input", "config.yaml"))
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
        # todo: make it so classes from the same package cannot appear in the same dataset (i.e. training, testing, validiation...)
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

    # print some stats
    print(f"total loaded={len(sources)+len(sinks)+len(sanitisers)+len(nones)}")
    print(f"\tnum sources={len(sources)}")
    print(f"\tnum sinks={len(sinks)}")
    print(f"\tnum sanitisers={len(sanitisers)}")
    print(f"\tnum nones={len(nones)}")

    print(f"total saved={data_saver.num_sources_saved+data_saver.num_sinks_saved+data_saver.num_sanitisers_saved+data_saver.num_nones_saved}")
    print(f"\tnum sources={data_saver.num_sources_saved}")
    print(f"\tnum sinks={data_saver.num_sinks_saved}")
    print(f"\tnum sanitisers={data_saver.num_sanitisers_saved}")
    print(f"\tnum nones={data_saver.num_nones_saved}")

if __name__ == "__main__":
    main()