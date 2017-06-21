import math

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