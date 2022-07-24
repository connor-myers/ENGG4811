from tkinter import *

def main():
    root = Tk()
    root.geometry("750x750")
    root.title('Java Method Adder')

    title_label = Label(root, text="Java Method Adder", width=20, font=("bold", 20))
    title_label.pack(side=TOP)

    root.mainloop()

if __name__ == '__main__':
    main()