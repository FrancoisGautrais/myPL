#!/usr/bin/python3
from .symbollexer import SymbolLexer

class StringIOWrapper:
	def __init__(self, text):
		self.text=text
		self.index=0
		self.len=len(text)
		self.char=""
	
	def read(self, n):
		if self.index>=self.len: return ""
		self.char=self.text[self.index]
		self.index+=1
		return self.char

class Lexer:
	TOK_UNKNOWN=-1
	TOK_END=0
	TOK_ADD=1
	TOK_MUL=2
	TOK_DIV=3
	TOK_SUB=4
	TOK_INT=5
	TOK_FLOAT=6
	TOK_PO=7
	TOK_PF=8
	TOK_IDENT=9
	TOK_STRING=10
	TOK_KEYWORD=11
	TOK_CMP=12
	TOK_NOT=13
	TOK_BOOL=14
	TOK_OR=15
	TOK_AND=16
	TOK_AFF=17
	TOK_VIRGULE=18
	TOK_PVIRGULE=19
	TOK_AO=20
	TOK_AF=21
	TOK_PLUSPLUS=22
	TOK_PLUSEQUALS=23
	TOK_MINUSUSMINUS=24
	TOK_MINUSEQUALS=25
	TOK_DIVEQUALS=26
	TOK_MULTEQUALS=27
	TOK_MODULO=28
	TOK_MODULOEQUALS=29
	TOK_BOR=30
	TOK_BOREQUALS=31
	TOK_BAND=32
	TOK_BANDEQUALS=33
	TOK_OREQUALS=34
	TOK_ANDEQUALS=35
	TOK_REF=36

	TOKEN_LIST=["END", "ADD", "MUL", "DIV", "SUB", "INT", "FLOAT",
							"P OOUVRANTE", "P FERMANTE", "IDENT", "STRING", "KEYWORD", 
							"CMP", "NOT", "BOOL", "OR", "AND", "AFF", "VIRGULE", "PVIRGULE",
				"AO", "AF", "PLUSPLUS", "PLUSEQUALS", "MINUSMINUS", "MINUSEQUALS", "DIVEQUALS",
				"MULTEQUALS", "MODULO", "MODULOEQUALS", "BOR", "BOREQUALS", "BAND", "BANDEQUALS",
				"OREQUALS", "ANDEQUALS", "REF"]
	SEPARATOR=" \t\n\r"


	@staticmethod
	def isAff(tok):
		return tok in [Lexer.TOK_PLUSEQUALS, Lexer.TOK_MINUSEQUALS,
					   Lexer.TOK_DIVEQUALS, Lexer.TOK_MULTEQUALS, Lexer.TOK_MODULOEQUALS, Lexer.TOK_BOREQUALS,
					   Lexer.TOK_BANDEQUALS, Lexer.TOK_OREQUALS, Lexer.TOK_ANDEQUALS, Lexer.TOK_AFF]


	OPERATION={
		"+" : TOK_ADD,
		"*" : TOK_MUL,
		"/" : TOK_DIV,
		"-" : TOK_SUB,
		"(" : TOK_PO,
		")" : TOK_PF,
		"!" : TOK_NOT,
		"," : TOK_VIRGULE,
		";" : TOK_PVIRGULE,
		"{" : TOK_AO,
		"}" : TOK_AF,
		"++" : TOK_PLUSPLUS,
		"+=" : TOK_PLUSEQUALS,
		"--" : TOK_MINUSUSMINUS,
		"-=" : TOK_MINUSEQUALS,
		"/=" : TOK_DIVEQUALS,
		"*=" : TOK_MULTEQUALS,
		"%" : TOK_MODULO,
		"%=" : TOK_MODULOEQUALS,
		"|" : TOK_BOR,
		"|=" : TOK_BOREQUALS,
		"&" : TOK_BAND,
		"&=" : TOK_BANDEQUALS,
		"||" : TOK_OR,
		"||=" : TOK_OREQUALS,
		"&&" : TOK_AND,
		"&&=" : TOK_ANDEQUALS,
		"=" : TOK_AFF,
		"<" : TOK_CMP,
		"<=" : TOK_CMP,
		">" : TOK_CMP,
		">=" : TOK_CMP,
		"==" : TOK_CMP,
		"." : TOK_REF
	}
	KEYWORDS={
		"if" : TOK_KEYWORD, 
		"elif" : TOK_KEYWORD,
		"else" : TOK_KEYWORD,
		"def" : TOK_KEYWORD,
		"while" : TOK_KEYWORD,
		"for" : TOK_KEYWORD,
		"or" : TOK_OR,
		"and" : TOK_AND,
		"return" : TOK_KEYWORD
	}
	NUMBER="0123456789"
	IDENT="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
	CMP="=<>!"
	COMPARES=["=","==", "!", "!=", "<", "<=", ">",">="]
	def __init__(self, fd):
		self.fd=fd
		self.token=Lexer.OPERATION
		self.char=""
		self.data=None
		self.current=""
		self._nc()
		self.isFinished=False
		self.symbols=SymbolLexer(Lexer.OPERATION.keys())
	
	def _nc(self):
		self.char=self.fd.read(1)
		return self.char
	
	def _setToken(self, tok, string, data=None):
		self.token=tok
		if tok==Lexer.TOK_END:
			self.isFinished=True
		self.data=data if data!=None else string
		self.current=string
		return self.token
	
	def _trim(self):
		while (self.char in Lexer.SEPARATOR) and self.char!="": self._nc()
	
	def _number(self):
		isFloat=False
		string=self.char
		self._nc()
		while (self.char in Lexer.NUMBER) and self.char!="":
			string+=self.char
			self._nc()
			
		if self.char==".": 
			string+="."
			self._nc()
			while (self.char in Lexer.NUMBER) and self.char!="":
				string+=self.char
				self._nc()
			return self._setToken(Lexer.TOK_FLOAT, string, float(string))
		return self._setToken(Lexer.TOK_INT, string, int(string))
	
	def _ident(self):
		string=""
		while (self.char in Lexer.IDENT) and self.char!="":
			string+=self.char
			self._nc()
		return self._setToken(Lexer.TOK_IDENT, string, string)
	
	def _cmp(self):
		string=self.char
		self._nc()
		if (self.char in self.CMP) and self.char!="":
			string+=self.char
			self._nc()
		if string=="=": return self._setToken(Lexer.TOK_AFF, string, string)
		return self._setToken(Lexer.TOK_CMP, string, string)
	
	def _string(self):
		string=""
		self._nc()
		while (self.char!="\"" or (len(string)>0 and  string[-1]=="\\") ) and self.char!="":
			string+=self.char
			self._nc()
		if self.char!="\"":
			raise Exception("Erreur _string: chaine non terminée")
		self._nc()
		return self._setToken(Lexer.TOK_STRING, string, string)

	def next(self):
		self.current=""
		self._trim()
		if self.char=="":
			x=self._setToken(Lexer.TOK_END, None, None)
			self._nc()
			return x

		#entre ici
		ret=self.symbols.readNext(self.char, self)
		if ret:
			return self._setToken(Lexer.OPERATION[ret], ret)

		"""
		if self.char in Lexer.OPERATION:
			x=self._setToken(Lexer.OPERATION[self.char], self.char)
			self._nc()
			return x
		"""
		#et la

		if self.char in Lexer.NUMBER or self.char=='-':
			return self._number()

		if self.char=="\"":
			return self._string()

		if self.char in Lexer.IDENT:
			x=self._ident()
			if self.current.lower()=="true": return self._setToken(Lexer.TOK_BOOL, self.current, True)
			if self.current.lower()=="false": return self._setToken(Lexer.TOK_BOOL, self.current, False)
			if self.current in Lexer.KEYWORDS:
				return self._setToken(Lexer.KEYWORDS[self.current], self.current, self.current)
			return x
	
	@staticmethod
	def tokstr(tok):
		if tok==None:
			return "UNKNOWN"
		if tok>=0 and tok<len(Lexer.TOKEN_LIST):
			return Lexer.TOKEN_LIST[tok]
		return "UNKNOWN"

	def read(self, n=1):
		return self._nc()


