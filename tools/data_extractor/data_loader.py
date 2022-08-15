import sys

class ClassData():
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.methods_data = []

    def add_method_data(self, method_data):
        self.methods_data.append(method_data)

class MethodData():
    def __init__(self, name, method_type, code, javadoc):
        self.name = name
        self.method_type = method_type
        self.code = code
        self.javadoc = javadoc

class MethodLoader():
    def __init__(self, method_info):
        self.method_info = method_info
    
    def load(self):
        return MethodData(self.method_info.name, self.method_info.method_type, "", "")

class ClassLoader():
    def __init__(self, class_info):
        self.class_info = class_info
    
    def load(self):
        class_data = ClassData(self.class_info.name, self.class_info.class_type)
        for method_info in self.class_info.methods:
            class_data.add_method_data(MethodLoader(method_info).load())
        return class_data