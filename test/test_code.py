'''
Created on Sep 29, 2015

@author: ari
'''
import unittest
from code_writer import CodeWriter

class Test(unittest.TestCase):

    def test_mov_edi_literal(self):
        writer = CodeWriter()
        writer.mov_edi_literal(1234)
        code = writer.get_code()
        inst = code[len(code)-5:]
        expected = [0xbf, 0xd2, 0x4, 0, 0]
        for i in range(len(expected)):
            self.assertEqual(inst[i], expected[i])

    def test_fixup(self):
        writer = CodeWriter()
        writer.add_literals([0,0,0,0,0,0xbf,0,0,0,0])
        fixval = [0x1,0x2,0x3,0x4]
        writer.fixup(6, fixval)
        code = writer.get_code()
        for i in range(len(fixval)):
            self.assertEqual(code[6+i], fixval[i])
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()