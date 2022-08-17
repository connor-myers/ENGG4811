import xml.etree.ElementTree as xml

import json
import math
import random

from config_loader import MethodType

class DataSaver:
    def __init__(self, filename):
        self.filename = filename
        self.tree = xml.parse(f"{self.filename}.xml")
        self.root = self.tree.getroot()

        self.num_sources = 0
        self.num_sinks = 0
        self.num_sanitisers = 0
        self.num_none = 0

    def save_all_as_json(self, sources, sinks, sanitisers, nones):
        train = open("train.jsonl", "w+")
        test = open("test.jsonl", "w+")
        valid = open("valid.jsonl", "w+")

        sources_json = []
        sinks_json = []
        sanitisers_json = []
        nones_json = []

        # make into json

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

    def save_method_data_as_xml(self, method_data):
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
        self.tree.write(f"{self.filename}.xml")

        # what did we actually get?
        if method_data.method_type.value == "source":
            self.num_sources += 1
        if method_data.method_type.value == "sink":
            self.num_sinks += 1
        if method_data.method_type.value == "sanitiser":
            self.num_sanitisers += 1
        if method_data.method_type.value == "none":
            self.num_none += 1

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

    def print(self):
        print(f"Saved:\n\t sources: {self.num_sources} \n\t sinks: {self.num_sinks} \n\t sanitisers: {self.num_sanitisers} \n\t none: {self.num_none}")


