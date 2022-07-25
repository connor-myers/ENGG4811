from os.path import exists
from cwe import Database
import sys
import javalang
import re

allowed_types = ["Source", "Sink", "Sanitiser"]

# arbitrary numbers
min_javadoc_length = 20
min_code_length = 20


class Input:
    def __init__(self, filename, qualified_name, cwe, type, javadoc, code):
        self.filename = filename
        self.qualified_name = qualified_name
        self.cwe = cwe
        self.type = type
        self.javadoc = javadoc
        self.code = code


class InputValidator:
    def __init__(self, user_input):
        self.input = user_input
        self.cwe_database = Database()

    def validate(self):
        valid = True
        valid = self.__validate_filename() and valid
        valid = self.__validate_qualified_name() and valid
        valid = self.__validate_cwe() and valid
        valid = self.__validate_type() and valid
        valid = self.__validate_javadoc() and valid
        valid = self.__validate_code() and valid

        sys.stderr.flush()

        return valid

    def __validate_filename(self):
        if self.input.filename == "" or self.input.filename is None:
            print("no file provided", file=sys.stderr)
            return False

        if not self.input.filename.endswith(".xml"):
            print("%s is not an xml file" % self.input.filename, file=sys.stderr)
            return False

        if not exists(self.input.filename):
            print("%s cannot be found on computer" % self.input.filename, file=sys.stderr)
            return False

        return True

    def __validate_qualified_name(self):
        if self.input.qualified_name == "" or self.input.qualified_name is None:
            print("no qualified name provided", file=sys.stderr)
            return False

        # find a way to check if string is a valid qualified name for java

        return True

    def __validate_cwe(self):
        if self.input.cwe is None or len(self.input.cwe) <= 0:
            print("no cwe provided", file=sys.stderr)
            return False
        if not self.input.cwe.isnumeric():
            print("cwe provided is not a number (only provide the number)", file=sys.stderr)
            return False
        if self.cwe_database.get(int(self.input.cwe)) is None:
            print("%s is not a valid CWE" % self.input.cwe, file=sys.stderr)
            return False

        return True

    def __validate_type(self):
        # literally impossible for user to put bad input here but may as well check
        if self.input.type not in allowed_types:
            print("%s is not a valid type" % self.input.type, file=sys.stderr)
            return False

        return True

    def __validate_javadoc(self):
        length = len(self.input.javadoc.strip())

        if length <= 0:
            print("no javadoc provided", file=sys.stderr)
            return False
        if length < min_javadoc_length:
            print("provided javadoc has a length of %d. This is too small to be useful for training." % length,
                  file=sys.stderr)
            return False

        return True

    def __validate_code(self):
        length = len(self.input.code.strip())

        if length <= 0:
            print("no code provided", file=sys.stderr)
            return False
        if length < min_code_length:
            print("provided code has a length of %d. This is too small to be useful for training." % length,
                  file=sys.stderr)
            return False

        # parsing library will only parse complete files so we put method inside a small class to make it valid
        # note: we obviously can't compile a single method, only parse it, so invalid code can technically be added
        # this is more a sanity check than anything so blatantly invalid data is not accidently added
        complete_class = "class Test {{\n {} }}".format(self.input.code)  # absolutely cursed oh my god

        try:
            javalang.parse.parse(complete_class)
        except javalang.parser.JavaSyntaxError:
            print("provided code is invalid (cannot be parsed)", file=sys.stderr)
            return False

        return True


class InputCleaner:
    def __init__(self, valid_input):
        self.input = valid_input
        self.html_regex = re.compile("<.*?>")
        self.links_regex = re.compile("http\\S+")

    def clean(self):
        self.__clean_filename()
        self.__clean_qualified_name()
        self.__clean_cwe()
        self.__clean_type()
        self.__clean_javadoc()
        self.__clean_code()
        return 1

    def __clean_filename(self):
        # might need to do something here later
        return self.input.filename

    def __clean_qualified_name(self):
        # might need to do something here later
        return self.input.qualified_name

    def __clean_cwe(self):
        # might need to do something here later
        return self.input.cwe

    def __clean_type(self):
        # might need to do something here later
        return self.input.type

    def __clean_javadoc(self):
        clean = self.input.javadoc.replace("\n", "")  # get rid of all newline characters
        clean = clean.replace("/**", "")
        clean = clean.replace("*/", "")
        clean = clean.replace("*", "")  # remove stars that create comment
        clean = clean.replace("\t", " ")  # replace tabs with a single space
        clean = re.sub(self.html_regex, "", clean)  # remove html tags
        clean = re.sub(self.links_regex, "", clean)  # remove links
        clean = re.sub(self.links_regex, "", clean)  # remove links
        clean = ' '.join(clean.split()) # cursed method of replacing multiple spaces with 1

        # remove javadoc symbols (if they are there)
        print(clean)

        return clean

    def __clean_code(self):
        return 1
