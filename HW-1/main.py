'''
-------------------      CS-421-HOMEWORK 1-PART 2      -------------------      
----------------            Lexical-Analyzer              --------------            

    -------------------------GROUP MEMBERS:-------------------------
                ------Fizza Rubab
                ------Iqra Siddiqui

'''
'''
In this file i.e. main.py, we have imported the Lexer class from lexical_analyzer.py and have called run method from this class to
tokenize the file passed in the argument. 
While implementing lexical analyzer, we have assumed following:
1) . is considered as a punctuator. faff110. gets tokenized into <id, num>, <.> . 23.5.9 gets tokenized to <num,23.5><.><num,9>
2) Since str and return not in datatypes or keywords hence are tokenized as identifiers.
string literal and character constants can both begin from either double quotes or single quotes. String literal have length>1
 while char constants have length just 1
 
'''

from lexical_analyzer import Lexer #importing Lexer class

lex = Lexer() 
# lex.run("test01.tpl")
# lex.run("test02.tpl")
lex.run("eh.tpl")