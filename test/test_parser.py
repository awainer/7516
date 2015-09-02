'''
Created on 23/8/2015

@author: ari
'''
import unittest

from cStringIO import StringIO 
import scanner
import parser

class Test(unittest.TestCase):

    #--------------------------------------------- def test_unequal_token(self):
        #------------------------------------------------------ txt = StringIO()
        #--------------------------------------------------- txt.write("1 <> 2")
        #----------------------------------------------------------- txt.seek(0)
        #------------------------------------- my_scanner = scanner.Scanner(txt)    

    #===========================================================================
    #------------------------------------- def test_parse_var_declaration(self):
        #------------------------------------------------------ txt = StringIO()
        #------------------------------------------------- txt.write("readln;.")
        #----------------------------------------------------------- txt.seek(0)
        #------------------------------------- my_scanner = scanner.Scanner(txt)
        #--------------------------------- my_parser = parser.Parser(my_scanner)
        #----------------------------------------------------- my_parser.parse()
      
    #----------------------------------- def test_parse_const_declaration(self):
        #------------------------------------------------- s = 'if y < 0 then .'
        #------------------------------------------------------ txt = StringIO()
        #---------------------------------------------------------- txt.write(s)
        #----------------------------------------------------------- txt.seek(0)
        #------------------------------------- my_scanner = scanner.Scanner(txt)
        #--------------------------------- my_parser = parser.Parser(my_scanner)
        #----------------------------------------------------- my_parser.parse()


    def test_parse_bien0(self):
        with open('../ejemplos/BIEN-00.PL0') as txt:
            my_scanner = scanner.Scanner(txt)
            my_parser = parser.Parser(my_scanner)
            my_parser.parse()
        #tok = my_scanner.next_token()
        #------------------------------------------------------------ while tok:
            #--------------------------------------------------------- print tok
            #------------------------------------- tok = my_scanner.next_token()
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
