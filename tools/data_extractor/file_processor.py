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

class ClassTypes(Enum):
    CLASS = 1,
    ABSTRACT = 2,
    INTERFACE = 3

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
    def __init__(self, path, type_class):
        if type_class == "class":
            self.type_class = ClassTypes.CLASS
        if type_class == "abstract":
            self.type_class = ClassTypes.ABSTRACT
        if type_class == "interface":
            self.type_class = ClassTypes.INTERFACE 

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
        self.contents_split = self.contents.split("\n")
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
        for _, method_node in self.parsed.filter(javalang.tree.MethodDeclaration):
            if method_node.name == method_info.name:
                if method_node.documentation is None:
                    continue
                javadoc = self.__clean_javadoc(method_node.documentation)
                start, end = self.__get_start_and_end(method_node)
                print(start)
                print(end)
                code = self.__clean_code(self.__get_method_code(start, end))
                print(code)

                return MethodData(javadoc, code, method_info.method_type)

    def __get_method_code(self, start, end):
        code = []
        for i in range(start - 1, end):
            code.append(self.contents_split[i])
        return ' '.join(code)


    def __get_start_and_end(self, node):
        """Finds start and end line of a node.
        :return: start line, end line
        """
        max_line = node.position.line

        def traverse(node):
            try:
                for child in node.children:
                    if isinstance(child, list) and (len(child) > 0):
                        for item in child:
                            traverse(item)
                    else:
                        if hasattr(child, '_position'):
                            nonlocal max_line
                            if child._position.line > max_line:
                                max_line = child._position.line
                                return
            except:
                return

        traverse(node)

        if self.type_class is not ClassTypes.INTERFACE:
            return node.position.line, max_line + 1 # dont ask

        return node.position.line, max_line

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