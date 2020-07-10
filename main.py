import lexer as L
import parser as P
import evaluator as E
import sys, os

lexes = []
locations = {}
debugmode = False

if len(sys.argv) > 1:
    foundFile = -1
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            foundFile = i

    if sys.argv[1] == "-d":
        debugmode = True

    if foundFile == -1:
        code = sys.argv[2] if debugmode else sys.argv[1]
    else:
        source = open(sys.argv[foundFile], "r")
        code = source.read()

    code += " "

    lexes = L.tokenize(code, debugmode)
    locations = P.mapNames(lexes, debugmode)

    if debugmode:
        print("Lexes:", lexes)
        print("Locations:", locations)

    E.evaluate(lexes, locations, debugmode)

#Hereby on 6:06, July 9, 2020, Itzz me is declared confused.
