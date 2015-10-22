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
var X, Y, Z;

procedure MULTIPLICAR;
var A, B, A;
begin
     A := X;
     B := Y;
     Z := 0;
     if X < 0 then A := -A;
     if Y ( 0 then B := -B;
     while B > 0 then
         begin
           if odd B then Z:= Z + A;
           A := A * 2;
           B := B / 2
         end;
     if X < 0 then Z:= -Z;
     if Y < 0 then Z:= -Z
end;

Begin
     write ('X: '); readLn X;
     write ('Y: '); readLn (Y);
     MULTIPLICAR;
     writeLn ('X*Y=', Z);
end.


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