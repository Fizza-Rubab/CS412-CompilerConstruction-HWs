'''
-------------------      CS-421-HOMEWORK 2     -------------------      
----------------            Syntax-Analyzer              --------------            

    -------------------------GROUP MEMBERS:-------------------------
                ------Fizza Rubab
                ------Iqra Siddiqui

'''
'''
In this file i.e. main.py, we have imported the Parser class from parser2.py that that holds all the attribute and methods required for parsing. The Parser class also uses lexer class from lexer_analyzer2.py, that was implemented as a part of hw1.  
 
'''

from parser2 import Parser

parse = Parser()
parse.run_parser("test01.tpl")
parse.run_parser("test02.tpl")
parse.run_parser("test03.tpl")
parse.run_parser("test04.tpl") 
parse.run_parser("test05.tpl")
parse.run_parser("test06.tpl")
