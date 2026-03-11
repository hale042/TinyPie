import re
from tkinter import *

class Lexer:
        # Dictionary of the types and their regex lists 
        # order of checking is based on order of this list 
        regex_dict = {
            "Whitespace" : ["\\s"],
            "String_literal" : ["\".+\""],
            "Keyword" : ["if", "else", "int", "float"],
            "Operator" : ["\\+", "\\*", "=", ">"],
            "Separator" : [";", ":", "\"", "\\(", "\\)"],
            "Identifier" : ["[a-zA-Z]+\\d*"],
            "Float_literal" : ["\\d+\\.\\d+"],
            "Int_literal" : ["\\d+"],
        }
        
        
        # Checks regex at start of string and
        # (1) returns token        
        # (2) deletes whitespace and returns nothing
        # (3) returns string as three tokens
        # (4) returns syntax error
        def removeFirstToken(self, str_in):                        
            r = []                                          
        
            for key, val in self.regex_dict.items() :            
                for s in val :                              
                    m = re.match("^" + s, str_in[0])
                    if m :
                        if key != "Whitespace":
                            if key == "String_literal" :
                                r.append(("Separator", "\""))
                                r.append((key, str_in[0][1 : m.end() - 1]))
                                r.append(("Separator", "\""))
                            else:
                                r.append((key, str_in[0][: m.end()]))
                        str_in[0] = str_in[0][m.end() :]
                        return r
        
            r.append(("Syntax Error", str_in[0]))
            str_in[0] = ""
            return r
        
        # removes all tokens from the string and creates a list of tuples (type, token)
        # currently the removeFirstToken() function returns a syntax error as a token
        def createTokenList(self, str_in):
            l = []
            while(str_in[0] != ""):
                l = l + self.removeFirstToken(str_in)
            return l
        
        
        # takes string as arguement, creates a token list, prints it in the format
        # defined in the assignment
        # prints error message
        def printTokens(self, str_in):
            str_wrapper = [str_in]
            token_list = self.createTokenList(str_wrapper)
        
        
            #str = "Output <type, token> list: ["
            str = "["
            for element in token_list :
                if element[0] == "Syntax Error" :
                    str = "Syntax Error: Invalid Token \'" + element[1] + "\'"
                    print(str)
                    return str
                str += "<" + element[0] + "," + element[1] + ">, "
            str = str[: -2]
            str += "]"
        
            print(str)
            return str


class LexerGUI:


    def __init__(self, root):
    
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        self.label1 = Label(self.master, text="Source Code Input")
        self.label1.grid(row=0,column=0,sticky=W)

        self.label2 = Label(self.master, text="Lexical Analyzed Result")
        self.label2.grid(row=0,column=1,sticky=W)
        
        self.input_box = Text(self.master, width=40, height=8)
        self.input_box.grid(row=1, column=0)

        self.output_box = Text(self.master, width=40, height=8)
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
        self.lex = Lexer()

    def nextline (self):
        s = str(self.line_number) + ".0"
        e = str(self.line_number+1) + ".0"
        line = self.input_box.get(s, e)

        str_wrapper = [line]
        tokens = self.lex.createTokenList(str_wrapper)

        for e in tokens :
            tmp = "<" + e[0] + "," + e[1] + ">\n"
            self.output_box.insert("end", tmp)

        self.line_num.delete("1.0", "end")
        self.line_num.insert("1.0", str(self.line_number))

        self.line_number = self.line_number + 1
        

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = LexerGUI(myTkRoot)
    myTkRoot.mainloop()

