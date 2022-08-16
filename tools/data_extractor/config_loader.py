import yaml
import sys

from enum import Enum

class ClassType(Enum):
    ABSTRACT = "abstract"
    INTERFACE = "interface"
    CLASS = "class"

class ClassInfo():
    def __init__(self, name, path, class_type):
        self.name = name
        self.path = path
        self.class_type = ClassType[class_type.upper()]
        self.methods = []

    def add_method_info(self, method_info):
        self.methods.append(method_info)

class MethodType(Enum):
    SOURCE = "source"
    SANITISER = "sanitiser"
    SINK = "sink"
    NONE = "none"

class MethodInfo():
    def __init__(self, name, method_type):
        self.name = name
        self.method_type = MethodType[method_type.upper()]

class ConfigLoader():
    def __init__(self, filename):
        self.filename = filename
        self.classes_info = []

        self.num_sources = 0
        self.num_sinks = 0
        self.num_sanitisers = 0
        self.num_none = 0

    def load(self):
        with open(self.filename, 'r') as file:
            packages = yaml.safe_load(file)

        for package in packages["packages"]:
            package = package["package"]
            class_info = ClassInfo(package["name"], package["file"], package["type"])

            methods = package["methods"]
            for method in methods:
                method = method["method"]
                class_info.add_method_info(MethodInfo(method["name"], method["type"]))

                if method["type"] == "source":
                    self.num_sources += 1
                if method["type"] == "sink":
                    self.num_sinks += 1
                if method["type"] == "sanitiser":
                    self.num_sanitisers += 1
                if method["type"] == "none":
                    self.num_none += 1

            self.classes_info.append(class_info)
                
        return self.classes_info

    def print(self):
        print(f"Loaded:\n\t sources: {self.num_sources} \n\t sinks: {self.num_sinks} \n\t sanitisers: {self.num_sanitisers} \n\t none: {self.num_none}")
