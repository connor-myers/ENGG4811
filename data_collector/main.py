from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import showinfo
from functools import partial

paddings = {'padx': 0, 'pady': 10}

def main():
    root = Tk()
    root.geometry("750x400")
    root.title('Java Method Adder')

    create_widgets(root)

    root.mainloop()

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

def create_file_selection(root):
    file_label = Label(root, text="File", width=20, font=("regular", 15), anchor='w')
    file_label.grid(column=0, row=0, sticky='w', **paddings)

    file_frame = Frame(root)

    file_name = Label(file_frame, font=("bold", 15), anchor='e')
    file_name.pack(side=RIGHT)

    file_button = Button(file_frame, text="Open a File", command=partial(select_file, file_name))
    file_button.pack(side=LEFT)

    file_frame.grid(column=1, row=0, sticky='w', **paddings)

def create_name_entry(root):
    name_label = Label(root, text="Qualified Name", width=20, font=("bold", 15), anchor='w')
    name_label.grid(column=0, row=1, sticky='w', **paddings)
    name_entry = Entry(root, width=60)
    name_entry.grid(column=1, row=1, sticky='w', **paddings)

def create_cwe_entry(root):
    cwe_label = Label(root, text="CWE", width=20, font=("bold", 15), anchor='w')
    cwe_label.grid(column=0, row=2, sticky='w', **paddings)
    cwe_entry = Entry(root, width=20)
    cwe_entry.grid(column=1, row=2, sticky='w', **paddings)

def create_type_entry(root):
    type_label = Label(root, text="Method Type", width=20, font=("bold", 15), anchor='w')
    type_label.grid(column=0, row=3, sticky='w', **paddings)
    method_type = StringVar(root)
    method_type.set("Source")
    option_menu = OptionMenu(root, method_type, "Source", "Sink", "Sanitiser")
    option_menu.grid(column=1, row=3, sticky='w', **paddings)

def create_javadoc_entry(root):
    javadoc_label = Label(root, text="Javadoc", width=20, font=("bold", 15), anchor='w')
    javadoc_label.grid(column=0, row=4, sticky='w', **paddings)
    javadoc_text = scrolledtext.ScrolledText(root, wrap=WORD, width=50, height=1, font=("Arial", 10))
    javadoc_text.grid(column=1, row=4, sticky='w', **paddings)

def create_code_entry(root):
    code_label = Label(root, text="Code", width=20, font=("bold", 15), anchor='w')
    code_label.grid(column=0, row=5, sticky='w', **paddings)
    code_text = scrolledtext.ScrolledText(root, wrap=WORD, width=50, height=1, font=("Arial", 10))
    code_text.grid(column=1, row=5, sticky='w', **paddings)

def create_submit_button(root):
    submit_button = Button(root, text="Submit")
    submit_button.grid(column=1, row=6, **paddings)

def create_widgets(root):
    create_file_selection(root)
    create_name_entry(root)
    create_cwe_entry(root)
    create_type_entry(root)
    create_javadoc_entry(root)
    create_code_entry(root)
    create_submit_button(root)

if __name__ == '__main__':
    main()
