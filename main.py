import stacks as S
import lexer as L
import parser as P
import evaluator as E
import sys, os

lexes = []
locations = {}

if len(sys.argv) > 1:
    foundFile = -1
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            foundFile = i

	if foundFile == -1:
        code = sys.argv[1]
	else:
        source = open(sys.argv[foundFile], "r")
        code = source.read()
	
	code += " "

	lexes = L.tokenize(code)
	locations = P.mapNames(lexes)
	E.evaluate(lexes, locations)

#Hereby on 6:06, July 9, 2020, Itzz me is declared confused.