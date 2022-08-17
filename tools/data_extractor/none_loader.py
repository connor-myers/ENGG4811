import os
import random
import javalang
import sys

from pathlib import Path
from data_loader import ClassData
from data_loader import MethodData
from data_loader import MethodLoader

from config_loader import ClassType
from config_loader import MethodType
from config_loader import MethodInfo

class_files_dir = "projects"

class NoneLoader():
    def __init__(self, filepath):
        self.filepath = filepath

    def get_none_examples(self):
        files = self.__get_java_files()
        random.shuffle(files)

        none_examples = []
        for file in files:
            file_name = file.split(os.sep)[-1]

            class_data = ClassData(file_name,  file, ClassType.CLASS)
            class_data.name = f"{class_data.parsed.package.name}.{file_name}"
            for _, method_node in class_data.parsed.filter(javalang.tree.MethodDeclaration):
                method_info = MethodInfo(method_node.name, MethodType.NONE.value)
                method_data = MethodLoader(method_info, method_node).load(class_data)
                if method_data is None:
                    continue
                else:
                    none_examples.append(method_data)
                    break
        return none_examples
    
    def __get_java_files(self):
        java_files = []

        for root, dirs, files in os.walk(self.filepath):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))

        return java_files