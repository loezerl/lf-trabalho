from exceptions import *
from operators import *
from lexer import Token
from aux import *

class Parser(object):

	def __init__(self, expression, tokens):
		self.expression = expression
		self.tokens = tokens

	def evaluateNum(self, tokens):
		if len(tokens) == 1 and tokens[0].kind == "num": return tokens[0].value
		else: return None

	def evaluateParenthesis(self, tokens):
		
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

		return self.evaluate(a + [Token("num", self.evaluate(b))] + c)

	def evaluateUnary(self, tokens):

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

		return self.evaluate(a + [Token("num", -self.evaluate(b))] + c)

	def evaluateOperation(self, tokens):

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

		return oper.evalfunc(self.evaluate(a), self.evaluate(b))

	def decode(tokens):

		text = ""
		for token in tokens:
			text += str(token.value)
		return text

	# Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
	def evaluate(self, tokens):

		err = ParseTokenException(None)

		if len(tokens) == 0:
			raise err

		result = self.evaluateNum(tokens)
		if result != None: return result

		result = self.evaluateParenthesis(tokens)
		if result != None: return result		

		result = self.evaluateUnary(tokens)
		if result != None: return result
		
		result = self.evaluateOperation(tokens)
		if result == None:
			raise err

		return result

	def parse(self):

		try: return self.evaluate(self.tokens)
		except ParseTokenException as ex:
			if ex.token == None: expressionInvalid("Could not parse expression", self.expression, -1)
			else: 				 expressionInvalid("Could not parse expression", self.expression, ex.token.position)