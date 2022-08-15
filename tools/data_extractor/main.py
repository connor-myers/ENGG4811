from config_loader import ConfigLoader
from data_loader import ClassLoader

def main():
    # load meta info
    classes_info = ConfigLoader("config.yaml").load()
    
    # load data
    classes_data = []
    for class_info in classes_info:
        classes_data.append(ClassLoader(class_info).load())

    # clean data

    # save data

if __name__ == "__main__":
    main()