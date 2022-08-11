from config_loader import ConfigLoader
from file_processor import FileProcessor
import os

files_dir = "data_source"

def main():
    # get config
    data_to_load = ConfigLoader("methods.yaml").load()

    # load methods specified in config
    all_methods_data = []
    for data in data_to_load:
        data = data["package"]
        all_methods_data = all_methods_data + FileProcessor(os.path.join(files_dir, data["file"]), data["type"]).get_all_data(data)
        #print(len(FileProcessor(os.path.join(files_dir, data["file"]), data["type"]).get_all_data(data)))
    
    # count= 0
    # for thing in all_methods_data:
    #     for bruh in thing:
    #         bruh.print()
    #         count += 1

    # print(count)

        
if __name__ == "__main__":
    main()