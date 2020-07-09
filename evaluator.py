from lexer import Token as T
import stacks as s

commands = ("new","pop","enter","exit","warp","send","read","write") # pre defined

cursor = s.Cursor()

def evaluate(lexes, locations):
	# input is a Lex list, and a dict of locations
	# outputs nothing
	ep = locations["main"] if "main" in locations else len(lexes)
	executionStack = []
	while ep < len(lexes):
		if lexes[ep].token == T.NAME: # jump to the name definition
			if lexes[ep].lexeme in "new":
				cursor.new()
			elif lexes[ep].lexeme in "pop":
				cursor.pop()
			elif lexes[ep].lexeme in "enter":
				cursor.enter()
			elif lexes[ep].lexeme in "exit":
				cursor.exit()
			elif lexes[ep].lexeme in "warp":
				cursor.warp()
			elif lexes[ep].lexeme in "send":
				cursor.send()
			elif lexes[ep].lexeme in "read":
				cursor.read()
			elif lexes[ep].lexeme in "write":
				cursor.write()
			elif lexes[ep].lexeme in locations:
				executionStack.append(ep)
				ep = locations[lexes[ep].lexeme]
		elif lexes[ep].token == T.DEFEND:
			ep = executionStack.pop()
		elif lexes[ep].token == T.IFSTART:
			if len(cursor.active) == 0: # jump to the endif if empty
				ep = locations[ep]
		ep += 1