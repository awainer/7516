'''
Created on Sep 10, 2015

@author: ari
'''
import unittest
import scanner
import pl0_parser
import  importlib
class Test(unittest.TestCase):

    def setUp(self):
        importlib.reload(pl0_parser)
        importlib.reload(scanner)

    def test_ejemplo_0(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-00.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-00.ELF')
        parser.parse()

    def test_ejemplo_1(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-01.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-01.ELF')
        parser.parse()

    def test_ejemplo_2(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-02.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-02.ELF')
        parser.parse()


    def test_ejemplo_3(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-03.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-03.ELF')
        parser.parse()

    def test_ejemplo_4(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-04.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-04.ELF')
        parser.parse()

    def test_ejemplo_5(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-05.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-05.ELF')
        parser.parse()

    def test_ejemplo_6(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-06.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-06.ELF')
        parser.parse()

    def test_ejemplo_7(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-07.PL0", 'r'))

        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-07.ELF')
        parser.parse()

    def test_ejemplo_8(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-08.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-08.ELF')
        parser.parse()

    def test_ejemplo_9(self):
        my_scanner = scanner.Scanner(open("../ejemplos/BIEN-09.PL0", 'r'))
        parser = pl0_parser.Parser(my_scanner,output_file='BIEN-09.ELF')
        parser.parse()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_ejemplo_0']
    unittest.main()
