def is_num(c):
	return c >= '0' and c <= '9'

def expressionInvalid(title, expression, position):
	print (expression)
	if position >= 0:
		print (" " * position + "^")