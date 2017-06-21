# -*- coding: utf-8 -*-

import math
import sys
from enum import Enum

class Operator:

	def __init__(self, char, evalfunc, assocLeft):
		self.char = char
		self.evalfunc = evalfunc
		self.assocLeft = assocLeft

	def evaluate(self, num1, num2):
		return 0

# lower to higher priority
operators = [
	[Operator('-', lambda x, y: x - y, True), Operator('+', lambda x, y: x + y, True)],
	[Operator('/', lambda x, y: x / y, True), Operator('*', lambda x, y: x * y, True)],
	[Operator('^', lambda x, y: math.pow(x, y), False)]
]

# Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
# Num ::= [0-9]+([.][0-9]+)?
# BinOp ::= + | - | * | / | ^

class Token:
	
	kind = ""
	value = None

	def __init__(self, kind, value):
		self.kind = kind
		self.value = value

	def __repr__(self):

		desc = self.kind
		if self.value != None:
			desc += "[" + str(self.value) + "]"
		return desc

def evaluateNum(tokens):
	if len(tokens) == 1 and tokens[0].kind == "num": return tokens[0].value
	else: return None

def evaluateParenthesis(tokens):
	
	i = 0
	for token in tokens:
		if token.kind == "block" and token.value == "(": break
		i += 1

	if i >= len(tokens):
		return None

	start = i
	end = start + 1
	count = 1

	while end < len(tokens):
		token = tokens[end]
		if token.kind == "block":
			if token.value == "(": count += 1
			elif token.value == ")": count -= 1
			if count == 0:
				break
		end += 1

	if count != 0:
		return None

	a = tokens[:start]
	b = tokens[start+1:end]
	c = tokens[end+1:]

	return evaluate(a + [Token("num", evaluate(b))] + c)

def evaluateUnary(tokens):

	i = 0
	while i < len(tokens):
		token = tokens[i]

		if token.kind == "oper" and token.value == "-" and \
		   	(i == 0 or tokens[i-1].kind != "num") and tokens[i+1].kind == "num":
			break

		i += 1

	if i >= len(tokens):
		return None

	a = tokens[:i]
	b = [tokens[i+1]]
	c = tokens[i+2:]

	return evaluate(a + [Token("num", -evaluate(b))] + c)

def evaluateOperation(tokens):
	
	oper = None
	for ops in operators:
		
		i = len(tokens) - 1
		while i >= 0:

			for op in ops:

				token = tokens[i]
				if token.kind == "oper" and token.value == op.char:
					oper = op
					break
			if oper != None: break
			i -= 1
		if oper != None: break

	if oper == None:
		return None

	if i <= 0 or i >= len(tokens) - 1:
		raise Exception("Expression error.")

	a = tokens[:i]
	b = tokens[i+1:]

	return oper.evalfunc(evaluate(a), evaluate(b))
	
	return result

def decode(tokens):

	text = ""
	for token in tokens:
		text += str(token.value)
	return text

def evaluate(tokens):

	err = Exception("Could not evaluate tokens: ", tokens)

	if len(tokens) == 0:
		raise err

	result = evaluateNum(tokens)
	if result != None: return result

	result = evaluateParenthesis(tokens)
	if result != None: return result		

	result = evaluateUnary(tokens)
	if result != None: return result
	
	result = evaluateOperation(tokens)
	if result == None:
		raise err

	return result

def is_num(c):
	return c >= '0' and c <= '9'

class Lexer:

	@staticmethod
	def scan(exp):

		i = 0
		tokens = []

		try:	
			while i < len(exp):

				c = exp[i]
				token = None

				# scan number
				if is_num(c):
					
					numstr = ""
					while is_num(c) and i < len(exp):
						numstr += c
						i += 1

						if i != len(exp):
							c = exp[i]

					# scan floating number
					if c == '.':

						if i >= len(exp) - 1 or not is_num(exp[i + 1]):
							raise Exception()

						numstr += '.'

						i += 1
						c = exp[i]

						while is_num(c) and i < len(exp):
							numstr += c
							i += 1

							if i != len(exp):
								c = exp[i]
					
					i -= 1
					token = Token("num", float(numstr))

				# scan parenthesis
				elif c in ['(', ')']:
					token = Token("block", str(c))

				# scan operations
				elif c in ['+', '-', '*', '/', '^']:
					token = Token("oper", str(c))

				# ignores empty space
				elif c != ' ' and c != '\t':
					raise Exception()

				if token != None:
					tokens.append(token)

				i += 1
		
		except Exception:
			print ("### Expression error near column", i)
			print (exp)
			print (" " * i + "^")
			return None

		return tokens

if len(sys.argv) != 2:
	print("USAGE: <EXP>")
	sys.exit(0)

expressao = sys.argv[1]
tokens = Lexer.scan(expressao)

if tokens != None:
	result = evaluate(tokens)
	print("Resultado: ", result)

