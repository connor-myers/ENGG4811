import yaml

from config import PackageData
from config import MethodData
from config import allowed_method_types

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
                # i.e. package does not have source, sink, sanitiser...
                if method_type not in package:
                    continue
                for method in package[method_type]:
                    # there should only be 1 element here, so we do this to get the name
                    name = next(iter(method.values()))["name"]
                    methods.append(MethodData(name, method_type[:-1]))

            packages_data.append(PackageData(package["name"], package["url"], methods))

        return packages_data






