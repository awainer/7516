'''
Created on 10 de oct. de 2015

@author: ari
'''
import unittest
from io import StringIO
from pl0_parser import Parser
from scanner import Scanner

class Test(unittest.TestCase):


    def test_out(self):
        txt = StringIO()
        p = '''
VAR BASE, EXPO, RESU;

PROCEDURE POT;
IF EXPO > 0 THEN
   BEGIN
        RESU := RESU * BASE;
        EXPO := EXPO - 1;
        CALL POT
   END;

BEGIN
     WRITE ('BASE: '); READLN(BASE);
     WRITE ('EXPONENTE: '); READLN(EXPO);
     RESU := 1;
     CALL POT;
     IF EXPO < 0  THEN RESU := 0;
     WRITELN ('RESULTADO: ', RESU);
     WRITELN
END.


             '''
        #WRITE ('RAIZ CUADRADA DE ', N, ': ');
        txt.write(p)
        txt.seek(0)
        scanner = Scanner(txt)
        parser = Parser(scanner)
        parser.parse()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()