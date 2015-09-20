'''
Created on 14 de set. de 2015

@author: ari
'''
import unittest
import pl0_parser
from io import StringIO
import scanner

class Test(unittest.TestCase):

    def get_txt(self, text):
        txt = StringIO()
        txt.write(text)
        txt.seek(0)
        return txt

    def generic_test(self, text):
        txt = self.get_txt(text)
        my_scanner = scanner.Scanner(txt)
        my_parser = pl0_parser.Parser(my_scanner)
        my_parser.parse(debug=1)
        txt.close()

    def test_re_declare_var(self):
        self.generic_test('var a,b,c;\n procedure foo; var a;;.')
        
    def test_wrong_type(self):
        with self.assertRaises(ValueError):
            self.generic_test('var a,b,c;\n call a.')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()