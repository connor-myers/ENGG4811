from tkinter import *
from tkinter import scrolledtext


def main():
    root = Tk()
    root.geometry("750x400")
    root.title('Java Method Adder')

    create_widgets(root)

    root.mainloop()


def create_widgets(root):
    paddings = {'padx': 20, 'pady': 10}

    name_label = Label(root, text="Qualified Name", width=20, font=("bold", 15), anchor='w')
    name_label.grid(column=0, row=0, sticky='w', **paddings)
    name_entry = Entry(root, width=60)
    name_entry.grid(column=1, row=0, sticky='w', **paddings)

    cwe_label = Label(root, text="CWE", width=20, font=("bold", 15), anchor='w')
    cwe_label.grid(column=0, row=1, sticky='w', **paddings)
    cwe_entry = Entry(root, width=20)
    cwe_entry.grid(column=1, row=1, sticky='w', **paddings)

    type_label = Label(root, text="Method Type", width=20, font=("bold", 15), anchor='w')
    type_label.grid(column=0, row=2, sticky='w', **paddings)
    method_type = StringVar(root)
    method_type.set("Source")
    option_menu = OptionMenu(root, method_type, "Source", "Sink", "Sanitiser")
    option_menu.grid(column=1, row=2, sticky='w', **paddings)

    javadoc_label = Label(root, text="Javadoc", width=20, font=("bold", 15), anchor='w')
    javadoc_label.grid(column=0, row=3, sticky='w', **paddings)
    javadoc_text = scrolledtext.ScrolledText(root, wrap=WORD, width=50, height=1, font=("Arial", 10))
    javadoc_text.grid(column=1, row=3, sticky='w', **paddings)

    code_label = Label(root, text="Code", width=20, font=("bold", 15), anchor='w')
    code_label.grid(column=0, row=4, sticky='w', **paddings)
    code_text = scrolledtext.ScrolledText(root, wrap=WORD, width=50, height=1, font=("Arial", 10))
    code_text.grid(column=1, row=4, sticky='w', **paddings)

    submit_button = Button(root, text ="Submit")
    submit_button.grid(column=1,row=5, **paddings)

if __name__ == '__main__':
    main()
