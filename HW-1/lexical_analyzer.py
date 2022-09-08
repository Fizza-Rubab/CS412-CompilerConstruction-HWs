import re
keywords = ["and", "break", "continue", "then", "true", "void", "while"]
punctuators = ["{", "}", "(", ")", ";", "[", "]", ",", "."]
data_types = ["bool", "char", "int", "float"]
rel_operators = [">", "<", ">=", "<=", "==", "!="]
arith_operators = ["+", "-", "*", "/", "^"]
whitespaces = [" ", "\n", "\t"]
comment_starter = "/$"
comment_ender = "$/"
test_file = open('eh.tpl','r+')
text_stream = test_file.read()
length = len(text_stream) 
symbol_table = {}
buffer = []
index = 0
line_no = 1
token_stream=""
id_num=1

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
def is_space(token_text):
    return token_text in whitespaces
def is_char_constant(token_text):
    return re.match("'[^']'", token_text)
def is_string_literal(token_text):
    return re.match('"[^"]*"', token_text)
def is_comment(token_text):
    return re.match("/\$.*?\$/", token_text)
while True:
    if index >= length-2:
        break
    curr_char = text_stream[index]
    if curr_char==" " or curr_char=="\t":
        index+=1
        continue
    elif curr_char=="\n":
        line_no+=1
    elif is_punctuator(curr_char):
        token_stream+="<%s>"%curr_char
    else:
        peek_char = text_stream[index+1]
        buffer.append(curr_char)
        if curr_char!="=" and peek_char=="=":
            word = "".join(buffer)
            buffer.clear()
            if is_identifier(word):
                symbol_table[id_num]=word
                token_stream+=("<id,%s>"%id_num)
                id_num+=1
            elif is_char_constant(word):
                token_stream+=("<character,%s>"%word[1:-1])
            elif is_string_literal(word):
                token_stream+=("<literal,%s>"%word[1:-1])
            elif is_number(word):
                token_stream+=("<num,%s>"%word)
                symbol_table[id_num]=word
                id_num+=1

        if is_space(peek_char):
            word = "".join(buffer)
            buffer.clear()
            if is_datatype(word):
                token_stream+=("<dt,%s>"%word)
            elif is_keyword(word):
                token_stream+=("<%s>"%word)
            elif is_number(word):
                token_stream+=("<num,%s>"%word)
                symbol_table[id_num]=word
                id_num+=1
            elif is_arithop(word):
                token_stream+=("<%s>"%word)
            elif is_identifier(word):
                symbol_table[id_num]=word
                token_stream+=("<id,%s>"%id_num)
                id_num+=1
            elif is_char_constant(word):
                token_stream+=("<character,%s>"%word[1:-1])
            elif is_string_literal(word):
                token_stream+=("<literal,%s>"%word[1:-1])
            elif word=="=":
                token_stream+=("<%s>"%word)
    print(index)
    index+=1
        # if peek_char in punctuators:
        #     if buffer:
        #         word = "".join(buffer)
        #         buffer.clear()
        #         if is_identifier(word):
        #             token_stream+=("<id,{id_num}>"%id_num)
        #         elif is_number(word):
        #             token_stream+=("<id,{id_num}>"%id_num)
                    

        # if (curr_char=="<" and peek_char=="=") or (curr_char==">" and peek_char=="=") or (curr_char=="=" and peek_char=="=") or (curr_char=="!" and peek_char=="="):
        #     token_stream+="<rel_op, " + curr_char+peek_char + ">"
        #     buffer.clear()
        #     index+=2
        # elif 
        # if peek_char==' ' or peek_char=='\t':
        #     word = ''.join(buffer)
        #     buffer = []
        #     if word in data_types:
        #         token_stream+="<dt, " + word + ">"
        #     elif word in keyword:
        #         token_stream+="<" + word + ">"
        #     elif word in rel_operators:
        #         token_stream+="<rel_op, " + word + ">"
        #     elif word in rel_operators:
        #         token_stream+="<rel_op, " + word + ">"
        #     elif word in arith_operators:
        #         token_stream+="<" + word + ">"
        # else:

        #     if buffer
        


            
            # process the token


out_file = open("test.out", 'w')
out_file.write(token_stream)
out_file.close()
symbol_file = open("test.sym", 'a')
for i in symbol_table:
    symbol_file.write(str(i) + " " + symbol_table[i] +'\n')
symbol_file.close()


