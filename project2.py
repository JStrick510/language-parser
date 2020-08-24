#Jacob Strickland and Colin Morrison

#imported files to for file opening
import os.path
from os import path

output = []
tokenValue = ""
fpIndex = 0
global file

def Program():
    output.append("<Program>")
    if(stmt_list()):
        if("$$"):
            output.append("</Program>")
            return True
        else:
            return False
    else:
        return False

def stmt_list():
    output.append("<stmt_list>")
    if(stmt()):
        if(stmt_list()):
            output.append("</stmt_list>")
            return True
        else:
            return False
    elif(empty()):
        output.append("</stmt_list>")
        return True
    else:
        return False

def stmt():
    output.append("<stmt>")
    global fpIndex
    output.append("<id>")
    string = scan()
    if(string == "id"):
        output.append("</id>")
        output.append("<assign>")
        string = scan() 
        if(string == "assign"):
            output.append("</assign>")
            if(expr()):
                output.append("</stmt>")
                return True
        else:
            output.pop()
            output.pop()
            if(string is not None):
                fpIndex-=len(string)
                fpIndex-=3
            else:
                fpIndex-=1
    else:
        output.pop()
        if(string is not None):
            fpIndex-=len(string)
            fpIndex-=1
        else:
            fpIndex-=1
        output.append("<read>")
        string = scan()
        if(string == "read"):
            output.append("read")
            output.append("</read>")
            output.append("<id>")
            string = scan()
            if(string == "id"):
                output.append("</id>")
                output.append("</stmt>")
                return True
            else:
                output.pop()
                output.pop()
                if(string is not None):
                    fpIndex-=len(string)
                    fpIndex-=5
                else:
                    fpIndex-=1
        else:
            output.pop()
            if(string is not None):
                fpIndex-=len(string)
                fpIndex-=1
            else:
                fpIndex-=1
            output.append("<write>")
            string = scan()
            if(string == "write"):
                output.append("write")
                output.append("</write>")
                if(expr()):
                    output.append("</stmt>")
                    return True
            else:
                output.pop()
                if(string is not None):
                    fpIndex-=len(string)
                else:
                    fpIndex-=1

    output.pop()
    return False


def expr():
    output.append("<expr>")
    if(term()):
        if(term_tail()):
            output.append("</expr>")
            return True
        else:
            output.pop()
            return False
    elif(empty()):
        output.append("</expr>")
        return True
    else:
        output.pop()
        return False

def term_tail():
    output.append("<term_tail>")
    if(add_op()):
        if(term):
            if(term_tail()):
                output.append("</term_tail>")
                return True
            else:
                output.pop()
                return False
    elif(empty()):
        output.append("</term_tail>")
        return True
    else:
        output.pop()
        return False

def term():
    output.append("<term>")
    if(factor()):
        if(fact_tail()):
            output.append("</term>")
            return True
        else:
            output.pop()
            return False
    else:
        output.pop()
        return False

def fact_tail():
    output.append("<fact_tail>")
    if(mult_op()):
        if(factor()):
            if(fact_tail()):
                output.append("</fact_tail>")
                return True
            else:
                output.pop()
                return False
        else:
            output.pop()
            return False
    elif(empty()):
        output.append("</fact_tail>")
        return True
    else:
        output.pop()
        return False

def factor():
    output.append("<factor>")
    global fpIndex
    string = scan()
    if(string == "lparen"):
        if(expr()):
            string = scan()
            if(string == "rparen"):
                output.append("</factor>")
                return True
            else:
                fpIndex-=len(string)
                fpIndex-=1
                output.pop()
                return False
        else:
            fpIndex-=len(string)
            fpIndex-=1
            output.pop()
            return False
    else:
        if(string is not None):
            fpIndex-=len(string)
        string = scan()
        if(string == "id"):
            output.append("</factor>")
            return True
        else:
            if(string is not None):
                fpIndex-=len(string)
            else:
                fpIndex-=1
            string = scan()
            if(string == "number"):
                output.append("</factor>")
                return True

    if(string is not None):
        fpIndex-=len(string)
    else:
        fpIndex-=1
    output.pop()
    return False

def add_op():
    output.append("<add_op>")
    global fpIndex
    string = scan()
    if(string == "plus"):
        output.append("</add_op>")
        return True
    else:
        if(string is not None):
            fpIndex-=len(string)
        string = scan()
        if(string == "minus"):
            output.append("</add_op>")
            return True

    if(string is not None):
        fpIndex-=len(string)
    output.pop()
    output.pop()
    output.pop()
    return False

def mult_op():
    output.append("<mult_op>")
    global fpIndex
    string = scan()
    if(string == "times"):
        output.append("</mult_op>")
        return True
    else:
        if(string is not None):
            fpIndex-=len(string)
        else:
            fpIndex-=1
        string = scan()
        if(string == "division"):
            output.append("</mult_op>")
            return True

    if(string is not None):
        fpIndex-=len(string)
    else:
        fpIndex-=1
    output.pop()
    output.pop()
    return False

def empty():
    global fpIndex
    whitespace = ['\t','\n',' ','']
    if(fpIndex >= 0):
        file.seek(fpIndex,0)
    cur_char = file.read(1)
    if (cur_char in whitespace):
        return True
    else:
        fpIndex-=1
        return False

def scan():
    #arrays of constant values that will be used for checks
    digit = ['0','1','2','3','4','5','6','7','8','9']
    letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    whitespace = ['\t','\n',' ']
    global fpIndex
    global output
    global tokenValue
    
    state = 1       #value that keeps track of current state in DFA
    while 1:        #using a infinite loop and breaks to simulate switch statement since Python does not have switch statements
        if(fpIndex >= 0):            #to not get error at start since index is at -1
            file.seek(fpIndex,0)    #before reading from file set the pointer to where we want, used for read/write/id/number issues
        cur_char = file.read(1)     #read in one char at a time
        fpIndex+=1                  #update the file pointer when a charcter is read
        if(cur_char != whitespace and cur_char != None):
            tokenValue = tokenValue + cur_char;

        if not cur_char:            #if the file is over and DFA in a final state where something should be outputted, add that to the output
            if state == 2:
                output.append(tokenValue)
                tokenValue = ""
                return "division"
            if state == 6:
                output.append(tokenValue)
                tokenValue = ""
                return "lparen"
            if state == 7:
                output.append(tokenValue)
                tokenValue = ""
                return "rparen"
            if state == 8:
                output.append(tokenValue)
                tokenValue = ""
                return "plus"
            if state == 9:
                output.append(tokenValue)
                tokenValue = ""
                return "minus"
            if state == 10:
                output.append(tokenValue)
                tokenValue = ""
                return "times"
            if (state == 11 or state == 13):
                output.append(tokenValue)
                tokenValue = ""
                return "error"
            if state == 12:
                output.append(tokenValue)
                tokenValue = ""
                return "assign"
            if state == 14:
                output.append(tokenValue)
                tokenValue = ""
                return "number"
            if state == 15:
                output.append(tokenValue)
                tokenValue = ""
                return "number"
            if state == 16:
                output.append(tokenValue)
                tokenValue = ""
                return "id"
            break

        while 1: 
            if state == 1:
                if cur_char in whitespace:
                    state = 1
                if cur_char == '/':
                    state = 2
                if cur_char == '(':
                    state = 6
                if cur_char == ')':
                    state = 7
                if cur_char == '+':
                    state = 8
                if cur_char == '-':
                    state = 9
                if cur_char == '*':
                    state = 10
                if cur_char == ':':
                    state = 11
                if cur_char == '.':
                    state = 13
                if cur_char in digit:
                    state = 14
                if cur_char in letter:
                    #check if keyword read
                    if (cur_char == 'r'):
                        cur_char = file.read(3)
                        if(cur_char == 'ead'):
                            cur_char = file.read(1)
                            if(cur_char in whitespace or not cur_char):
                                tokenValue = ""
                                fpIndex+=4      #increase the file pointer to match the new chars read
                                return "read"
                                break

                    #check if keyword write
                    if (cur_char == 'w'):
                        cur_char = file.read(4)
                        if(cur_char == 'rite'):
                            cur_char = file.read(1)
                            if(cur_char in whitespace or not cur_char):
                                tokenValue = ""
                                fpIndex+=5      #increase the file pointer to match the new chars read
                                return "write"
                                break

                    state = 16
                break

            if state == 2:
                if cur_char == '/':
                    state = 3
                if cur_char == '*':
                    state = 4
                else:
                    state = 1
                    output.append(tokenValue)
                    tokenValue = ""
                    return "division"
                break

            if state == 3:
                if cur_char != '/n':
                    state = 3
                if cur_char == '/n':
                    state = 1
                break

            if state == 4:
                if cur_char == '*':
                    state = 5
                if cur_char != '*':
                    state = 4
                break

            if state == 5:
                if cur_char == '*':
                    state = 5
                if (cur_char != '/' or cur_char != '*'):
                    state = 4
                if cur_char == '/':
                    state = 1
                break

            if state == 6:
                output.append(tokenValue)
                tokenValue = ""
                return "lparen"
                state = 1

            if state == 7:
                output.append(tokenValue)
                tokenValue = ""
                return "rparen"
                state = 1

            if state == 8:
                output.append(tokenValue)
                tokenValue = ""
                return "plus"
                state = 1

            if state == 9:
                output.append(tokenValue)
                tokenValue = ""
                return "minus"
                state = 1

            if state == 10:
                output.append(tokenValue)
                tokenValue = ""
                return "times"
                state = 1

            if state == 11:
                if cur_char == '=':
                    state = 12
                else:
                    return "error"
                break

            if state == 12:
                output.append(tokenValue)
                tokenValue = ""
                return "assign"
                state = 1
                break

            if state == 13:
                if cur_char in digit:
                    state = 15
                else:
                    return "error"
                break

            if state == 14:
                if cur_char in digit:
                    state = 14
                elif cur_char == '.':
                    state = 15
                else:
                    output.append(tokenValue)
                    tokenValue = ""
                    return "number"
                    fpIndex-=1
                    state = 1
                break

            if state == 15:
                if cur_char in digit:
                    state = 15
                else:
                    output.append(tokenValue)
                    tokenValue = ""
                    return "number"
                    fpIndex-=1
                    state = 1
                break

            if state == 16:
                if (cur_char in letter or cur_char in digit):
                    state = 16
                else:
                    output.append(tokenValue)
                    tokenValue = ""
                    return "id"
                    fpIndex-=1
                    state = 1
                break

#def main():
while 1:                                                #infinite loop that runs until proper commandline is given
    line = input("Please enter your command: ")         #ask for user input
    if(line[0:7] != 'parser '):                        #if the first part of input is not the scanner call
        print("Invalid command, please try again")
    else:
        if(path.exists(line[7:])):                      #check the second half of the command line to see if it is a valid file
            file = open(line[7:], "r")                  #if it is a valid file, open it for reading
            break
        else:
            print("Could not open file, please try again")
            
if(Program()):
    counter = 0
    display = ""
    indentExtra = False
    error = False
    for item in output:
        if(item[0] == "<" and item[1] != "/"):
            string = "</" + item[1:]
            if(string not in output):
                error = True
    for item in output:
        if(item[0:2] != "</"):
            for indent in range(0,counter):
                display = display + "   "
                indentExtra = True
            display = display + item + "\n"
            counter+=1
        else:
            counter-=1
            if(indentExtra):
                counter-=1
                indentExtra = False
            for indent in range(0,counter):
                display = display + "   "   
            display = display + item + "\n"
    print(display)
else:
    print("error in parser")
