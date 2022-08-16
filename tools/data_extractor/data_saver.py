import xml.etree.ElementTree as xml

class DataSaver:
    def __init__(self, filename):
        self.filename = filename
        self.tree = xml.parse(f"{self.filename}.xml")
        self.root = self.tree.getroot()

        self.num_sources = 0
        self.num_sinks = 0
        self.num_sanitisers = 0
        self.num_none = 0

    def save_method_data_as_xml(self, method_data):
        # main element
        next_id = self.__get_next_method_id()
        new_method = xml.SubElement(self.root, "method", id=str(next_id))

        # sub elements
        qualified_name = xml.SubElement(new_method, "name")
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


