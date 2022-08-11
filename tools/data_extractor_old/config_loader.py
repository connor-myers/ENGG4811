import yaml

class ConfigLoader():
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, 'r') as file:
            packages = yaml.safe_load(file)

        return packages["packages"]
