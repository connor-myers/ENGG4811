import re

class DataCleaner():
    def __init__(self):
        self.comments_regex_1 = re.compile("/\*.*?\*/",re.DOTALL )
        self.comments_regex_2 = re.compile("//.*?\n" )

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
        method_data.name = self.__clean_name(method_data.name)
        method_data.code = self.__clean_code(method_data.code)
        method_data.javadoc = self.__clean_javadoc(method_data.javadoc)

        return method_data

    def __clean_name(self, name):
        clean = name.replace("\n", " ")

        clean = ' '.join(clean.split())  # cursed method of replacing multiple spaces with 1

        return clean

    def __clean_code(self, code):
        clean = self.__remove_comments(code)

        for search, replacement in self.code_replacements:
            clean = clean.replace(search, replacement)

        clean = ' '.join(clean.split())

        return clean

    def __remove_comments(self, string):
        string = re.sub(self.comments_regex_1, "", string) # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(self.comments_regex_2, "", string) # remove all occurrence single-line comments (//COMMENT\n ) from string

        return string

    def __clean_javadoc(self, javadoc):
        clean = javadoc
        for search, replacement in self.javadoc_replacements:
            clean = clean.replace(search, replacement)

        clean = re.sub(self.html_regex, "", clean)
        clean = re.sub(self.links_regex, "", clean)  

        clean = ' '.join(clean.split())

        return clean