from config_loader import ConfigLoader
from data_loader import ClassLoader
from data_cleaner import DataCleaner
from data_saver import DataSaver

def main():
    # load meta info
    classes_info = ConfigLoader("config.yaml").load()
    
    # load data
    classes_data = []
    for class_info in classes_info:
        classes_data.append(ClassLoader(class_info).load())

    # clean and save data
    data_cleaner = DataCleaner()
    data_saver = DataSaver("data.xml")
    for class_data in classes_data:
        for method_data in class_data.methods_data:
            clean_method_data = data_cleaner.clean_method_data(method_data)
            data_saver.save_method_data(clean_method_data)

if __name__ == "__main__":
    main()