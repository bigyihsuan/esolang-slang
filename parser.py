from lexer import Token as T

def mapNames(lexes, debugmode):
	# input is a list of Lexes
	# output is a dictionary mapping names to locations in the lexList
	locations = {}
	nesting = []
	for i,l in enumerate(lexes):
		# IFSTART points to its IFEND for condiitonal execution
		# 	IFs can be nested
		# names point to their definition
		# map str name to int definition location
		# map int if start to int if end
		if debugmode:
			print(nesting, locations)
		if l.token == T.DEFSTART:
			locations[lexes[i-1].lexeme] = i+1
		elif l.token == T.IFSTART:
			nesting.append(i)
		elif l.token == T.IFEND:
			locations[nesting.pop()] = i
	return locations