from pathlib import Path
from enum import Enum

import javalang
import sys
import re

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
        self.javadoc_replacements = [
            ("\n", " "),
            ("\t", " "),
            ("/**", ""),
            ("*/", ""),
            ("*", "")
        ]

        self.code_replacements = [
            ("\n", " "),
            ("\t", " ")
        ]

        self.html_regex = re.compile("<.*?>")
        self.links_regex = re.compile("http\\S+")

        self.path = path
        self.contents = self.__load_file()
        self.parsed = javalang.parse.parse(self.contents)

        self.comments_regex_1 = re.compile("/\*.*?\*/", re.DOTALL)
        self.comments_regex_2 = re.compile("//.*?\n")

    def __load_file(self):
        return Path(self.path).read_text()

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
        code = "code"

        for _, method_node in self.parsed.filter(javalang.tree.MethodDeclaration):
            if method_node.name == method_info.name:
                if method_node.documentation is None:
                    continue
                javadoc = self.__clean_javadoc(method_node.documentation)

                return MethodData(javadoc, code, method_info.method_type)

    def __clean_javadoc(self, javadoc):
        clean = javadoc
        for search, replacement in self.javadoc_replacements:
            clean = clean.replace(search, replacement)

        clean = re.sub(self.html_regex, "", clean)  # remove html tags
        clean = re.sub(self.links_regex, "", clean)  # remove links
        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        return clean

    def __clean_code(self, code):
        clean = re.sub(self.comments_regex_1, "", code)
        clean = re.sub(self.comments_regex_2, "", clean)

        for search, replacement in self.code_replacements:
            clean = clean.replace(search, replacement)

        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        return clean