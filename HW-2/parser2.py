from lexical_analyzer2 import Lexer
import sys
import enum
import re

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#----------------------CLASS DEFINITION---------------
'''
TokenType Class holds various oken ypes that is allowed in our grammar
'''  
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	DATATYPE = 3
	# Keywords.
	IF = 101
	ELSE = 102
	FOR = 103
	WHILE = 104
	THEN = 105
	CONTINUE = 106
	BREAK = 107
	TRUE = 108
	FALSE = 109
	RETURN = 110
	# Operators.
	EQ = 201  
	PLUS = 202
	MULT = 204
	RELOP = 215
	# Punctuators.
	COMMA = 301  
	SEMICOLON = 302
	OPENBRACE = 303
	CLOSEBRACE = 304
	OPENBRAC = 305
	CLOSEBRAC = 306

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#----------------------CLASS DEFINITION---------------
'''
Token Class have all the attributes and methods that is needed for a token during our implementation of parsing
'''    
class Token:   
    def __init__(self, tokenText, tokenType, lineNo):
        self.text = tokenText
        self.type = tokenType
        self.line_no = lineNo        
    #-------------------------------------
    def __str__(self) -> str:
        return 'Line %s Token %s - %s'%(self.line_no, self.text, self.type)

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#----------------------CLASS DEFINITION---------------
'''
Parser Class have all the attributes and methods that parser will need while parsing the oken stream
'''
class Parser:
    
    def __init__(self) -> None:
        'Parser constructor to initializer lookahead (peekToken), currentoken, trace string, token stream and lexer'

        self.lexer = Lexer() 
        self.parser_errors = []
        self.token_stream = []
        self.trace=""
        self.token_index = -1
        self.curToken = None
        self.peekToken = None
    #----------------------------
    def reset_parser(self):
        'The method resets parser including lexer and its attribute, making it ready for re-use'

        self.lexer.reset()
        self.parser_errors = []
        self.token_stream = []
        self.trace=""
        self.token_index = -1
        self.curToken = None
        self.peekToken = None
     #----------------------------
    def run_parser(self,filename):
        'The method activates parser for use. It retrieves the token stream from lexer and assign token type as our parsing later will be done using these types for ease. Then it initializes the current and peek tokens to start parsing by calling the start symbol and returns the result of the parser'
        
        self.reset_parser()
        self.filename = filename
        print("\"Parsing Started for token stream of file: "+filename+"\"")
        token_stream_line, self.errors = self.lexer.run(filename)
        for i in token_stream_line:
            i_token = i[1][1:-1]
            if i_token==',':
                self.token_stream.append(Token(i_token, TokenType.COMMA, i[0]))
                continue
            comma_index = i_token.find(',')
            if comma_index==-1:
                if i_token=='while':
                    self.token_stream.append(Token(i_token, TokenType.WHILE, i[0]))
                elif i_token=='for':
                    self.token_stream.append(Token(i_token, TokenType.FOR, i[0]))
                elif i_token=='else':
                    self.token_stream.append(Token(i_token, TokenType.ELSE, i[0]))
                elif i_token=='if':
                    self.token_stream.append(Token(i_token, TokenType.IF, i[0]))
                elif i_token=='return':
                    self.token_stream.append(Token(i_token, TokenType.RETURN, i[0]))
                elif i_token=='+':
                    self.token_stream.append(Token(i_token, TokenType.PLUS, i[0]))
                elif i_token=='*':
                    self.token_stream.append(Token(i_token, TokenType.MULT, i[0]))
                elif i_token=='=':
                    self.token_stream.append(Token(i_token, TokenType.EQ, i[0]))
                elif i_token=='(':
                    self.token_stream.append(Token(i_token, TokenType.OPENBRAC, i[0]))
                elif i_token==')':
                    self.token_stream.append(Token(i_token, TokenType.CLOSEBRAC, i[0]))
                elif i_token=='{':
                    self.token_stream.append(Token(i_token, TokenType.OPENBRACE, i[0]))
                elif i_token=='}':
                    self.token_stream.append(Token(i_token, TokenType.CLOSEBRACE, i[0]))
                elif i_token==';':
                    self.token_stream.append(Token(i_token, TokenType.SEMICOLON, i[0]))
            else:
                classpart = i[1][1:-1].split(',')[0]
                i_token = i[1][1:-1].split(',')[1]
                if classpart=='dt':
                    self.token_stream.append(Token(i_token, TokenType.DATATYPE, i[0]))
                elif classpart=='id':
                    self.token_stream.append(Token(i_token, TokenType.IDENT, i[0]))
                elif classpart=='rel_op':
                    self.token_stream.append(Token(i_token, TokenType.RELOP, i[0]))
        self.token_stream.append(Token('$', TokenType.EOF, token_stream_line[-1][0]))
        self.nextToken()
        self.nextToken() # Call this twice to initialize current and peek.
        self.program() #call start symbol
        self.output() #return parser result
    #-------------------------------------
    def checkToken(self, type):
        'The method return true if the current token matches.'

        return type == self.curToken.type
    #-------------------------------------
    def checkPeek(self, type):
        'The method return true if the next token matches.'

        return type == self.peekToken.type
    #-------------------------------------
    def match(self, type):
        'The method try to match current token. If not, error. Advances the current token.'

        if not self.checkToken(type):
            errmsg="Expected " + type.name + ", got " + self.curToken.type.name + " on line " + str(self.curToken.line_no) + "\n"
            self.parser_errors+=errmsg
            self.abort(errmsg)
        self.trace+="matched <%s,%s>\n" %(self.curToken.type,self.curToken.text)
        print("matched <%s,%s>\n" %(self.curToken.type,self.curToken.text))
        self.nextToken()
    #-------------------------------------
    def nextToken(self):
        'The method advances the current token.'

        self.curToken = self.peekToken
        self.token_index += 1
        if self.token_index<len(self.token_stream):
            self.peekToken = self.token_stream[self.token_index]
    #-------------------------------------
    def abort(self, message):
        'The method for situation when syntax error has arise by adding it to the parser_error list, trace and panic mode recovery'

        print("Error. " + message + '\n')
        self.parser_errors.append("Error. " + message + '\n')
        self.trace+=("Error. " + message + '\n')
        #panic mode recovery
        print("Skipping Token") 
        self.nextToken()
        self.trace+=("Token Skipped"+ '\n')
     #-------------------------------------
    def program(self):
        'Implementation of Program non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In Program()\n"
        print("In Program()\n")
        if self.checkToken(TokenType.DATATYPE):
            self.match(TokenType.DATATYPE)
            self.match(TokenType.IDENT)
            self.match(TokenType.OPENBRAC)
            self.param_list()
            self.match(TokenType.CLOSEBRAC)
            self.match(TokenType.OPENBRACE)
            self.stmts()
            self.match(TokenType.CLOSEBRACE)
            self.match(TokenType.EOF)
        else:
            self.abort("Incorrect Program syntax")
        self.trace+="Exiting Program()\n"
    #-------------------------------------
    def param_list(self):
        'Implementation of ParamList non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In ParamList()\n"
        print("In ParamList()\n")
        if self.checkToken(TokenType.DATATYPE):
            self.match(TokenType.DATATYPE)
            self.match(TokenType.IDENT)
            self.plist()
        else:
            self.abort("Incorrect Parameter format syntax")
        self.trace+="Exiting ParamList()\n"
    #-------------------------------------
    def plist(self):
        'Implementation of PList non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In PList()\n"
        print("In PList()\n")
        if self.checkToken(TokenType.COMMA):
            self.match(TokenType.COMMA)
            self.match(TokenType.DATATYPE)
            self.match(TokenType.IDENT)
            self.plist()
        else:
            if self.checkToken(TokenType.CLOSEBRAC):
                self.trace+="Exiting Plist()\n"
                return
            else:
                self.abort("Incorrect Parameter list format syntax")
        self.trace+="Exiting Plist()\n"

    #-------------------------------------
    def stmts(self):
        'Implementation of Stmts non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In Stmts()\n"
        print("In Stmts()\n")
        print(self.curToken)
        if self.checkToken(TokenType.IF) or self.checkToken(TokenType.FOR) or self.checkToken(TokenType.RETURN) or self.checkToken(TokenType.DATATYPE) or self.checkToken(TokenType.IDENT):
            self.stmts_()
        else:
            if self.checkToken(TokenType.CLOSEBRACE):
                return
            else:
                self.abort("Incorrect Stmt")
        self.trace+="Exiting Stmt()\n"
    #-------------------------------------
    def stmts_(self):
        'Implementation of Stmts\' non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In Stmts'()\n"
        print("In Stmts'()\n")
        if self.checkToken(TokenType.DATATYPE):
            self.dec_stmts()
            self.stmts()
        elif self.checkToken(TokenType.IDENT):
            self.assign_stmt()
            self.stmts_()
        elif self.checkToken(TokenType.FOR):
            self.for_stmt()
            self.stmts_()
        elif self.checkToken(TokenType.IF):
            self.if_stmt()
            self.stmts_()
        elif self.checkToken(TokenType.RETURN):
            self.return_stmt()
            self.stmts_()
        else:
            if self.checkToken(TokenType.CLOSEBRACE):
                self.trace+="Exiting Stmts'()\n"
                return
            else:
                self.abort("Incorrect Stmt' Syntax")
        self.trace+="Exiting Stmts'()\n"
    #-------------------------------------
    def dec_stmts(self):
        'Implementation of DecStmts non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In DecStmts()\n"
        print("In DecStmts()\n")
        if self.checkToken(TokenType.DATATYPE):
            self.match(TokenType.DATATYPE)
            self.match(TokenType.IDENT)
            self.optional_assign()
            self.list()
        else:
            self.abort("Incorrect declaration syntax")
        self.trace+="Exiting DecStmts()\n"
    #-------------------------------------
    def list(self):
        'Implementation of List non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In List()\n"
        print("In List'()\n")
        if self.checkToken(TokenType.COMMA):
            self.match(TokenType.COMMA)
            self.match(TokenType.DATATYPE)
            self.optional_assign()
            self.list()
        else:
            if self.checkToken(TokenType.IF) or self.checkToken(TokenType.FOR) or self.checkToken(TokenType.RETURN) or self.checkToken(TokenType.DATATYPE) or self.checkToken(TokenType.IDENT) or self.checkToken(TokenType.CLOSEBRACE):
                self.trace+="Exiting List()\n"
                return
            else:
                self.abort("Incorrect variable list assignment")
        self.trace+="Exiting List()\n"
    #-------------------------------------
    def optional_assign(self):
        'Implementation of OptionalAssign non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In OptionalAssign'()\n"
        print("In OptionalAssign'()\n")
        if self.checkToken(TokenType.EQ):
            self.match(TokenType.EQ)
            self.expr()
            self.match(TokenType.SEMICOLON)
        else:
            if self.checkToken(TokenType.IF) or self.checkToken(TokenType.FOR) or self.checkToken(TokenType.RETURN) or self.checkToken(TokenType.DATATYPE) or self.checkToken(TokenType.IDENT) or self.checkToken(TokenType.CLOSEBRACE) or self.checkToken(TokenType.COMMA):
                self.trace+="Exiting OptionalAssign()\n"
                return
            else:
                self.abort("Incorrect optional assignment")
        self.trace+="Exiting OptionalAssign()\n"
    #-------------------------------------
    def expr(self):
        'Implementation of Expr non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In Expr()\n"
        print("In Expr()\n")
        if self.checkToken(TokenType.OPENBRAC) or self.checkToken(TokenType.IDENT):
            self.t()
            self.expr_()
        else:
            self.abort("Incorrect expression syntax")
        self.trace+="Exiting Expr()\n"
    #-------------------------------------
    def expr_(self):
        'Implementation of E\' non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In E'()\n"
        print("In E'()\n")
        if self.checkToken(TokenType.PLUS):
            self.match(TokenType.PLUS)
            self.t()
            self.expr_()
        else:
            if self.checkToken(TokenType.SEMICOLON) or self.checkToken(TokenType.RELOP) or self.checkToken(TokenType.CLOSEBRAC):
                self.trace+="Exiting E'()\n"
                return
            else:
                self.abort("Incorrect plus expression syntax")
        self.trace+="Exiting E'()\n"
    #-------------------------------------
    def t(self):
        'Implementation of T non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In T()\n"
        print("In T()\n")
        if self.checkToken(TokenType.OPENBRAC) or self.checkToken(TokenType.IDENT):
            self.f()
            self.t_()
        else:
            if self.checkToken(TokenType.SEMICOLON) or self.checkToken(TokenType.RELOP) or self.checkToken(TokenType.CLOSEBRAC) or self.checkToken(TokenType.PLUS):
                self.trace+="Exiting T()\n"
                return
            else:
                self.abort("Incorrect term expression syntax")
        self.trace+="Exiting T()\n"
    #-------------------------------------
    def t_(self):
        'Implementation of T\' non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In T'()\n"
        print("In T'()\n")
        if self.checkToken(TokenType.MULT):
            self.match(TokenType.MULT)
            self.f()
            self.t_()
        else:
            if self.checkToken(TokenType.SEMICOLON) or self.checkToken(TokenType.RELOP) or self.checkToken(TokenType.CLOSEBRAC) or self.checkToken(TokenType.PLUS):
                self.trace+="Exiting T'()\n"
                return
            else:
                self.abort("Incorrect multiplication term expression syntax")
        self.trace+="Exiting T'()\n"
    #-------------------------------------
    def f(self):
        'Implementation of F non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In F()\n"
        print("In F()\n")
        if self.checkToken(TokenType.OPENBRAC):
            self.match(TokenType.OPENBRAC)
            self.expr()
            self.match(TokenType.CLOSEBRAC)
        elif self.checkToken(TokenType.IDENT):
            self.match(TokenType.IDENT)
        else:
            self.abort("Incorrect factor syntax")
        self.trace+="Exiting F()\n"
    #-------------------------------------
    def for_stmt(self):
        'Implementation of ForStmts non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In ForStmt()\n"
        print("In ForStmt()\n")
        if self.checkToken(TokenType.FOR):
            self.match(TokenType.FOR)
            self.match(TokenType.OPENBRAC)
            self.type()
            self.match(TokenType.IDENT)
            self.expr()
            self.match(TokenType.SEMICOLON)
            self.expr()
            self.match(TokenType.RELOP)
            self.expr()
            self.match(TokenType.SEMICOLON)
            self.match(TokenType.IDENT)
            self.match(TokenType.PLUS)
            self.match(TokenType.PLUS)
            self.match(TokenType.CLOSEBRAC)
            self.match(TokenType.OPENBRACE)
            self.stmts()
            self.match(TokenType.CLOSEBRACE)
        else:
            self.abort("Incorrect for loop syntax")
        self.trace+="Exiting ForStmt()\n"
    #-------------------------------------
    def type(self):
        'Implementation of Type non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In Type()\n"
        print("In Type()\n")
        if self.checkToken(TokenType.DATATYPE):
            self.match(TokenType.DATATYPE)
        else:
            if self.checkToken(TokenType.IDENT):
                return
            else:
                self.abort("Incorrect type syntax")
        self.trace+="Exiting Type()\n"
    #-------------------------------------
    def if_stmt(self):
        'Implementation of IfStmts non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In IfStmt()\n"
        print("In IfStmt()\n")
        if self.checkToken(TokenType.IF):
            self.match(TokenType.IF)
            self.match(TokenType.OPENBRAC)
            self.expr()
            self.match(TokenType.RELOP)
            self.expr()
            self.match(TokenType.CLOSEBRAC)
            self.match(TokenType.OPENBRACE)
            self.stmts()
            self.match(TokenType.CLOSEBRACE)
            self.optional_else()
        else:
            self.abort("Incorrect if statement syntax")
        self.trace+="Exiting IfStmt()\n"
    #-------------------------------------
    def assign_stmt(self):
        'Implementation of AssignStmts non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In AssignStmt()\n"
        print("In AssignStmt()\n")
        if self.checkToken(TokenType.IDENT):
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expr()
            self.match(TokenType.SEMICOLON)
        else:
            self.abort("Incorrect assignment statement syntax")
        self.trace+="Exiting AssignStmt()\n"
    #-------------------------------------
    def optional_else(self):
        'Implementation of OptionalElse non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In OptionalElse()\n"
        print("In OptionalElse()\n")
        if self.checkToken(TokenType.ELSE):
            self.match(TokenType.ELSE)
            self.match(TokenType.OPENBRACE)
            self.stmts()
            self.match(TokenType.CLOSEBRACE)
        else:
            if self.checkToken(TokenType.IF) or self.checkToken(TokenType.FOR) or self.checkToken(TokenType.RETURN) or self.checkToken(TokenType.DATATYPE) or self.checkToken(TokenType.IDENT) or self.checkToken(TokenType.CLOSEBRACE):
                self.trace+="Exiting OptionalElse()\n"
                return
            else:
                self.abort("Incorrect optional else syntax")
        self.trace+="Exiting OptionalElse()\n"
    #-------------------------------------
    def return_stmt(self):
        'Implementation of ReturnStmt non terminal and its production rule in our LL(1) Grammar'

        self.trace+="In ReturnStmt()\n"
        print("In ReturnStmt()\n")
        if self.checkToken(TokenType.RETURN):
            self.match(TokenType.RETURN)
            self.expr()
            self.match(TokenType.SEMICOLON)
        else:
            self.abort("Incorrect return statement syntax")
        self.trace+="Exiting ReturnStmt()\n"
    #-------------------------------------
    def output(self):
        'After parsing is done, the method is called and outputs the error file with lexical and syntactical errors and trace file for the parsing'

        file_name = self.filename[:self.filename.find('.')]
        err_file = open("%s.err" %file_name, 'w')
        err_file.write("\nLexical Errors\n")
        err_file.write(self.errors+"\n")
        err_file.write("\nSyntax Errors\n")
        err_file.write(''.join(self.parser_errors))
        err_file.close()

        trace_file = open("%s.tr" %file_name, 'w')
        trace_file.write(self.trace)
        trace_file.close()
    #-------------------------------------
    


