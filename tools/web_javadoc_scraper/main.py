import sys
import yaml
import requests

import xml.etree.ElementTree as xml

from bs4 import BeautifulSoup

allowed_method_types = ["sources", "sinks", "sanitisers"]

class ExtractedMethodInfo:
    def __init__(self, qualified_name, javadoc, method_type):
        self.qualified_name = qualified_name
        self.javadoc = javadoc
        self.method_type = method_type

    def print(self):
        print("qualified name = %s" % self.qualified_name)
        print("javadoc = %s" % self.javadoc)
        print("method_type = %s" % self.method_type)

class DataConfig:
    def __init__(self, packages):
        self.packages = packages

class PackageData:
    def __init__(self, name, url, methods):
        self.name = name
        self.url = url
        self.methods = methods

    def print(self):
        print("package name = %s, package url = %s" % (self.name, self.url))

        for method in self.methods:
            method.print()


class MethodData:
    def __init__(self, name, method_type):
        self.name = name
        self.method_type = method_type

    def print(self):
        print("     method name = %s, package type = %s" % (self.name, self.method_type))

class FileProcessor:
    def __init__(self, filename):
        self.filename = filename
    def load(self):
        with open(self.filename, 'r') as file:
            packages = yaml.safe_load(file)

        packages_data = []
        for package in packages["packages"]:
            package = package["package"]
            methods = []
            for method_type in allowed_method_types:
                if method_type not in package:
                    continue
                for method in package[method_type]:
                    # bit dodgy but there should only be 1 element here, so we do this to get the name
                    name = next(iter(method.values()))["name"]
                    methods.append(MethodData(name, method_type[:-1]))

            packages_data.append(PackageData(package["name"], package["url"], methods))

        return packages_data

class HtmlProcessor:
    def __init__(self, html):
        self.html_parser = BeautifulSoup(html, 'html.parser')
    def get_method_data(self, method):
        start = self.html_parser.find("a", attrs = {'name': lambda L: L and L.startswith(method.name)})
       
        # sometimes the method from dataset does not exist in java 8
        # this makes it easy to spot and remove
        try:
            pre = start.findNext("pre")
        except:
            print("Could not find method: %s" % method.name)
            sys.exit(1)

        div = pre.findNext("div")

        # java 8 javadoc format slightly changes if method is deprecated
        # still good data, though, so lets use it!
        span = div.findChildren("span", attrs = {"class" : "deprecatedLabel"})
        if len(span) != 0 and span[0] is not None:
            div = div.findNext("div")

        dl = div.findNext("dl")

        cleaned_pre = " ".join(pre.get_text().replace("\n", " ").replace("@Deprecated", "").split())
        cleaned_div = " ".join(div.get_text().replace("\n", " ").split())
        cleaned_dl = " ".join(dl.get_text().replace("\n", " ").split())

        qualified_name = cleaned_pre
        javadoc = cleaned_div + " " + cleaned_dl
        method_type = method.method_type

        return ExtractedMethodInfo(qualified_name, javadoc, method_type)

class XmlProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.tree = xml.parse(filename)
        self.root = self.tree.getroot()

    def save(self, method_info):
        # main element
        next_id = self.__get_next_method_id()
        new_method = xml.SubElement(self.root, "method", id=str(next_id))

        # sub elements
        qualified_name = xml.SubElement(new_method, "qualified-name")
        qualified_name.text = method_info.qualified_name

        method_type = xml.SubElement(new_method, "type")
        method_type.text = method_info.method_type

        javadoc = xml.SubElement(new_method, "javadoc")
        javadoc.text = method_info.javadoc

        xml.indent(self.tree, space="\t", level=0)
        self.tree.write(self.filename)

        return self.tree

    def __get_next_method_id(self):
        values = []
        for child in self.tree.iter('method'):
            values.append(int(child.attrib.get('id')))
        if len(values) == 0:
            return 1
        return max(values) + 1

def main():
    if len(sys.argv) != 3:
        print("usage: python3 main.py config.yaml data.xml")
        sys.exit(1)

    config = FileProcessor(sys.argv[1]).load()
    methods = []
    for package in config:
        html_processor = HtmlProcessor(requests.get(package.url).text)
        for method in package.methods:
            methods.append(html_processor.get_method_data(method))

    xml_processor = XmlProcessor(sys.argv[2])
    for method in methods:
        xml_processor.save(method)

if __name__ == "__main__":
    main()