class TokenizerException(Exception):
	def __init__(self, expression, position):
		super().__init__()
		self.expression = expression
		self.position = position

class ParseTokenException(Exception):
	def __init__(self, token):
		super().__init__()
		self.token = token