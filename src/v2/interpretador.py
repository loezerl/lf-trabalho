# -*- coding: utf-8 -*-

import math
import sys
from enum import Enum

class TokenizerException(Exception):
	def __init__(self, expression, position):
		super().__init__()
		self.expression = expression
		self.position = position

class ParseTokenException(Exception):
	def __init__(self, token):
		super().__init__()
		self.token = token

class OperatorSet:

	def __init__(self, operators, assocLeft):
		self.operators = operators
		self.assocLeft = assocLeft

class Operator:

	def __init__(self, char, evalfunc):
		self.char = char
		self.evalfunc = evalfunc

	def evaluate(self, num1, num2):
		return 0

# lower to higher priority
operators = [
	OperatorSet([Operator('-', lambda x, y: x - y), Operator('+', lambda x, y: x + y)], True),
	OperatorSet([Operator('/', lambda x, y: x / y), Operator('*', lambda x, y: x * y)], True),
	OperatorSet([Operator('^', lambda x, y: math.pow(x, y))], False)
]

# Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
# Num ::= [0-9]+([.][0-9]+)?
# BinOp ::= + | - | * | / | ^

class Token:
	
	kind = ""
	value = None
	position = 0

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
		if token.kind == "block":
			if token.value == "(": break
			elif token.value == ")":
				raise ParseTokenException(token)
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
		raise ParseTokenException(tokens[start])

	a = tokens[:start]
	b = tokens[start+1:end]
	c = tokens[end+1:]

	if len(b) == 0:
		raise ParseTokenException(tokens[start+1])

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
	for opset in operators:
		
		inc = 1
		i = 0

		if opset.assocLeft: 
			inc = -1
			i = len(tokens) - 1

		while (opset.assocLeft and i >= 0) or (not opset.assocLeft and i < len(tokens)):

			for op in opset.operators:

				token = tokens[i]
				if token.kind == "oper" and token.value == op.char:
					oper = op
					break
			if oper != None: break
			i += inc
		if oper != None: break

	if oper == None:
		return None

	if i == 0 or i == len(tokens) - 1:
		raise ParseTokenException(tokens[i])

	a = tokens[:i]
	b = tokens[i+1:]

	return oper.evalfunc(evaluate(a), evaluate(b))

def decode(tokens):

	text = ""
	for token in tokens:
		text += str(token.value)
	return text

# Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
def evaluate(tokens):

	err = ParseTokenException(None)

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

def parse(tokens):

	try: return evaluate(tokens)
	except ParseTokenException as ex:
		if ex.token == None: expressionInvalid("Could not parse expression", expression, -1)
		else: 				 expressionInvalid("Could not parse expression", expression, ex.token.position)

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
							raise TokenizerException(exp, i)

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
					raise TokenizerException(exp, i)

				if token != None:
					token.position = i
					tokens.append(token)

				i += 1
		
		except TokenizerException as ex:
			expressionInvalid("Expression error near column " + str(i), ex.expression, ex.position)
			return None

		return tokens

def expressionInvalid(title, expression, position):
	print (expression)
	if position >= 0:
		print (" " * position + "^")

if len(sys.argv) != 2:
	print("USAGE: <EXP>")
	sys.exit(0)

expression = sys.argv[1]
tokens = Lexer.scan(expression)

if tokens == None:
	print("Lexer error.")
	sys.exit(1)

result = parse(tokens)
if result == None:
	print("Parser error.")
	sys.exit(2)

print(result)

