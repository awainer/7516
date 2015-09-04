'''
Created on 23/8/2015

@author: ari
'''
import unittest

from io import StringIO
import scanner
import pl0_parser


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
        self.assert_(my_parser.parse(debug=1))
        txt.close()

    def test_parse_minimum_program(self):
        self.generic_test(".")

    def test_parse_single_const(self):
        self.generic_test("const A.")

    def test_parse_single_const_sc(self):
        self.generic_test("const A=6;.")

    def test_parse_multiple_const(self):
        self.generic_test("const A,B.")

    def test_parse_multiple_const_with_assigment(self):
        self.generic_test("const A=1,B.")

    def test_single_var_decl(self):
        self.generic_test("var a;.")

    def test_multi_var_decl(self):
        self.generic_test("var a,b,c,d;.")

    def test_var_and_const_decl(self):
        self.generic_test("const a,b,c; var d, e , f;.")

    def test_proc_decl(self):
        self.generic_test("procedure garompa1;.")
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
