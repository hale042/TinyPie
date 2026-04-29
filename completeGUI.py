import re
from tkinter import *


class Lexer:
    regex_dict = {
        "Whitespace": ["\\s"],
        "String_literal": ["\".+\""],
        "Keyword": ["if", "else", "int", "float"],
        "Operator": ["\\+", "\\*", "=", ">"],
        "Separator": [";", ":", "\"", "\\(", "\\)"],
        "Identifier": ["[a-zA-Z]+\\d*"],
        "Float_literal": ["\\d+\\.\\d+"],
        "Int_literal": ["\\d+"],
    }

    def removeFirstToken(self, str_in):
        r = []
        for key, val in self.regex_dict.items():
            for s in val:
                m = re.match("^" + s, str_in[0])
                if m:
                    if key != "Whitespace":
                        if key == "String_literal":
                            r.append(("Separator", "\""))
                            r.append((key, str_in[0][1:m.end() - 1]))
                            r.append(("Separator", "\""))
                        else:
                            r.append((key, str_in[0][:m.end()]))
                    str_in[0] = str_in[0][m.end():]
                    return r
        r.append(("Syntax Error", str_in[0]))
        str_in[0] = ""
        return r

    def createTokenList(self, str_in):
        l = []
        while str_in[0] != "":
            l = l + self.removeFirstToken(str_in)
        return l


# ── Parser ────────────────────────────────────────────────────────────────────
#
# BNF rules implemented:
#   exp            -> Keyword Identifier = math ;
#   math           -> multi + multi | multi
#   multi          -> number * multi | number
#   number         -> Int_literal | Float_literal
#
#   if_exp         -> if ( comparison_exp ) :
#   comparison_exp -> Identifier > Identifier
#
#   print_exp      -> print ( " String_literal " ) ;

class Parser:

    def __init__(self):
        self.tokens   = []
        self.pos      = 0
        self.in_token = ("empty", "empty")
        self.output   = []

    def _log(self, msg):
        self.output.append(msg)

    def _accept(self):
        self._log(f"     accept token: {self.in_token[1]}")
        self.pos += 1
        self.in_token = self.tokens[self.pos] if self.pos < len(self.tokens) else ("empty", "empty")

    # ── number ----------------------------------------------------------------
    def number(self):
        self._log("\n         ----parent node: number, finding children:")
        if self.in_token[0] in ("Int_literal", "Float_literal"):
            self._log(f"         child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"         ERROR: expected a number literal, got '{self.in_token[1]}'")

    # ── multi -----------------------------------------------------------------
    def multi(self):
        self._log("\n      ----parent node: multi, finding children:")
        self._log("      child node (internal): number")
        self.number()
        if self.in_token[1] == "*":
            self._log("      child node (token): *")
            self._accept()
            self._log("      child node (internal): multi")
            self.multi()

    # ── math ------------------------------------------------------------------
    def math(self):
        self._log("\n   ----parent node: math, finding children:")
        self._log("   child node (internal): multi")
        self.multi()
        if self.in_token[1] == "+":
            self._log("   child node (token): +")
            self._accept()
            self._log("   child node (internal): multi")
            self.multi()

    # ── exp (math assignment line) -------------------------------------------
    def exp(self):
        self._log("\n----parent node: exp, finding children:")

        if self.in_token[0] == "Keyword" and self.in_token[1] in ("float", "int"):
            self._log("child node (internal): keyword")
            self._log(f"   keyword has child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"ERROR: expected 'float'/'int' keyword, got '{self.in_token[1]}'")
            return

        if self.in_token[0] == "Identifier":
            self._log("child node (internal): identifier")
            self._log(f"   identifier has child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"ERROR: expected identifier, got '{self.in_token[1]}'")
            return

        if self.in_token[1] == "=":
            self._log("child node (token): =")
            self._accept()
        else:
            self._log(f"ERROR: expected '=', got '{self.in_token[1]}'")
            return

        self._log("child node (internal): math")
        self.math()

        if self.in_token[1] == ";":
            self._log("child node (token): ;")
            self._accept()
            self._log("\n*** Parse tree building SUCCESS! ***")
        else:
            self._log(f"ERROR: expected ';', got '{self.in_token[1]}'")

    # ── comparison_exp --------------------------------------------------------
    def comparison_exp(self):
        self._log("\n   ----parent node: comparison_exp, finding children:")

        if self.in_token[0] == "Identifier":
            self._log("   child node (internal): identifier")
            self._log(f"      identifier has child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"   ERROR: expected identifier, got '{self.in_token[1]}'")
            return

        if self.in_token[1] == ">":
            self._log("   child node (token): >")
            self._accept()
        else:
            self._log(f"   ERROR: expected '>', got '{self.in_token[1]}'")
            return

        if self.in_token[0] == "Identifier":
            self._log("   child node (internal): identifier")
            self._log(f"      identifier has child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"   ERROR: expected identifier, got '{self.in_token[1]}'")

    # ── if_exp ----------------------------------------------------------------
    def if_exp(self):
        self._log("\n----parent node: if_exp, finding children:")

        if self.in_token[1] == "if":
            self._log("child node (token): if")
            self._accept()
        else:
            self._log(f"ERROR: expected 'if', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == "(":
            self._log("child node (token): (")
            self._accept()
        else:
            self._log(f"ERROR: expected '(', got '{self.in_token[1]}'")
            return

        self._log("child node (internal): comparison_exp")
        self.comparison_exp()

        if self.in_token[1] == ")":
            self._log("child node (token): )")
            self._accept()
        else:
            self._log(f"ERROR: expected ')', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == ":":
            self._log("child node (token): :")
            self._accept()
            self._log("\n*** Parse tree building SUCCESS! ***")
        else:
            self._log(f"ERROR: expected ':', got '{self.in_token[1]}'")

    # ── print_exp -------------------------------------------------------------
    def print_exp(self):
        # BNF: print_exp -> print ( " String_literal " ) ;
        self._log("\n----parent node: print_exp, finding children:")

        if self.in_token[1] == "print":
            self._log("child node (token): print")
            self._accept()
        else:
            self._log(f"ERROR: expected 'print', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == "(":
            self._log("child node (token): (")
            self._accept()
        else:
            self._log(f"ERROR: expected '(', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == '"':
            self._log('child node (token): "')
            self._accept()
        else:
            self._log(f"ERROR: expected '\"', got '{self.in_token[1]}'")
            return

        if self.in_token[0] == "String_literal":
            self._log("child node (internal): string_literal")
            self._log(f"   string_literal has child node (token): {self.in_token[1]}")
            self._accept()
        else:
            self._log(f"ERROR: expected string literal, got '{self.in_token[1]}'")
            return

        if self.in_token[1] == '"':
            self._log('child node (token): "')
            self._accept()
        else:
            self._log(f"ERROR: expected closing '\"', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == ")":
            self._log("child node (token): )")
            self._accept()
        else:
            self._log(f"ERROR: expected ')', got '{self.in_token[1]}'")
            return

        if self.in_token[1] == ";":
            self._log("child node (token): ;")
            self._accept()
            self._log("\n*** Parse tree building SUCCESS! ***")
        else:
            self._log(f"ERROR: expected ';', got '{self.in_token[1]}'")

    # ── parser entry point ---------------------------------------------------
    def parser(self, token_list, line_number):
        self.tokens   = token_list
        self.pos      = 0
        self.output   = []
        self.in_token = self.tokens[0] if self.tokens else ("empty", "empty")

        self._log(f"####Parse tree for line {line_number}####")

        first = self.in_token
        if first[0] == "Keyword" and first[1] in ("float", "int"):
            self.exp()
        elif first[1] == "if":
            self.if_exp()
        elif first[1] == "print":
            self.print_exp()
        else:
            self._log(f"ERROR: unrecognized line starting with '{first[1]}'")

        return "\n".join(self.output)


# ── GUI ───────────────────────────────────────────────────────────────────────

class LexerGUI:

    def __init__(self, root):
        self.master = root
        self.master.title("Lexer and Parser for TinyPie")

        # ── column labels
        Label(self.master, text="Source Code Input").grid(row=0, column=0, sticky=W, padx=4)
        Label(self.master, text="Token List").grid(row=0, column=1, sticky=W, padx=4)
        Label(self.master, text="Parse Tree").grid(row=0, column=2, sticky=W, padx=4)

        # ── text boxes
        self.input_box  = Text(self.master, width=38, height=10)
        self.token_box  = Text(self.master, width=32, height=10)
        self.parse_box  = Text(self.master, width=42, height=10)

        self.input_box.grid(row=1, column=0, padx=4, pady=4)
        self.token_box.grid(row=1, column=1, padx=4, pady=4)
        self.parse_box.grid(row=1, column=2, padx=4, pady=4)

        # ── current line display
        self.frame = Frame(self.master)
        self.frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=4)
        self.frame.columnconfigure(1, weight=1)

        Label(self.frame, text="Current Processing Line:").grid(row=0, column=0, sticky=W)
        self.line_num = Text(self.frame, width=4, height=1)
        self.line_num.grid(row=0, column=1, sticky=W, padx=4)

        # ── buttons
        self.next_line   = Button(self.master, text="Next Line", command=self.nextline)
        self.quit_button = Button(self.master, text="Quit",      command=root.destroy)
        self.next_line.grid(row=3,   column=0, sticky=E, padx=4, pady=4)
        self.quit_button.grid(row=3, column=2, sticky=E, padx=4, pady=4)

        self.line_number = 1
        self.lex = Lexer()
        self.par = Parser()

    def nextline(self):
        s    = str(self.line_number) + ".0"
        e    = str(self.line_number + 1) + ".0"
        line = self.input_box.get(s, e).rstrip("\n")

        if not line.strip():
            self.line_number += 1
            return

        sep = f"── Line {self.line_number} " + "─" * 20 + "\n"

        # ── Lexer
        str_wrapper = [line]
        tokens = self.lex.createTokenList(str_wrapper)

        self.token_box.insert("end", sep)
        for tok in tokens:
            self.token_box.insert("end", f"<{tok[0]}, {tok[1]}>\n")
        self.token_box.insert("end", "\n")

        # ── Parser
        parse_output = self.par.parser(tokens, self.line_number)
        self.parse_box.insert("end", sep + parse_output + "\n\n")

        # ── update line counter
        self.line_num.delete("1.0", "end")
        self.line_num.insert("1.0", str(self.line_number))

        self.line_number += 1


if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = LexerGUI(myTkRoot)
    myTkRoot.mainloop()
