from os.path import exists
from cwe import Database
import sys
import javalang

allowed_types = ["Source", "Sink", "Sanitiser"]

# arbitrary numbers
min_javadoc_length = 20
min_code_length = 20


class DataProcessor:
    def __init__(self, filename, qualified_name, cwe, type, javadoc, code):
        self.filename = filename
        self.qualified_name = qualified_name
        self.cwe = cwe
        self.type = type
        self.javadoc = javadoc
        self.code = code

        self.cwe_database = Database()

    def is_filename_valid(self):
        if self.filename == "" or self.filename is None:
            print("no file provided", file=sys.stderr)
            return False

        if not self.filename.endswith(".xml"):
            print("%s is not an xml file" % self.filename, file=sys.stderr)
            return False

        if not exists(self.filename):
            print("%s cannot be found on computer" % self.filename, file=sys.stderr)
            return False

        return True

    def is_qualified_name_valid(self):
        if self.qualified_name == "" or self.qualified_name is None:
            print("no qualified name provided", file=sys.stderr)
            return False

        # find a way to check if string is a valid qualified name for java

        return True

    def is_cwe_valid(self):
        if self.cwe is None or len(self.cwe) <= 0:
            print("no cwe provided", file=sys.stderr)
            return False
        if not self.cwe.isnumeric():
            print("cwe provided is not a number (only provide the number)", file=sys.stderr)
            return False
        if self.cwe_database.get(int(self.cwe)) is None:
            print("%s is not a valid CWE" % self.cwe, file=sys.stderr)
            return False

        return True

    def is_valid_type(self):
        # literally impossible for user to put bad input here but may as well check
        if self.type not in allowed_types:
            print("%s is not a valid type" % self.type, file=sys.stderr)
            return False

        return True

    def is_valid_javadoc(self):
        length = len(self.javadoc.strip())

        if length <= 0:
            print("no javadoc provided", file=sys.stderr)
            return False
        if length < min_javadoc_length:
            print("provided javadoc has a length of %d. This is too small to be useful for training." % length,
                  file=sys.stderr)
            return False

        return True

    def is_valid_code(self):
        length = len(self.code.strip())

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
        complete_class = "class Test {{\n {} }}".format(self.code)  # absolutely cursed oh my god

        try:
            javalang.parse.parse(complete_class)
        except javalang.parser.JavaSyntaxError:
            print("provided code is invalid (cannot be parsed)", file=sys.stderr)
            return False

        return True

    def is_input_valid(self):
        valid = True
        valid = self.is_filename_valid() and valid
        valid = self.is_qualified_name_valid() and valid
        valid = self.is_cwe_valid() and valid
        valid = self.is_valid_type() and valid
        valid = self.is_valid_javadoc() and valid
        valid = self.is_valid_code() and valid

        sys.stderr.flush()

        # if we couldn't show its invalid, its probably valid
        return valid
