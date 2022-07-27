from dataclasses import dataclass

allowed_method_types = ["sources", "sinks", "sanitisers"]

class DataConfig:
    """
    Stores all the information to be retrieved from all the packages' javadocs
    """

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
