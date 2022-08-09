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
                # trickier to get code

        return MethodData(javadoc, code, method_info.method_type)

    def __get_method_start_end(self, method_node):
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
        return startpos, endpos, startline, endline

    def __get_method_text(self, startpos, endpos, startline, endline, last_endline_index):
        if startpos is None:
            return "", None, None, None
        else:
            startline_index = startline - 1 
            endline_index = endline - 1 if endpos is not None else None 

            # 1. check for and fetch annotations
            if last_endline_index is not None:
                for line in self.contents[(last_endline_index + 1):(startline_index)]:
                    if "@" in line: 
                        startline_index = startline_index - 1
            meth_text = "<ST>".join(self.contents[startline_index:endline_index])
            meth_text = meth_text[:meth_text.rfind("}") + 1] 

            # 2. remove trailing rbrace for last methods & any external content/comments
            # if endpos is None and 
            if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
                # imbalanced braces
                brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

                for _ in range(brace_diff):
                    meth_text  = meth_text[:meth_text.rfind("}")]    
                    meth_text  = meth_text[:meth_text.rfind("}") + 1]     

            meth_lines = meth_text.split("<ST>")  
            meth_text  = "".join(meth_lines)                   
            last_endline_index = startline_index + (len(meth_lines) - 1) 

            return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index

    def __clean_javadoc(self, javadoc):
        clean = javadoc
        for search, replacement in self.javadoc_replacements:
            clean = clean.replace(search, replacement)

        clean = re.sub(self.html_regex, "", clean)  # remove html tags
        clean = re.sub(self.links_regex, "", clean)  # remove links
        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        return clean