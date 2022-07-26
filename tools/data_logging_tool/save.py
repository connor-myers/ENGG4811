import xml.etree.ElementTree as xml
from enum import Enum

class DataSaver:
    def __init__(self, filename):
        self.filename = filename
        self.tree = xml.parse(filename)
        self.root = self.tree.getroot()

    def update_no_save(self, clean_input):
        # main element
        next_id = self.__get_next_method_id()
        new_method = xml.SubElement(self.root, "method", id=str(next_id))

        # sub elements
        qualified_name = xml.SubElement(new_method, "qualified-name")
        qualified_name.text = clean_input.qualified_name

        cwe = xml.SubElement(new_method, "cwe")
        cwe.text = clean_input.cwe

        type = xml.SubElement(new_method, "type")
        type.text = clean_input.type

        javadoc = xml.SubElement(new_method, "javadoc")
        javadoc.text = clean_input.javadoc

        code = xml.SubElement(new_method, "code")
        code.text = clean_input.code

        # make it look pretty!
        xml.indent(self.tree, space="\t", level=0)
        self.tree.write("test.xml")

        # updated xml but not saving to disk (yet)
        return self.tree

    def __get_next_method_id(self):
        values = []
        for child in self.tree.iter('method'):
            values.append(int(child.attrib.get('id')))
        return max(values) + 1


