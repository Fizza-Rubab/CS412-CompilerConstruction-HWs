import re
from string import whitespace
keywords = ["and", "break", "continue", "else", "false", "for", "if", "mod", "not", "or", "then", "true", "void", "while"]
punctuators = ["{", "}", "(", ")", ";", "[", "]", ",", "."]
id_punctuators = punctuators.copy()
id_punctuators.extend(["'", '"'])
data_types = ["bool", "char", "int", "float"]
rel_operators = [">", "<", ">=", "<=", "==", "!="]
special_chars = list('[@!#$%^&*<>?/\|~:')
arith_operators = ["+", "-", "*", "/", "^"]
whitespaces = [" ", "\t"]
comment_starter = "/$"
comment_ender = "$/"
test_file = open('test01.tpl','r')
text_stream = test_file.read()
length = len(text_stream) 
symbol_table = {}
buffer = []
index = 0
line_no = 1
token_stream=""
id_num=1
errors = ""
end = False

def is_identifier(token_text):
    return re.match("[_a-zA-Z][_a-zA-Z0-9]{0,30}", token_text)
def is_number(token_text):
    return re.match("[-+]?\d+(\.\d+)?(E[-+]?\d+)?", token_text)
def is_arithop(token_text):
    return token_text in arith_operators
def is_relop(token_text):
    return token_text in rel_operators
def is_keyword(token_text):
    return token_text in keywords
def is_punctuator(token_text):
    return token_text in punctuators
def is_datatype(token_text):
    return token_text in data_types
def is_char_constant(token_text):
    return re.match("'[^']'", token_text)
def is_string_literal(token_text):
    return re.match('"[^"]*"', token_text)

while not end:
    # print(line_no)
    while (not end):
        if index>=length:
            end = True
            continue
        peek = text_stream[index]
        if (peek in whitespaces):
            index+=1
        elif (peek=='\n'):
            # print(line_no)
            index+=1
            line_no+=1
        else:
            break
    if end:
        break
    if peek=='+':
        token_stream+="<+>"
    elif peek=='-':
        token_stream+="<->"
    elif peek=='*':
        token_stream+="<*>"
    elif peek=='^':
        token_stream+="<^>"
    elif peek in punctuators:
        token_stream+="<%s>"%peek
    elif peek=='/':
        # print("ind %d"%index)
        if index+1<length and text_stream[index+1]=='$':
            temp_index = index+2
            while not end:
                if temp_index>=length:
                    errors+=str(line_no)+" incomplete comment\n"
                    index = temp_index
                    end = True
                    continue
                if text_stream[temp_index]=='\n':
                    # print(line_no)
                    errors+=str(line_no)+" incomplete comment\n"
                    line_no+=1
                    index=temp_index+1
                    break
                elif text_stream[temp_index]=='$' and text_stream[temp_index+1]=='/':
                    index=temp_index+1
                    break
                else:
                    temp_index+=1
        else:
            token_stream+="</>"
    elif peek=='>':
        if index+1<length and text_stream[index+1]=='=':
            token_stream+="<rel_op,>=>"
            index+=1
        else:
            token_stream+="<rel_op,>>"
    elif peek=='<':
        if index+1<length and text_stream[index+1]=='=':
            token_stream+="<rel_op,<=>"
            index+=1
        else:
            token_stream+="<rel_op,<>"
    elif peek=='=':
        if index+1<length and text_stream[index+1]=='=':
            token_stream+="<rel_op,==>"
            index+=1
        else:
            token_stream+="<=>"
    elif peek=='!':
        if index+1<length and text_stream[index+1]=='=':
            token_stream+="<rel_op,!=>"
            index+=1
        else:
            errors+="%s ! unrecognized symbol\n"%(line_no)
    elif peek=='"':
        buffer = []
        if index+1<length:
            temp_index = index+1
            while not end:
                if temp_index>=length:
                    errors+='%s " unrecognized symbol\n'%line_no
                    end = True
                elif text_stream[temp_index]=='"':
                    word = "".join(buffer)
                    if len(word)==1:
                        token_stream+="<character,%s>"%word
                    else:
                        token_stream+="<literal,%s>"%word
                    temp_index+=1
                    break
                elif text_stream[temp_index]=='\n':
                    errors+='%s " unrecognized symbol\n'%line_no
                    line_no+=1
                    break
                else:
                    buffer.append(text_stream[temp_index])
                    temp_index+=1
            index = temp_index-1
        else:
            errors+='%s " unrecognized symbol\n'%line_no
    elif peek=="'":
        buffer = []
        # print(line_no)
        if index+1<length:
            temp_index = index+1
            while not end:
                if temp_index>=length:
                    errors+="%s ' unrecognized symbol\n"%line_no
                    end = True
                elif text_stream[temp_index]=="'":
                    word = "".join(buffer)
                    if len(word)==1:
                        token_stream+="<character,%s>"%word
                    else:
                        token_stream+="<literal,%s>"%word
                    temp_index+=1
                    break
                elif text_stream[temp_index]=='\n':
                    errors+="%s ' unrecognized symbol\n"%line_no
                    break
                else:
                    buffer.append(text_stream[temp_index])
                    temp_index+=1
            index = temp_index-1
        else:
            errors+="%s ' unrecognized symbol\n"%line_no
    elif peek in special_chars:
        errors+="%s %s unrecognized symbol\n"%(line_no, peek)
    elif peek in punctuators:
        token_stream+="<%s>"%peek
    elif peek.isdigit():
        buffer = []
        temp_index = index
        new_punctuators = punctuators.copy()
        new_punctuators.remove('.')
        new_arith_ops = arith_operators.copy()
        new_arith_ops.remove('-')
        decimal  = 0
        while not end:
            if temp_index>=length:
                end=True
                continue
            if text_stream[temp_index] in new_punctuators or text_stream[temp_index] in new_arith_ops or text_stream[temp_index] in rel_operators or text_stream[temp_index] in whitespaces:
                break
            elif text_stream[temp_index]=='\n':
                line_no+=1
                break
            buffer.append(text_stream[temp_index])
            temp_index+=1
        index=temp_index-1
        num = ''.join(buffer)
        # print(num)
        if is_number(num):
            token_stream+=("<num,%s>"%num)
            symbol_table[id_num]=num
            id_num+=1
    elif peek=="_" or peek.isalpha():
        buffer = []
        temp_index = index
        while not end:
            if temp_index>=length:
                end=True
                continue
            if text_stream[temp_index] in id_punctuators or text_stream[temp_index] in arith_operators or text_stream[temp_index] in rel_operators or text_stream[temp_index] in whitespaces or text_stream[temp_index]=="=" or text_stream[temp_index] in special_chars:
                break
            elif text_stream[temp_index]=='\n':
                line_no+=1
                break
            buffer.append(text_stream[temp_index])
            temp_index+=1
        index=temp_index-1
        word = ''.join(buffer)
        # print(word)
        if is_keyword(word):
            token_stream+=("<%s>"%word)
        elif is_datatype(word):
            token_stream+=("<dt,%s>"%word)
        elif is_identifier(word):
            symbol_table[id_num]=word
            token_stream+=("<id,%s>"%id_num)
            id_num+=1         
        else:
            errors+=(str(line_no)+"%s unrecognized token\n")%word
    index+=1
    if index>=length:
        end = True
            
out_file = open("test.out", 'w')
out_file.write(token_stream)
out_file.close()
symbol_file = open("test.sym", 'a')
err_file = open("test.err", 'w')
err_file.write(errors)
err_file.close()
for i in symbol_table:
    symbol_file.write(str(i) + " " + symbol_table[i] +'\n')
symbol_file.close()


