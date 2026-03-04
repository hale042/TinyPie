
from tkinter import *

class lexerGUI: #class definition


    def __init__(self, root):
    
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        self.label1 = Label(self.master, text="Source Code Input")
        self.label1.grid(row=0,column=0,sticky=W)

        self.label2 = Label(self.master, text="Lexical Analyzed Result")
        self.label2.grid(row=0,column=1,sticky=W)
        
        self.input_box = Text(self.master, width=40, height=5)
        self.input_box.grid(row=1, column=0)

        self.output_box = Text(self.master, width=40, height=5)
        self.output_box.grid(row=1, column=1)

        self.frame = Frame(self.master)
        self.frame.grid(row=2, column=0, sticky='nsew')
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.label3 = Label(self.frame, text="Current Processing Line: ").grid(row=0, column=0, sticky=W)
        self.line_num = Text(self.frame, width=5, height=1)
        self.line_num.grid(row=0,column=0,sticky=E)

        
        self.next_line = Button (self.master, text="Next Line", command=self.nextline)
        self.next_line.grid(row=3,column=0, sticky=E)

        self.quit_button = Button (self.master, text="Quit", command=root.destroy)
        self.quit_button.grid(row=3,column=1, sticky=E)

        self.line_number = 1

    def nextline (self):
        s = str(self.line_number) + ".0"
        e = str(self.line_number+1) + ".0"
        line = self.input_box.get(s, e)
        self.output_box.insert(s, line)

        self.line_num.delete("1.0", "end")
        self.line_num.insert("1.0", str(self.line_number))

        self.line_number = self.line_number + 1
        

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = lexerGUI(myTkRoot)
    myTkRoot.mainloop()

