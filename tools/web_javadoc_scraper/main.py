import yaml
import sys
from file import FileProcessor
from web import get_javadoc_html
from html_processor import get_method_data

def main():
    if len(sys.argv) != 2:
        print("usage: python3 main.py config.yaml")
        sys.exit(1)

    # get list of packages we need to load methods for from config
    config = FileProcessor(sys.argv[1]).load()

    # load methods for each package
    for package in config:
        #print(get_javadoc_html(package.url))
        for method in package.methods:
            get_method_data(get_javadoc_html(package.url), method.name)
            print("###########################################")
        #print(package.url)
        #print(get_javadoc_html(package.url))

if __name__ == "__main__":
    main()