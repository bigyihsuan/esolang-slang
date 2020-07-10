from enum import Flag, auto
import string
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
	COMMENT = auto()
	END = auto()

class LexerState(Flag):
	BEGIN = auto()
	INNAME = auto()
	INDEF = auto()
	INCOMMENT = auto()


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
		return "<Lex: {}, {}>\n".format(self.token, repr(self.lexeme))


def getNextToken(code, debugmode):
	# returns a tuple that contains:
	#	a Lex that contains the lexeme and its token
	#	the code with the Lex removed
	chars = {"(": Token.IFSTART, ")": Token.IFEND}
	lexeme = ""
	state = LexerState.BEGIN
	for i, c in enumerate(code):
		if debugmode:
			print("saw", repr(c))
		if state == LexerState.BEGIN:
			if c in string.whitespace:
				code = code[1:]
				continue
			if c in chars:  # check for ifs
				return (Lex(chars[c], c), code[1:])
			elif c in ":":  # check for assignemnt op
				return (Lex(Token.DEFSTART, ":="), code[2:])
			elif c in "/":
				state = LexerState.INCOMMENT
			elif c not in " \n\t():":  # a name is found, continue until whitespace or (): is hit
				state = LexerState.INNAME
		lexeme += c
		if state == LexerState.INCOMMENT:
			if c in "\n":  # comments end at a newline
				return (Lex(Token.COMMENT, lexeme), code[len(lexeme):])
		elif state == LexerState.INNAME:
			if c in " \n\t():":  # names end at one of these
				return (Lex(Token.NAME, lexeme[:-1]), code[len(lexeme) - 1:])
	return (Lex(Token.END, ""), "")


def tokenize(code, debugmode):
	# input is code
	# output is a list of Lexes
	lexes = []
	c = code
	lastTok = Token.BEGIN
	inDefinition = False
	if debugmode: print("Creating lex list:")
	while lastTok != Token.END:
		if debugmode:
			print(lexes, c)
		l, c = getNextToken(c, debugmode)
		lexes.append(l)
		if inDefinition and l.token in [Token.NAME, Token.IFEND] and c[0] in "\n":
			lexes.append(Lex(Token.DEFEND, ""))
			lastTok = Token.DEFEND
		else:
			lastTok = l.token
		if l.token == Token.DEFSTART and not inDefinition:
			inDefinition = True
	return lexes
