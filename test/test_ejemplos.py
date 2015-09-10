'''
Created on Sep 10, 2015

@author: ari
'''
import unittest
import scanner
import pl0_parser

class Test(unittest.TestCase):


    def test_ejemplo_0(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-00.PL0",'r'))
        parser = pl0_parser.Parser(my_scanner)
        parser.parse()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_ejemplo_0']
    unittest.main()