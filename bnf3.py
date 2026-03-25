'''

BNF3: 

exp -> float id = math;
math -> multi + multi
multi -> int*multi | float

'''
Mytokens=[("keyword",
           "float"),("id","myvar"),("op","="),("int","5"),("op","*"),("float",
           "2.3"),("op","+"),("int","6"),("op","*"),("float","2.3"),("sep",";")]
inToken = ("empty","empty")

def accept_token():
    global inToken
    print("     accept token from the list:"+inToken[1])
    inToken=Mytokens.pop(0)

def multi():
    print("\n----parent node multi, finding children nodes:")
    global inToken
    if(inToken[0] == "int"):
        print("child node (internal): int")
        print("   int has child node (token):"+inToken[1])
        accept_token()

        if(inToken[1]=="*"):
            print("child node (token):"+inToken[1])
            accept_token()

            print("child node (internal): multi")
            multi()
        else:
            print("error, you need a * after the int in multi")
    elif(inToken[0] == "float"):
        print("child node (internal): float")
        print("   float has child node (token):"+inToken[1])
        accept_token()
    else:
        print("error, multi expects float or int")



def math():
    print("\n----parent node math, finding children nodes:")
    global inToken
    multi()
    if(inToken[1]=="+"):
        print("child node (token): +")
        accept_token()
    else:
        print("error, math expects multi + multi")
    
    multi()

def exp():
    print("\n----parent node exp, finding children nodes:")
    global inToken;
    typeT,token=inToken;
    if(token=="float"):
        print("child node (internal): keyword")
        print("   keyword has child node (token):"+token)
        accept_token()
    else:
        print("expect float as the first element of the expression!\n")
        return

    if(inToken[0]=="id"):
        print("child node (internal): identifier")
        print("   identifier has child node (token):"+token)
        accept_token()
    else:
        print("expect identifier as the second element of the expression!\n")
        return

    if(inToken[1]=="="):
        print("child node (token):"+inToken[1])
        accept_token()
    else:
        print("expect = as the third element of the expression!")
        return

    print("Child node (internal): math")
    math()
        
def main():
    global inToken
    inToken=Mytokens.pop(0)
    exp()
    if(inToken[1]==";"):
        print("\nparse tree building success!")

    return
main()
