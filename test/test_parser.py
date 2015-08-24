'''
Created on 23/8/2015

@author: ari
'''
import unittest

from cStringIO import StringIO 
import scanner
import parser

class Test(unittest.TestCase):


    def test_parse_factor(self):
        txt = StringIO()
        txt.write(".")
        txt.seek(0)
        
        my_scanner = scanner.Scanner(txt)
        
        my_parser = parser.Parser(my_scanner)
        
        my_parser.parse()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()