import os
import javalang

from config_loader import ClassType

from pathlib import Path

input_files_dir = os.path.join("input", "input_files")

class ClassData():
    def __init__(self, name, path, class_type):
        self.name = name
        self.path = path
        self.class_type = class_type
        self.methods_data = []

        self.class_text = Path(self.path).read_text()
        self.class_text_split = self.class_text.split("\n")
        self.parsed = javalang.parse.parse(self.class_text)

    def add_method_data(self, method_data):
        self.methods_data.append(method_data)

class MethodData():
    def __init__(self, name, method_type, code, javadoc):
        self.name = name
        self.method_type = method_type
        self.code = code
        self.javadoc = javadoc

class MethodLoader():
    def __init__(self, method_info, method_node):
        self.method_info = method_info
        self.method_node = method_node
    
    def load(self, class_data):
        code = self.__get_method_code(class_data)
        javadoc = self.method_node.documentation

        if code is None or javadoc is None:
            return
            
        code = code.rstrip()

        qualified_name = f"{class_data.name}.{self.method_info.name}({self.__get_method_parameters(code)})"

        return MethodData(qualified_name, self.method_info.method_type, code, javadoc)

    def __get_method_code(self, class_data):
        startline, endline, startpos, endpos = self.__get_method_margins(class_data)

        if startline is None or endline is None:
            return None

        code = []
        for i in range(startline - 1, endline - 1):
            code.append(class_data.class_text_split[i])
        code = '\n'.join(code)

        if class_data.class_type == ClassType.INTERFACE:
            return code[0:code.find(";") + 1]
        if class_data.class_type == ClassType.ABSTRACT or class_data.class_type == ClassType.CLASS:
            return code[0:code.find("/**")]

    def __get_method_margins(self, class_data):
        startpos  = None
        endpos    = None
        startline = None
        endline   = None

        for path, node in class_data.parsed:
            if startpos is not None and self.method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == self.method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None

        return startline, endline, startpos, endpos

    def __get_method_parameters(self, code):
        return code[code.find("(") + 1:code.find(")")]        

class ClassLoader():
    def __init__(self, class_info):
        self.class_info = class_info
    
    def load(self):
        class_data = ClassData(self.class_info.name, os.path.join(input_files_dir, self.class_info.path), self.class_info.class_type)

        # O(n^2) makes me sad but because multiple methods can have same name, this is the easiest way to do this
        for method_info in self.class_info.methods:
            for _, method_node in class_data.parsed.filter(javalang.tree.MethodDeclaration):
                if method_info.name == method_node.name:
                    method_data = MethodLoader(method_info, method_node).load(class_data)
                    if method_data is None:
                        continue
                    class_data.add_method_data(method_data)
                    break # comment out if want duplicated (functions with same name but different paramters)

        return class_data