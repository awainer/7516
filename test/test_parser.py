'''
Created on 23/8/2015

@author: ari
'''
import unittest

from cStringIO import StringIO 
import scanner
import parser

class Test(unittest.TestCase):


    #===========================================================================
    # def test_parse_var_declaration(self):
    #     txt = StringIO()
    #     txt.write("var a.")
    #     txt.seek(0)
    #     my_scanner = scanner.Scanner(txt)
    #     my_parser = parser.Parser(my_scanner)
    #     print my_parser.parse()
    # 
    #===========================================================================

#    def test_parse_bien0(self):
#        with open('../ejemplos/BIEN-00.PL0') as txt:
#            my_scanner = scanner.Scanner(txt)
#            my_parser = parser.Parser(my_scanner)
#            print my_parser.parse()            

    def test_parse_const_declaration(self):
        s = 'const a=2.'
        txt = StringIO()
        txt.write(s)
        txt.seek(0)
        my_scanner = scanner.Scanner(txt)
        #tok = my_scanner.next_token()
        #while tok:
        #    print tok
        #    tok = my_scanner.next_token()
        my_parser = parser.Parser(my_scanner)
        print my_parser.parse()
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
