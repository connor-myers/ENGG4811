from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import showinfo
from functools import partial
from process import DataProcessor
from process import allowed_types
import sys

class Gui:
    def __init__(self):
        root = Tk()
        root.geometry("750x400")
        root.title('Java Method Adder')

        # tkinter elements
        self.filename_label = None
        self.qualified_name_entry = None
        self.cwe_entry = None
        self.javadoc_text = None
        self.code_text = None

        # user input stored here
        self.filename = None
        self.name = StringVar()
        self.cwe = StringVar()
        self.type = StringVar()
        self.javadoc = None
        self.code = None

        self.root = root
        self.paddings = {'padx': 0, 'pady': 10}

        self.create_widgets()

        root.mainloop()

    def print(self):
        print("filename = %s" % self.filename)
        print("qualified_name = %s" % self.name.get())
        print("cwe = %s" % self.cwe.get())
        print("type = %s" % self.type.get())
        print("javadoc = %s" % self.javadoc)
        print("code = %s" % self.code)

    def save(self):
        # scrolled text is weird and we can't use StringVar() for it, so we save manually
        self.javadoc = self.javadoc_text.get("1.0", END)
        self.code = self.code_text.get("1.0", END)

        # hand over to process.py to process
        processor = DataProcessor(self.filename, self.name.get(), self.cwe.get(), self.type.get(), self.javadoc, self.code)
        if processor.is_input_valid():
            self.clear()
            # put data into xml file!
        else:
            # separate errors
            print("\n#############################\n", file=sys.stderr)

    def clear(self):
        # clear user input from screen
        self.filename_label.config(text="")
        self.qualified_name_entry.delete(0, 'end')
        self.cwe_entry.delete(0, 'end')
        self.type.set(allowed_types[0]) # by default set it to the first option
        self.javadoc_text.delete('1.0', END)
        self.code_text.delete('1.0', END)

        # special variable we manually must reset
        self.filename = ""

    def create_widgets(self):
        self.create_file_selection()
        self.create_name_entry()
        self.create_cwe_entry()
        self.create_type_entry()
        self.create_javadoc_entry()
        self.create_code_entry()
        self.create_submit_button()

    def create_file_selection(self):
        file_label = Label(self.root, text="File", width=20, font=("regular", 15), anchor='w')
        file_label.grid(column=0, row=0, sticky='w', **self.paddings)

        file_frame = Frame(self.root)

        file_name = Label(file_frame, font=("bold", 15), anchor='e')
        file_name.pack(side=RIGHT)

        file_button = Button(file_frame, text="Open a File", command=partial(self.select_file, file_name))
        file_button.pack(side=LEFT)

        file_frame.grid(column=1, row=0, sticky='w', **self.paddings)

        self.filename_label = file_name

    def select_file(self, label):
        filetypes = (
            ('xml files', '*.xml'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename != "":
            showinfo(title='Selected File', message=filename)
            label["text"] = filename
            self.filename = filename

    def create_name_entry(self):
        name_label = Label(self.root, text="Qualified Name", width=20, font=("bold", 15), anchor='w')
        name_label.grid(column=0, row=1, sticky='w', **self.paddings)
        name_entry = Entry(self.root, width=60, textvariable=self.name)
        name_entry.grid(column=1, row=1, sticky='w', **self.paddings)

        self.qualified_name_entry = name_entry

    def create_cwe_entry(self):
        cwe_label = Label(self.root, text="CWE (Number only)", width=20, font=("bold", 15), anchor='w')
        cwe_label.grid(column=0, row=2, sticky='w', **self.paddings)
        cwe_entry = Entry(self.root, width=20, textvariable=self.cwe)
        cwe_entry.grid(column=1, row=2, sticky='w', **self.paddings)

        self.cwe_entry = cwe_entry

    def create_type_entry(self):
        type_label = Label(self.root, text="Method Type", width=20, font=("bold", 15), anchor='w')
        type_label.grid(column=0, row=3, sticky='w', **self.paddings)
        self.type.set("Source")
        option_menu = OptionMenu(self.root, self.type, *allowed_types)
        option_menu.grid(column=1, row=3, sticky='w', **self.paddings)

    def create_javadoc_entry(self):
        javadoc_label = Label(self.root, text="Javadoc", width=20, font=("bold", 15), anchor='w')
        javadoc_label.grid(column=0, row=4, sticky='w', **self.paddings)
        javadoc_text = scrolledtext.ScrolledText(self.root, wrap=WORD, width=50, height=1, font=("Arial", 10))
        javadoc_text.grid(column=1, row=4, sticky='w', **self.paddings)

        self.javadoc_text = javadoc_text

    def create_code_entry(self):
        code_label = Label(self.root, text="Code", width=20, font=("bold", 15), anchor='w')
        code_label.grid(column=0, row=5, sticky='w', **self.paddings)
        code_text = scrolledtext.ScrolledText(self.root, wrap=WORD, width=50, height=1, font=("Arial", 10))
        code_text.grid(column=1, row=5, sticky='w', **self.paddings)

        self.code_text = code_text

    def create_submit_button(self):
        submit_button = Button(self.root, text="Submit", command=self.save)
        submit_button.grid(column=1, row=6, stick='w', **self.paddings)
