from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import showinfo
from functools import partial


def select_file(label):
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != "":
        showinfo(title='Selected File', message=filename)
        label["text"] = filename


class Gui:
    def __init__(self):
        root = Tk()
        root.geometry("750x400")
        root.title('Java Method Adder')

        self.root = root
        self.paddings = {'padx': 0, 'pady': 10}

        self.create_widgets()

        root.mainloop()

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

        file_button = Button(file_frame, text="Open a File", command=partial(select_file, file_name))
        file_button.pack(side=LEFT)

        file_frame.grid(column=1, row=0, sticky='w', **self.paddings)

    def create_name_entry(self):
        name_label = Label(self.root, text="Qualified Name", width=20, font=("bold", 15), anchor='w')
        name_label.grid(column=0, row=1, sticky='w', **self.paddings)
        name_entry = Entry(self.root, width=60)
        name_entry.grid(column=1, row=1, sticky='w', **self.paddings)

    def create_cwe_entry(self):
        cwe_label = Label(self.root, text="CWE", width=20, font=("bold", 15), anchor='w')
        cwe_label.grid(column=0, row=2, sticky='w', **self.paddings)
        cwe_entry = Entry(self.root, width=20)
        cwe_entry.grid(column=1, row=2, sticky='w', **self.paddings)

    def create_type_entry(self):
        type_label = Label(self.root, text="Method Type", width=20, font=("bold", 15), anchor='w')
        type_label.grid(column=0, row=3, sticky='w', **self.paddings)
        method_type = StringVar(self.root)
        method_type.set("Source")
        option_menu = OptionMenu(self.root, method_type, "Source", "Sink", "Sanitiser")
        option_menu.grid(column=1, row=3, sticky='w', **self.paddings)

    def create_javadoc_entry(self):
        javadoc_label = Label(self.root, text="Javadoc", width=20, font=("bold", 15), anchor='w')
        javadoc_label.grid(column=0, row=4, sticky='w', **self.paddings)
        javadoc_text = scrolledtext.ScrolledText(self.root, wrap=WORD, width=50, height=1, font=("Arial", 10))
        javadoc_text.grid(column=1, row=4, sticky='w', **self.paddings)

    def create_code_entry(self):
        code_label = Label(self.root, text="Code", width=20, font=("bold", 15), anchor='w')
        code_label.grid(column=0, row=5, sticky='w', **self.paddings)
        code_text = scrolledtext.ScrolledText(self.root, wrap=WORD, width=50, height=1, font=("Arial", 10))
        code_text.grid(column=1, row=5, sticky='w', **self.paddings)

    def create_submit_button(self):
        submit_button = Button(self.root, text="Submit")
        submit_button.grid(column=1, row=6, **self.paddings)