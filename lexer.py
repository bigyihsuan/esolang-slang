from enum import Flag, auto

"""
program = (__ name __ ":=" code)+ __
code = (_ (name | "(" code _ ")" ) )*
name = /[^ \n\t():]+/
_ = " "*
__ = /[ \n\t]*/
"""

# program is 0+ whitespace, 1 name, 0+ whitespace, 1 ":=", 1 code, 1+; 0+ whitespace
# code is 0+ spaces, then 1 name OR "(" code, 0+ spaces, ")"; 0+
# name is 1+ nonwhitespace or "():" characters
# _ is 0+ spaces
# __ is 0+ whitespace

class Token(Flag):
	# Defines the tokens
	BEGIN = auto()
	NAME = auto()
	DEFSTART = auto()
	DEFEND = auto()
	IFSTART = auto()
	IFEND = auto()
	END = auto()

class LexerState(Flag):
	BEGIN = auto()
	INNAME = auto()
	INDEF = auto()


# https://github.com/bigyihsuan/International-Phonetic-Esoteric-Language/blob/master/src/lexer.py
class Lex:
    """
    Defines a lexeme. Contains the token, and the lexed characters.
    """
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __eq__(self, token):
        return self.token == token

    def __ne__(self, token):
        return self.token != token

    def __repr__(self):
        return "<Lex: {}, {}>".format(self.token, repr(self.lexeme))

def getNextToken(code):
	chars = {"(": Token.IFSTART, ")": Token.IFEND}
	# returns a tuple that contains:
	#	a Lex that contains the lexeme and its token
	#	the code with the Lex removed
	lexeme = ""
	for i,c in enumerate(code):
		if c in chars: # check for ifs
			return (Lex(chars[c], c), code[i+1:])
		if c in ":": # check for assignemnt op
			if code[i+1] in "=":
				return (Lex(Token.DEFSTART, ":="), code[i+2:])
		elif c not in " \n\t():": # a name is found, continue until whitespace or (): is hit
			lexeme += c
			continue
		elif c in "\n": # definitions end at a newline
			return (Lex(Token.DEFEND, ""), code[i+1:])
		elif len(code) > 0:
			return (Lex(Token.NAME, lexeme), code[i+len(lexeme):])
		else:
			return (Lex(Token.END, ""), "")
def tokenize(code):
	# input is code
	# output is a list of Lexes
	lexes = []
	c = code
	lastTok = Token.BEGIN
	while lastTok != Token.END:
		l,c = self.getNextToken(c)
		lastTok = l.token
		lexes.append(l)
	return lexes

