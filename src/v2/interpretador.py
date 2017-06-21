# -*- coding: utf-8 -*-

import sys
from lexer import Lexer
from parser import Parser

# Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
# Num ::= [0-9]+([.][0-9]+)?
# BinOp ::= + | - | * | / | ^

if len(sys.argv) != 2:
	print("USAGE: <EXP>")
	sys.exit(0)

expression = sys.argv[1]

# lexer
tokens = Lexer.scan(expression)
if tokens == None:
	print("Lexer error.")
	sys.exit(1)

# parser
parser = Parser(expression, tokens)
result = parser.parse()

if result == None:
	print("Parser error.")
	sys.exit(2)

# print result
print(result)
