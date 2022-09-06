import re

class DataCleaner():
    def __init__(self):
        self.comments_regex_1 = re.compile("/\*.*?\*/",re.DOTALL ) # to remove /*COMMENT */
        self.comments_regex_2 = re.compile("//.*?\n" ) # to remove // comment

        self.html_regex = re.compile("<.*?>")
        self.links_regex = re.compile("http\\S+")

        self.javadoc_replacements = [
            ("\n", " "),
            ("\t", " "),
            ("/**", ""),
            ("*/", ""),
            ("*", "")
        ]

        self.code_replacements = [
            ("\n", " "),
            ("\t", " ")
        ]

    def clean_method_data(self, method_data):
        method_data.qualified_name = self.__clean_name(method_data.qualified_name)
        method_data.method_name = self.__clean_name(method_data.method_name)
        method_data.code = self.__clean_code(method_data.code)
        method_data.javadoc = self.__clean_javadoc(method_data.javadoc)

        return method_data

    def __clean_name(self, name):
        clean = name.replace("\n", " ")

        clean = ' '.join(clean.split())  # replace multiple spaces with 1

        return clean

    def clean_code(self, code):
        clean = self.__remove_comments(code)

        for search, replacement in self.code_replacements:
            clean = clean.replace(search, replacement)

        clean = ' '.join(clean.split())

        return clean

    def __remove_comments(self, string):
        string = re.sub(self.comments_regex_1, "", string)
        string = re.sub(self.comments_regex_2, "", string)

        return string

    def clean_javadoc(self, javadoc):
        clean = javadoc
        for search, replacement in self.javadoc_replacements:
            clean = clean.replace(search, replacement)

        clean = re.sub(self.html_regex, "", clean)
        clean = re.sub(self.links_regex, "", clean)  

        clean = ' '.join(clean.split())

        return clean