import re
import os

#----------------------CLASS DEFINITION---------------
'''
Lexer Class have all the attributes and methods that lexer will need while scanning and tokenization
'''
class Lexer:
    def __init__(self):
        '''
        The method initializes Lexer and set predefined attributes according to TUPLE language specifications. It includes reserved words, operators, white spaces, punctautors, data type, special characters, alphabets, numbers and comment terminators. 
        In addition to this, symbol table, line number, lexer index, token stream, lexeam, errors, peek and stream terminator is also set to null to begin with.  
        '''
        self.keywords = ["and", "break", "continue", "else", "false", "for", "if", "mod", "not", "or", "then", "true", "void", "while"]
        self.punctuators = ["{", "}", "(", ")", ";", "[", "]", ",", "."]
        self.id_punctuators = self.punctuators.copy()
        self.id_punctuators.extend(["'", '"'])
        self.data_types = ["bool", "char", "int", "float"]
        self.rel_operators = [">", "<", ">=", "<=", "==", "!="]
        self.special_chars = list('[@!#$%^&*<>?/\|~:')
        self.arith_operators = ["+", "-", "*", "/", "^"]
        self.whitespaces = [" ", "\t"]
        self.comment_starter = "/$"
        self.comment_ender = "$/"
        self.symbol_table = {}
        self.buffer = []
        self.index = 0
        self.line_no = 1
        self.token_stream=""
        self.id_num=1
        self.errors = "<line number> <error found>\n"
        self.end = False
        self.peek=""
        self.test_file = ""
        self.test_file_name = ""
        self.text_stream = ""
        self.length = 0  
    #-------------------------------------
    #-------------------------------------
    def reset(self):
        '''
        The method resets state of lexical analyzer to intitial state that includes setting symbol table, token stream, buffer and other dependents to null
        '''
        self.symbol_table = {}
        self.buffer = []
        self.index = 0
        self.line_no = 1
        self.token_stream=""
        self.id_num=1
        self.errors = "<line number> <error found>\n"
        self.end = False
        self.peek=""
        self.test_file = ""
        self.text_stream = ""
        self.test_file_name = ""
        self.length = 0  
    #-------------------------------------
    #-------------------------------------
    def is_identifier(self,token_text):
        '''
        The method checks if token text is an identifier or not according to TUPLE specifications
        '''
        return re.match("[_a-zA-Z][_a-zA-Z0-9]{0,30}", token_text)
    def is_number(self,token_text):
        '''
        The method checks if token text is number or not according to TUPLE specifications
        '''
        token_text = token_text.strip()
        # Need to find the match of same size as the token because of the capturing group.
        for i in re.findall("-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+\-]?\d+)?", token_text):
            if len(i)==len(token_text):
                return True
        return False
    def is_arithop(self,token_text):
        '''
        The method checks if token text is an arithmetic operator or not according to TUPLE specifications
        '''
        return token_text in self.arith_operators
    def is_relop(self,token_text):        
        '''
        The method checks if token text is an relational operator or not according to TUPLE specifications
        '''
        return token_text in self.rel_operators
    def is_keyword(self,token_text):
        '''
        The method checks if token text is a keyword or not according to TUPLE specifications
        '''
        return token_text in self.keywords
    def is_punctuator(self,token_text):
        '''
        The method checks if token text is puncutuator or not according to TUPLE specifications
        '''
        return token_text in self.punctuators
    def is_datatype(self,token_text):
        '''
        The method checks if token text is data type or not according to TUPLE specifications
        '''
        return token_text in self.data_types
    def is_char_constant(self,token_text):
        '''
        The method checks if token text is character constant or not according to TUPLE specifications
        '''
        return re.match("'[^']'", token_text)
    def is_string_literal(self,token_text):
        '''
        The method checks if token text is string literal or not according to TUPLE specifications
        '''
        return re.match('"[^"]*"', token_text)
    #-------------------------------------
    #-------------------------------------
    def check_symbol_table(self, word): 
        '''
        The method checks if the word is already in symbol table or not. If it is not then only new id is assigned to it otherwise earlier is use
        '''  
        ans = False
        for i in self.symbol_table:
            if self.symbol_table[i]==word:
                ans = i
                break
        return ans
    #-------------------------------------
    #-------------------------------------
    def whitespaceAnalyze(self):
        '''
        The method checks if current word is whitespace and if it is then it gets ignored.
        '''
        while (not self.end):
            if self.index>=self.length:
                self.end = True
                continue
            self.peek = self.text_stream[self.index]
            if (self.peek in self.whitespaces):
                self.index+=1
            elif (self.peek=='\n'):
                self.index+=1
                self.line_no+=1
            else:
                break
    #-------------------------------------
    #-------------------------------------
    def commentAnalyze(self):
        '''
        The method checks if a comment is found or not and if it is then it gets ignored.
        '''
        if self.index+1<self.length and self.text_stream[self.index+1]=='$':
            temp_index = self.index+2
            while not self.end:
                if temp_index>=self.length:
                    self.errors+=str(self.line_no)+" incomplete comment\n"
                    self.index = temp_index
                    self.end = True
                    continue
                if self.text_stream[temp_index]=='\n':
                    self.errors+=str(self.line_no)+" incomplete comment\n"
                    self.line_no+=1
                    self.index=temp_index+1
                    break
                elif self.text_stream[temp_index]=='$' and self.text_stream[temp_index+1]=='/':
                    self.index=temp_index+1
                    break
                else:
                    temp_index+=1
        else:
            self.token_stream+="</>"
    #-------------------------------------
    #-------------------------------------
    def doublequoteAnalyze(self):
        self.buffer = []
        if self.index+1<self.length:
            temp_index = self.index+1
            while not self.end:
                if temp_index>=self.length:
                    halfword = "".join(self.buffer)
                    if len(halfword)<=1:
                        self.errors+='%s "%s (Invalid char constant)\n'%(self.line_no, halfword)
                    else:
                        self.errors+='%s "%s (Invalid string literal)\n'%(self.line_no, halfword)
                    self.end = True
                elif self.text_stream[temp_index]=='"':
                    word = "".join(self.buffer)
                    if len(word)==0:
                        self.token_stream+="<character,>"%word
                    if len(word)==1:
                        self.token_stream+="<character,%s>"%word
                    else:
                        self.token_stream+="<literal,%s>"%word
                    temp_index+=1
                    break
                elif self.text_stream[temp_index]=='\n':
                    halfword = "".join(self.buffer)
                    if len(halfword)<=1:
                        self.errors+='%s "%s (Invalid char constant)\n'%(self.line_no, halfword)
                    else:
                        self.errors+='%s "%s (Invalid string literal)\n'%(self.line_no, halfword)
                    break
                else:
                    self.buffer.append(self.text_stream[temp_index])
                    temp_index+=1
            self.index = temp_index-1
        else:
            self.errors+='%s " (Invalid string literal)\n'%self.line_no
    #-------------------------------------
    #-------------------------------------
    def singlequoteAnalyze(self): 
        self.buffer = []
        if self.index+1<self.length:
            temp_index = self.index+1
            while not self.end:
                if temp_index>=self.length:
                    halfword = "".join(self.buffer)
                    if len(halfword)<=1:
                        self.errors+="%s '%s (Invalid char constant)\n"%(self.line_no, halfword)
                    else:
                        self.errors+="%s '%s (Invalid string literal)\n"%(self.line_no, halfword)
                    self.end = True
                elif self.text_stream[temp_index]=="'":
                    word = "".join(self.buffer)
                    if len(word)==0:
                        self.token_stream+="<character,>"%word
                    if len(word)==1:
                        self.token_stream+="<character,%s>"%word
                    else:
                        self.token_stream+="<literal,%s>"%word
                    temp_index+=1
                    break
                elif self.text_stream[temp_index]=='\n':
                    halfword = "".join(self.buffer)
                    if len(halfword)<=1:
                        self.errors+="%s '%s (Invalid char constant)\n"%(self.line_no, halfword)
                    else:
                        self.errors+="%s '%s (Invalid string literal)\n"%(self.line_no, halfword)
                    break
                else:
                    self.buffer.append(self.text_stream[temp_index])
                    temp_index+=1
            self.index = temp_index-1
        else:
            self.errors+="%s ' (Invalid char constant)\n"%self.line_no
    #-------------------------------------
    #-------------------------------------
    def digitAnalyze(self):
        '''
        The method checks for the digits
        '''
        self.buffer = []
        temp_index = self.index
        new_punctuators = self.punctuators.copy()
        new_punctuators.remove('.')
        new_arith_ops = self.arith_operators.copy()
        new_arith_ops.remove('-')
        decimal = 0
        while not self.end:
            if temp_index>=self.length:
                self.end=True
                continue
            if self.text_stream[temp_index] in new_punctuators or self.text_stream[temp_index] in new_arith_ops or self.text_stream[temp_index] in self.rel_operators or self.text_stream[temp_index] in self.whitespaces:
                break
            elif self.text_stream[temp_index]=='\n':
                self.line_no+=1
                break
            if self.text_stream[temp_index]=='.':
                decimal+=1
            if decimal>=2:
                break
            self.buffer.append(self.text_stream[temp_index])
            temp_index+=1
        self.index=temp_index-1
        num = ''.join(self.buffer)
        if self.is_number(num):
            self.token_stream+=("<num,%s>"%num)
        else:
            self.errors+="%s (%s invalid number)\n"%(self.line_no, num)
    #-------------------------------------
    #-------------------------------------
    def alphaAnalyze(self):
        '''
        The method checks for alphabets
        '''
        self.buffer = []
        temp_index = self.index
        while not self.end:
            if temp_index>=self.length:
                self.end=True
                continue
            if self.text_stream[temp_index] in self.id_punctuators or self.text_stream[temp_index] in self.arith_operators or self.text_stream[temp_index] in self.rel_operators or self.text_stream[temp_index] in self.whitespaces or self.text_stream[temp_index]=="=" or self.text_stream[temp_index] in self.special_chars:
                break
            elif self.text_stream[temp_index]=='\n':
                self.line_no+=1
                break
            self.buffer.append(self.text_stream[temp_index])
            temp_index+=1
        self.index=temp_index-1
        word = ''.join(self.buffer)
        if self.is_keyword(word):
            self.token_stream+=("<%s>"%word)
        elif self.is_datatype(word):
            self.token_stream+=("<dt,%s>"%word)
        elif self.is_identifier(word):
            check = self.check_symbol_table(word)
            if check==False:
                self.symbol_table[self.id_num]=word
                self.token_stream+=("<id,%s>"%self.id_num)
                self.id_num+=1
            else:
                self.token_stream+=("<id,%d>"%check)
        else:
            self.errors+=(str(self.line_no)+"%s unrecognized token\n")%word
    #-------------------------------------
    #-------------------------------------
    def notAnalyze(self):
        '''
        The method checks for the not operator
        '''
        if self.index+1<self.length and self.text_stream[self.index+1]=='=':
            self.token_stream+="<rel_op,!=>"
            self.index+=1
        else:
            self.errors+="%s ! unrecognized symbol\n"%(self.line_no)
    #-------------------------------------
    #-------------------------------------
    def greatAnalyze(self):
        '''
        The method checks for greator than operator
        '''
        if self.index+1<self.length and self.text_stream[self.index+1]=='=':
            self.token_stream+="<rel_op,>=>"
            self.index+=1
        else:
            self.token_stream+="<rel_op,>>"
    #-------------------------------------
    #-------------------------------------
    def lessAnalyze(self):
        '''
        The method checks for less than operator
        '''
        if self.index+1<self.length and self.text_stream[self.index+1]=='=':
            self.token_stream+="<rel_op,<=>"
            self.index+=1
        else:
            self.token_stream+="<rel_op,<>"
    #-------------------------------------
    #-------------------------------------
    def eqAnalyze(self):
        '''
        The method checks for relation equals or assignment operators
        '''
        if self.index+1<self.length and self.text_stream[self.index+1]=='=':
            self.token_stream+="<rel_op,==>"
            self.index+=1
        else:
            self.token_stream+="<=>"
    #-------------------------------------
    #-------------------------------------
    def analyze(self):
        '''
        This method serves as a top module with all the analyze methods composed.
        '''
        while(not self.end):
            self.whitespaceAnalyze()
            if self.end:
                break 
            if self.peek=='+':
                self.token_stream+="<+>"
            elif self.peek=='-':
                self.token_stream+="<->"
            elif self.peek=='*':
                self.token_stream+="<*>"
            elif self.peek=='^':
                self.token_stream+="<^>"
            elif self.peek in self.punctuators:
                self.token_stream+="<%s>"%self.peek
            elif self.peek=='/':
                self.commentAnalyze()   
            elif self.peek=='>':
                self.greatAnalyze()
            elif self.peek=='<':
                self.lessAnalyze()
            elif self.peek=='=':
                self.eqAnalyze()
            elif self.peek=='!':
                self.notAnalyze()
            elif self.peek=='"':  
                self.doublequoteAnalyze() 
            elif self.peek=="'":
                self.singlequoteAnalyze()
            elif self.peek in self.special_chars:
                self.errors+="%s %s unrecognized symbol\n"%(self.line_no, self.peek)
            elif self.peek in self.punctuators:
                self.token_stream+="<%s>"%self.peek
            elif self.peek.isdigit():
                self.digitAnalyze()
            elif self.peek=="_" or self.peek.isalpha():
                self.alphaAnalyze()
            self.index+=1
            if self.index>=self.length:
                self.end = True
    #-------------------------------------
    #-------------------------------------
    def output(self):
        '''
        The method outputs error, sym and out files
        '''
        out_file = open("%s.out" %self.test_file_name,'w')
        out_file.write(self.token_stream)
        out_file.close()
        symbol_file = open("%s.sym" %self.test_file_name, 'a')
        for i in self.symbol_table:
            symbol_file.write(str(i) + " " + self.symbol_table[i] +'\n')
        symbol_file.close()
        err_file = open("%s.err" %self.test_file_name, 'w')
        err_file.write(self.errors)
        err_file.close()

    #-------------------------------------
    #-------------------------------------        

    def run(self,filename):
        '''
        The method serves as a lexer activator for the given filename. 
        '''
        self.reset()
        self.test_file = open(filename,'r')
        self.test_file_name = os.path.splitext(filename)[0]
        self.text_stream = self.test_file.read()
        self.length = len(self.text_stream)  
        self.analyze()
        self.output()
#-------------------------------------
#-------------------------------------



