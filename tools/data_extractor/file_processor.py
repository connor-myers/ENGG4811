from pathlib import Path
from enum import Enum

class MethodTypes(Enum):
    SOURCE = 1
    SINK = 2
    SANITISER = 3
    NONE = 4

class MethodData():
    def __init__(self, javadoc, code, method_type):
        self.javadoc = javadoc 
        self.code = code
        self.method_type = method_type

    def print(self):
        print("javadoc=%s, code=%s, method_type=%d" % (self.javadoc, self.code, self.method_type.value))

class MethodInfo():
    def __init__(self, name, method_type):
        self.name = name
        self.method_type = method_type

class FileProcessor():
    def __init__(self, path):
        self.path = path

    def get_all_data(self, data):
        all_data = []
        methods = self.__get_all_method_info(data)
        for method in methods:
            all_data.append(self.__get_method_data(method))

        return all_data

    def __get_all_method_info(self, data):
        names = []

        # all sources
        if "sources" in data:
            for source in data["sources"]:
                names.append(MethodInfo(source["source"]["name"], MethodTypes.SOURCE))

        # all sinks
        if "sinks" in data:
            for sink in data["sinks"]:
                names.append(MethodInfo(sink["sink"]["name"], MethodTypes.SINK))

        # all sanitisers
        if "sanitisers" in data:
            for sanitiser in data["sanitisers"]:
                names.append(MethodInfo(sanitiser["sanitiser"]["name"], MethodTypes.SANITISER))

        # all nones
        if "none" in data:
            for none in data["nones"]:
                names.append(MethodInfo(none["none"]["name"], MethodTypes.NONE))

        return names


    def __get_method_data(self, method_info):
        javadoc = self.path
        code = "code"

        return MethodData(javadoc, code, method_info.method_type)

    def __load__file(self):
        self.file_contents = Path(self.path).read_text()        