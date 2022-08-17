import os
import math
import random
import javalang
#import yaml
import ruamel.yaml as other_yaml
import shutil

import sys

from pathlib import Path

num_examples = 100

min_doc_length = 50

files_dir = "files"

class MethodData():
    def __init__(self, package, file, class_type, method_name):
        self.package = package
        self.file = file
        self.class_type = class_type
        self.method_name = method_name
    def print(self):
        print(f"{self.filepath},{self.method_name}")

def get_java_files(directory):
    java_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                if "test" in file.lower():
                    continue
                java_files.append(os.path.join(root, file))

    return java_files
    
def get_method_data_from_file(file):
    methods = []

    file_text = Path(file).read_text()

    try:
        file_parsed = javalang.parse.parse(file_text)
    except:
        return None

    try:
        class_decl = file_parsed.types[0]
        if type(class_decl) == javalang.tree.ClassDeclaration:
            class_type = "class"
            if "abstract" in class_decl.modifiers:
                class_type = "abstract"
        if type(class_decl) == javalang.tree.InterfaceDeclaration:
            class_type = "interface"
            #tbh probably dont use these
            return None
    except:
        return None
    
    try:
        decls = file_parsed.types[0].body
        random.shuffle(decls)
    except:
        return None

    for decl in decls:
        if type(decl) == javalang.tree.MethodDeclaration:
            if "test" in decl.name.lower():
                continue
            if decl.documentation is None or len(decl.documentation) < min_doc_length:
                continue 

            methods.append(MethodData(file_parsed.package.name, file, class_type, decl.name))

    return methods

def create_yaml_dictionary(methods):
    packages = []
    for method in methods:
        file = method.file.split(os.sep)[-1]
        packages.append({'package' : {'name' : method.package, 'file' : file, 'type' : method.class_type, 'methods' : [{'method' : {'name' : method.method_name, 'type' : 'none'}}]}})

    return {"packages" : packages}

def save_yaml(path, methods):
    yaml_dict = create_yaml_dictionary(methods)

    yaml = other_yaml.YAML()
    yaml.indent(sequence=6, offset=4)

    with open(path, 'w+') as file:
        file.truncate(0)
        yaml.dump(yaml_dict, file)
        #other_yaml.safe_dump(yaml_dict, file, default_flow_style=False, indent=4, block_seq_indent=True)

def save_files(methods):

    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    else:
        shutil.rmtree(files_dir)           
        os.makedirs(files_dir)

    for method in methods:
        src = method.file
        dst = os.path.join(files_dir, method.file.split(os.sep)[-1])
        os.system(f"cp {src} {dst}")

def main():
    java_files = get_java_files("projects")
    random.shuffle(java_files)

    methods = []
    for file in java_files:
        more_methods = get_method_data_from_file(file)
        if more_methods is not None:
            methods += more_methods

    random.shuffle(methods)

    methods = methods[0:num_examples]

    save_files(methods)

    save_yaml("output.yaml", methods)

if __name__ == "__main__":
    main()