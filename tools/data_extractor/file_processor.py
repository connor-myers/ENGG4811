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
                count += 1
                names.append(MethodInfo(none["none"]["name"], MethodTypes.NONE))

        return names

    def __get_method_data(self, method_info):
        methods_data = []
        for _, method_node in self.parsed.filter(javalang.tree.MethodDeclaration):
            if method_node.name == method_info.name:
                if method_node.documentation is None:
                    #print(method_node.name)
                    continue
                javadoc = self.__clean_javadoc(method_node.documentation)
                start, end, startpos, endpos = self.__get_start_and_end(method_node)
                if start is None or end is None:
                    #print(method_node.name)
                    continue
                code = self.__clean_code(self.__get_method_code(start, end))

                methods_data.append(MethodData(javadoc, code, method_info.method_type))
        return methods_data

    def __get_method_code(self, start, end):
        code = []
        for i in range(start - 1, end - 1):
            code.append(self.contents_split[i])
        return '\n'.join(code)


    def __get_start_and_end(self, method_node):
        startpos  = None
        endpos    = None
        startline = None
        endline   = None
        for path, node in self.parsed:
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None
        return startline, endline, startpos, endpos

    def __clean_javadoc(self, javadoc):
        clean = javadoc
        for search, replacement in self.javadoc_replacements:
            clean = clean.replace(search, replacement)

        clean = re.sub(self.html_regex, "", clean)  # remove html tags
        clean = re.sub(self.links_regex, "", clean)  # remove links
        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        return clean

    def __clean_code(self, code):
        clean = self.__remove_comments(code)

        for search, replacement in self.code_replacements:
            clean = clean.replace(search, replacement)

        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        # i want to die
        clean = " ".join(filter(lambda x:x[0]!='@', clean.split()))

        return clean

    def __remove_comments(self, string):
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
        return string