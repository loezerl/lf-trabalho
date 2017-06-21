# -*- coding: utf-8 -*-

import sys

class Operator:

	def __init__(self, char, evalfunc):
		self.char = char
		self.evalfunc = evalfunc

	def evaluate(self, num1, num2):
		return 0

# lower to higher priority
operators = [
	Operator('-', lambda x, y: x - y),
	Operator('+', lambda x, y: x + y),
	Operator('/', lambda x, y: x / y),
	Operator('*', lambda x, y: x * y)
]

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
	for token in tokens:
		if token.kind == "oper" and token.value == "-": break
		i += 1

	if i >= len(tokens): return None
	return evaluate(tokens[:i] + [Token("num", -evaluate(tokens[i+1:]))])

def evaluateOperation(tokens):
	
	oper = None
	for op in operators:
		i = 0
		for token in tokens:
			if token.kind == "oper" and token.value == op.char:
				oper = op
				break
			i += 1
		if oper != None:
			break

	if oper == None or i <= 0 or i >= len(tokens) - 1:
		return None

	a = tokens[0:i]
	b = tokens[i+1:]

	print "--"
	print "OPER = ", oper.char
	print "RECEBE: ", tokens
	print "A: ", a
	print "B", b

	return oper.evalfunc(evaluate(a), evaluate(b))


def evaluate(tokens):

	err = Exception("Could not evaluate tokens: ", tokens)

	if len(tokens) == 0:
		raise err

	result = evaluateNum(tokens)
	if result != None: return result

	result = evaluateParenthesis(tokens)
	if result != None: return result		

	result = evaluateOperation(tokens)
	if result != None: return result

	result = evaluateUnary(tokens)
	
	if result == None:
		raise err

	return result

def is_num(c):
	return c >= '0' and c <= '9'

class Lexer:

	@staticmethod
	def scan(exp):

		tokens = []

		i = 0
		while i < len(exp):

			c = exp[i]
			token = None

			if c >= '0' and c <= '9':
				
				numstr = ""
				while is_num(c) and i < len(exp):
					numstr += c
					i += 1

					if i != len(exp):
						c = exp[i]
				
				i -= 1

				token = Token("num", int(numstr))
			elif c in ['(', ')']:
				token = Token("block", str(c))
			elif c in ['+', '-', '*', '/']:
				token = Token("oper", str(c))
			elif c != ' ' and c != '\t':
				print "Could not interpret character '" + c + "' at column " + str(i)
				return None

			if token != None:
				tokens.append(token)

			i += 1

		return tokens

if len(sys.argv) != 2:
	print("USAGE: <EXP>")
	sys.exit(0)

expressao = sys.argv[1]
print "Expressão: \"" + expressao + "\""

tokens = Lexer.scan(expressao)
result = evaluate(tokens)
print "Resultado: ", result



