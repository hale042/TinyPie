import re

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
def removeFirstToken(str_in):                        
    r = []                                          

    for key, val in regex_dict.items() :            
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
def createTokenList(str_in):
    l = []
    while(str_in[0] != ""):
        '''
        tmp = removeFirstToken(str_in)
        if tmp[0][0] == "Sytax Error" :
        '''

        l = l + removeFirstToken(str_in)
    return l


# takes string as arguement, creates a token list, prints it in the format
# defined in the assignment
def printTokens(str_in):
    str_wrapper = [str_in]
    token_list = createTokenList(str_wrapper)
    str = "Output <type, token> list: ["
    for element in token_list :
        str += "<" + element[0] + "," + element[1] + ">, "
    str = str[: -2]
    str += "]"

    print(str)


test_list = [   "if ( \"hello world\" ) :", 
                "if aadf342 44.44 33",
                "int A1=5",
                "float BBB2 =1034.2",
                "float cresult = A1 +BBB2 * BBB2",
                "if (cresult >10):",
                "print(\"TinyPie \" )",
             ]

for i in test_list:
    printTokens(i)

