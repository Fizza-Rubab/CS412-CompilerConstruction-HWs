'''
-------------------      CS-421-HOMEWORK 1-PART 2      -------------------      
----------------            Lexical-Analyzer              --------------            

    -------------------------GROUP MEMBERS:-------------------------
                ------Fizza Rubab
                ------Iqra Siddiqui

'''
'''
In this file i.e. main.py, we have imported the Lexer class from lexical_analyzer.py and activated lexical analyzer for TUPLE on test file. 
While implementing lexical analyzer, we have assumed following:
- %write assumptions here
 
'''

from lexical_analyzer import Lexer #importing Lexer class

lex=Lexer() 
lex.lexer_activate("test01.tpl")
#lex.lexer_activate("test02.tpl")
lex.lexer_activate("test03.tpl")