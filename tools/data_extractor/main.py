from config_loader import ConfigLoader

def main():
    classes_info = ConfigLoader("config.yaml").load()

    # for class_info in classes_info:
    #     class_info.print()

if __name__ == "__main__":
    main()