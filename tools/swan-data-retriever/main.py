import json
import os
import javalang
import math
import random

from data_cleaner import DataCleaner

file_map = {
    'java-rt-jar-stubs-1.5.0.jar' : 'src-jdk7',
    'hibernate-core-5.2.10.Final.jar': 'hibernate-core',
    'wicket-core-7.8.0.jar': 'wicket-core',
    'apache-commons' : 'apache-commons',
    'apache-xalan' : 'apache-xalan',
    'encoder-1.2.1.jar' : 'owasp-encoder',
    'apache-xmlrpc' : 'apache-xmlrpc',
    'apache-stratos' : 'apache-stratos',
    'pebble' : 'pebble',
    'spring-web-4.3.9.RELEASE.jar' : 'spring-web',
    'esapi-2.0_rc10.jar' : 'owasp-esapi',
    'spring-context' : 'spring-context',
    'google-oauth2' : 'google-oauth2',
    'apache-shiro' : 'apache-shiro',
    'spring-jdbc' : 'spring-jdbc',
    'jsoup' : 'jsoup',
    'spring-security' : 'spring-security',
    'spring-core' : 'spring-core',
    'xmldb' : 'xmldb',
    'spring-websocket' : 'spring-websocket',
    'spring-expression' : 'spring-expression',
    'owasp-html' : 'owasp-html',
    'owasp-json' : 'owasp-json',
    'apache-axis2' : 'apache-axis2',
    'apache-commons-io' : 'apache-commons-io',
    'scribejava' : 'scribejava',
    'apache-commons-jxpath' : 'apache-commons-jxpath',
    'apache-bcel' : 'apache-bcel',
    'dmfs' : 'dmfs',
    'novell' : 'novell',
    'tomcat-5.5-servlet-api.jar' : 'tomcat55',
    'apache-xerces' : 'apache-xerces'
}

root_dir = "data"
allowed_types = ["source", "sink", "sanitizer"]
output_dir = "output"


class ExampleData():
    def __init__(self, code, javadoc):
        self.code = code
        self.javadoc = javadoc


def generate_links():
    subfolders = [ f.path for f in os.scandir(root_dir) if f.is_dir() ]
    
    for subfolder in subfolders:
        link_path = os.path.join(subfolder, "source.txt")
        if not os.path.exists(link_path):
            os._exit(1)
        with open(link_path, 'r') as link:
            link = link.read().strip()
            print(link)

def get_method_margins(method_node, parsed):
        startpos  = None
        endpos    = None
        startline = None
        endline   = None

        for path, node in parsed:
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None

        return startline, endline, startpos, endpos
def get_method_code(method_node, parsed, text_split):
    startline, endline, startpos, endpos = get_method_margins(method_node, parsed)

    if startline is None or endline is None:
        return None

    code = []
    for i in range(startline - 1, endline - 1):
        code.append(text_split[i])
    code = '\n'.join(code)

    # if class_data.class_type == ClassType.INTERFACE:
    #     return code[0:code.find(";") + 1]
    #if class_data.class_type == ClassType.ABSTRACT or class_data.class_type == ClassType.CLASS:
    return code[0:code.find("/**")]

def main():
    #generate_links()
    with open('data.json', 'r') as file:
        data = file.read().replace('\n', ' ')
    loaded_methods = json.loads(data)["methods"]

    sources = []
    sinks = []
    sanitizers = []

    for method in loaded_methods:
        types = method["type"]
        dir = file_map[method["jar"]]
        name = os.sep.join(method["name"].split(".")[:-1]) + ".java"
        path = os.path.join(root_dir, dir, name)
        if not os.path.exists(path):
            os._exit(1)

        method_name = method["name"].split('.')[-1]

        with open(path, 'r') as file:
            data = file.read()
        parsed = javalang.parse.parse(data)
        text_split = data.split("\n")

        examples_data = []

        for _, method_node in parsed.filter(javalang.tree.MethodDeclaration):
            if method_name == method_node.name:
                javadoc = method_node.documentation
                code = get_method_code(method_node, parsed, text_split)
                dc = DataCleaner()

                if code is None:
                    code = ""
                if javadoc is None:
                    javadoc = ""

                if code == "" or javadoc == "":
                    continue

                code = dc.clean_code(code)
                javadoc = dc.clean_javadoc(javadoc)

                examples_data.append(ExampleData(code, javadoc))

        for type in types:
            if type not in allowed_types:
                continue
            if type == "source":
                for example in examples_data:
                    new_example = ExampleData(example.code, example.javadoc)
                    new_example.label = 0
                    sources.append(new_example)
            if type == "sink":
                for example in examples_data:
                    new_example = ExampleData(example.code, example.javadoc)
                    new_example.label = 1
                    sinks.append(new_example)
            if type == "sanitizer":
                for example in examples_data:
                    new_example = ExampleData(example.code, example.javadoc)
                    new_example.label = 2
                    sanitizers.append(new_example)

    random.shuffle(sources)
    random.shuffle(sinks)
    random.shuffle(sanitizers)

    train = open(os.path.join(output_dir, "train.jsonl"), "w+")
    test = open(os.path.join(output_dir, "test.jsonl"), "w+")
    valid = open(os.path.join(output_dir, "eval.jsonl"), "w+")

    methods = [sources, sinks, sanitizers]
    random.shuffle(methods)

    for method_type in methods:
        num_train = math.floor(0.6 * len(method_type))
        num_test = math.floor(0.2 * len(method_type))
        num_valid = math.floor(0.2 * len(method_type))


        json_objects = []

        for method in method_type:
            json_object = {"code" : method.code, "javadoc" : method.javadoc, "label" : method.label}
            json_objects.append(json_object)

        index = 0
        for i in range(num_train):
            json.dump(json_objects[index], train)
            train.write("\n")
            index += 1

        for i in range(num_test):
            json.dump(json_objects[index], test)
            test.write("\n")
            index += 1

        for i in range(num_valid):
            json.dump(json_objects[index], valid)
            valid.write("\n")
            index += 1

    print(len(sources))
    print(len(sinks))
    print(len(sanitizers))


if __name__ == "__main__":
    main()