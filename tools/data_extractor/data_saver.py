import xml.etree.ElementTree as xml

import json
import math
import random
import os
import shutil

from config_loader import MethodType

class DataSaver:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.root = xml.Element("methods")
        self.tree = xml.ElementTree(self.root)

        # create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        else:
            shutil.rmtree(self.output_dir)
            os.makedirs(self.output_dir)

    def save_all_as_json(self, sources, sinks, sanitisers, nones):
        train = open(os.path.join(self.output_dir, "train.jsonl"), "w+")
        test = open(os.path.join(self.output_dir, "test.jsonl"), "w+")
        valid = open(os.path.join(self.output_dir, "valid.jsonl"), "w+")

        sources_json = []
        sinks_json = []
        sanitisers_json = []
        nones_json = []

        self.save_method_data(sources, train, test, valid, 0)
        self.save_method_data(sinks, train, test, valid, 1)
        self.save_method_data(sanitisers, train, test, valid, 2)
        self.save_method_data(nones, train, test, valid, 3)

        train.close()
        test.close()
        valid.close()

    def save_method_data(self, methods, train, test, valid, method_type):
        num_train = math.floor(0.6 * len(methods))
        num_test = math.floor(0.2 * len(methods))
        num_valid = math.floor(0.2 * len(methods))

        random.shuffle(methods)

        json_objects = []
        for method in methods:
            json_object = {"code" : method.code, "javadoc" : method.javadoc, "label" : method_type}
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

    def save_all_as_xml(self, filename, sources, sinks, sanitisers, nones):
        all_examples = sources + sinks + sanitisers + nones

        for example in all_examples:
            self.__save_method_data_as_xml(example)

        self.tree.write( os.path.join(self.output_dir, filename))

    def __save_method_data_as_xml(self, method_data):
        # main element
        next_id = self.__get_next_method_id()
        new_method = xml.SubElement(self.root, "method", id=str(next_id))

        # sub elements
        qualified_name = xml.SubElement(new_method, "qualified_name")
        qualified_name.text = method_data.name

        # cwe = xml.SubElement(new_method, "cwe")
        # cwe.text = clean_input.cwe

        type = xml.SubElement(new_method, "type")
        type.text = method_data.method_type.value.title()

        javadoc = xml.SubElement(new_method, "javadoc")
        javadoc.text = method_data.javadoc

        code = xml.SubElement(new_method, "code")
        code.text = method_data.code

        # make it look pretty!
        xml.indent(self.tree, space="\t", level=0)
        #self.tree.write(f"{self.filename}.xml")

        # updated xml but not saving to disk (yet)
        return self.tree

    def __get_next_method_id(self):
        values = []
        for child in self.tree.iter('method'):
            values.append(int(child.attrib.get('id')))
        # in-case of empty file
        if len(values) == 0:
            return 1    
        return max(values) + 1