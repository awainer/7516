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
        my_parser.parse(debug=1)
        txt.close()

    def test_parse_minimum_program(self):
        self.generic_test(".")

    def test_parse_single_const_sc(self):
        self.generic_test("const A=6;.")

    def test_parse_multiple_const(self):
        self.generic_test("const C=0,B=1;.")

    def test_single_var_decl(self):
        self.generic_test("var a;.")

    def test_multi_var_decl(self):
        self.generic_test("var a,b,c,d;.")

    def test_var_and_const_decl(self):
        self.generic_test("const a=0,b=2; var d, e , f;.")

    def test_proc_decl_empty_body(self):
        self.generic_test("procedure foo; ; .")

    def test_proc_decl_with_body(self):
        self.generic_test("procedure foo;const a;;.")

    def test_parse_assign(self):
        self.generic_test("var a; a := 1.")

    def test_parse_assign_menosuno(self):
        self.generic_test('var R,UNO; R := -(-UNO).')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
