import scanner
import pl0_parser
import sys
import os

filename = sys.argv[1]
my_scanner = scanner.Scanner(open(filename, 'r'))
parser = pl0_parser.Parser(my_scanner,output_file=os.path.basename(filename) + '.elf')
parser.parse()

