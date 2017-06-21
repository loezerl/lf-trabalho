from aux import *
from exceptions import *

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

class Lexer:

	@staticmethod
	def scan(expression):

		i = 0
		tokens = []

		try:	
			while i < len(expression):

				c = expression[i]
				token = None

				# scan number
				if is_num(c):
					
					numstr = ""
					while is_num(c) and i < len(expression):
						numstr += c
						i += 1

						if i != len(expression):
							c = expression[i]

					# scan floating number
					if c == '.':

						if i >= len(expression) - 1 or not is_num(expression[i + 1]):
							raise TokenizerException(expression, i)

						numstr += '.'

						i += 1
						c = expression[i]

						while is_num(c) and i < len(expression):
							numstr += c
							i += 1

							if i != len(expression):
								c = expression[i]
					
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
					raise TokenizerException(expression, i)

				if token != None:
					token.position = i
					tokens.append(token)

				i += 1
		
		except TokenizerException as ex:
			expressionInvalid("Expression error near column " + str(i), ex.expression, ex.position)
			return None

		return tokens