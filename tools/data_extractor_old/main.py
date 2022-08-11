from config_loader import ConfigLoader
from file_processor import FileProcessor
from save import DataSaver
import os
import random

files_dir = "data_source"

def main():
    # get config
    data_to_load = ConfigLoader("methods.yaml").load()

    # load methods specified in config
    all_methods_data = []
    for data in data_to_load:
        data = data["package"]
        all_methods_data = all_methods_data + FileProcessor(os.path.join(files_dir, data["file"]), data["type"]).get_all_data(data)

    # save data into xml
    ds = DataSaver("data.xml")
    random.shuffle(all_methods_data)
    for methods_data in all_methods_data:
        random.shuffle(methods_data)
        for method_data in methods_data:
            ds.save(method_data)
        
if __name__ == "__main__":
    main()