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
VAR R, N;

PROCEDURE INICIALIZAR;
CONST UNO = 1;
R := -(-UNO);

PROCEDURE RAIZ;
BEGIN
  CALL INICIALIZAR;
  WHILE R * R < N DO R := R + 1
END;

BEGIN
  WRITE ('N: '); READLN (N);
  WRITE ('RAIZ CUADRADA DE ', N, ': ');
  IF N < 0 THEN WRITE ('ERROR');
  IF N = 0 THEN WRITE (0);
  IF N > 0 THEN
    BEGIN
      CALL RAIZ;
      IF R*R<>N THEN WRITE (R - 1, '..');
      WRITE (R);
    END;
  WRITELN
END.

             '''
        txt.write(p)
        txt.seek(0)
        scanner = Scanner(txt)
        parser = Parser(scanner)
        parser.parse()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()